# API Specification
## CRYPTOLENS-AI REST API v1

| Field | Value |
|---|---|
| Base URL | `https://api.cryptolens.ai/api/v1` (prod) / `http://localhost:8000/api/v1` (dev) |
| Version | 1.0 |
| Auth | WebAuthn (Passkeys) — `Authorization: Bearer <access_token>` (JWT issued after WebAuthn verification) |
| Content-Type | `application/json` |
| Streaming | `text/event-stream` (SSE) for `/chat` |
| Interactive Docs | `/docs` (Swagger UI) / `/redoc` (ReDoc) |

---

# Standard Response Envelope

All non-streaming responses use this wrapper:

```json
{
  "success": true,
  "data": { },
  "error": null,
  "meta": {
    "request_id": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2026-03-06T10:00:00Z",
    "version": "1.0"
  }
}
```

Error response:

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": { }
  },
  "meta": { ... }
}
```

---

# Error Codes

| Code | HTTP Status | Description |
|---|---|---|
| `UNAUTHORIZED` | 401 | Missing or invalid Bearer token |
| `TOKEN_EXPIRED` | 401 | Access token expired — use refresh token |
| `FORBIDDEN` | 403 | Authenticated but not permitted for this action |
| `TIER_RESTRICTED` | 403 | Feature requires higher subscription tier |
| `NOT_FOUND` | 404 | Resource does not exist |
| `VALIDATION_ERROR` | 422 | Request body validation failed (Pydantic) |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests for current tier |
| `CHAT_LIMIT_REACHED` | 429 | Daily chat query limit reached (free tier) |
| `LLM_UNAVAILABLE` | 503 | All LLM providers failed or rate limited |
| `VECTOR_DB_ERROR` | 503 | Qdrant unavailable |
| `INTERNAL_ERROR` | 500 | Unexpected server error |

---

# Authentication Endpoints

> CRYPTOLENS-AI sử dụng **WebAuthn (W3C Passkeys standard)** — không password.
> Flow gồm 2 bước (begin + complete) cho cả registration lẫn authentication.
> Sau khi WebAuthn verify thành công, server issue JWT access_token + refresh_token.
> Frontend dùng thư viện `@simplewebauthn/browser` để handle WebAuthn browser API.

---

## POST /auth/webauthn/register/begin

Step 1 of registration — server trả về challenge và options cho trình duyệt.

**Request**
```json
{
  "email": "alex@example.com",
  "full_name": "Alex Nguyen"
}
```

**Response 200**
```json
{
  "success": true,
  "data": {
    "challenge": "base64url-encoded-random-32-bytes",
    "rp": {
      "name": "CRYPTOLENS-AI",
      "id": "cryptolens.ai"
    },
    "user": {
      "id": "base64url-encoded-user-id",
      "name": "alex@example.com",
      "displayName": "Alex Nguyen"
    },
    "pubKeyCredParams": [
      {"type": "public-key", "alg": -7},
      {"type": "public-key", "alg": -257}
    ],
    "timeout": 60000,
    "attestation": "none",
    "authenticatorSelection": {
      "residentKey": "preferred",
      "userVerification": "required"
    }
  }
}
```

Challenge được lưu vào Redis với key `webauthn:reg:{email}`, TTL 5 phút.

**Errors**: `VALIDATION_ERROR` (422) if email already registered

---

## POST /auth/webauthn/register/complete

Step 2 of registration — gửi credential response từ trình duyệt để server verify.

**Request** — body là response từ `navigator.credentials.create()`
```json
{
  "id": "base64url-credential-id",
  "rawId": "base64url-raw-id",
  "response": {
    "clientDataJSON": "base64url...",
    "attestationObject": "base64url..."
  },
  "type": "public-key",
  "device_name": "MacBook Touch ID"
}
```

**Response 201**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "email": "alex@example.com",
      "full_name": "Alex Nguyen",
      "role": "free"
    },
    "credential": {
      "id": "uuid",
      "device_name": "MacBook Touch ID",
      "created_at": "2026-03-06T10:00:00Z"
    },
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "token_type": "bearer",
    "expires_in": 900
  }
}
```

**Errors**: `VALIDATION_ERROR` (422) invalid credential, `UNAUTHORIZED` (401) challenge expired or mismatch

---

## POST /auth/webauthn/login/begin

Step 1 of authentication — server trả về challenge.

**Request**
```json
{
  "email": "alex@example.com"
}
```

**Response 200**
```json
{
  "success": true,
  "data": {
    "challenge": "base64url-encoded-random-32-bytes",
    "rpId": "cryptolens.ai",
    "allowCredentials": [
      {
        "id": "base64url-credential-id",
        "type": "public-key"
      }
    ],
    "userVerification": "required",
    "timeout": 60000
  }
}
```

Challenge lưu vào Redis với key `webauthn:auth:{email}`, TTL 5 phút.

**Errors**: `NOT_FOUND` (404) if email not registered

---

## POST /auth/webauthn/login/complete

Step 2 of authentication — verify chữ ký; issue JWT.

**Request** — body là response từ `navigator.credentials.get()`
```json
{
  "id": "base64url-credential-id",
  "rawId": "base64url-raw-id",
  "response": {
    "clientDataJSON": "base64url...",
    "authenticatorData": "base64url...",
    "signature": "base64url...",
    "userHandle": "base64url-user-id"
  },
  "type": "public-key"
}
```

**Response 200**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "token_type": "bearer",
    "expires_in": 900,
    "user": {
      "id": "uuid",
      "email": "alex@example.com",
      "role": "pro"
    }
  }
}
```

**Errors**: `UNAUTHORIZED` (401) invalid signature, challenge mismatch, or sign_count anomaly (possible clone)

---

## GET /auth/credentials

List user's registered passkeys.

**Headers**: `Authorization: Bearer <access_token>`

**Response 200**
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "device_name": "MacBook Touch ID",
      "aaguid": "adce0002-35bc-...",
      "created_at": "2026-03-01T00:00:00Z",
      "last_used_at": "2026-03-06T10:00:00Z"
    },
    {
      "id": "uuid",
      "device_name": "iPhone Face ID",
      "created_at": "2026-03-05T00:00:00Z",
      "last_used_at": "2026-03-06T09:00:00Z"
    }
  ]
}
```

---

## DELETE /auth/credentials/{id}

Remove a registered passkey.

**Note**: Không thể xóa passkey cuối cùng nếu Google OAuth chưa được liên kết (tránh lockout).

**Response 204** (no body)

**Errors**: `FORBIDDEN` (403) last credential và không có Google linked, `NOT_FOUND` (404)

---

## GET /auth/google

Google OAuth2 — phương thức đăng nhập thay thế (không phải WebAuthn).

Redirects to Google consent screen.

---

## GET /auth/google/callback

Google OAuth2 callback — tạo/link user, issue JWT.

**Response 200**: Same as WebAuthn login/complete response

---

## POST /auth/refresh

Refresh access token using refresh token.

**Request**
```json
{
  "refresh_token": "eyJ..."
}
```

**Response 200**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJ...",
    "expires_in": 900
  }
}
```

---

## DELETE /auth/logout

Invalidate refresh token (server-side blacklist).

**Headers**: `Authorization: Bearer <access_token>`

**Response 204** (no body)

---

# Chat Endpoint

## POST /chat

AI chat with RAG. Returns streaming SSE or JSON (based on `stream` param).

**Headers**
```
Authorization: Bearer <access_token>
Content-Type: application/json
Accept: text/event-stream   (if streaming)
```

**Request**
```json
{
  "message": "What is happening with ETH today?",
  "session_id": "uuid",
  "stream": true,
  "filters": {
    "symbols": ["ETH"],
    "since_hours": 24
  }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `message` | string | Yes | User query (max 1000 chars) |
| `session_id` | UUID | No | Continue existing session; omit to create new |
| `stream` | boolean | No | Default: true |
| `filters.symbols` | string[] | No | Filter retrieved news to these asset symbols |
| `filters.since_hours` | int | No | Limit retrieved news to last N hours (default: 24) |

**Streaming Response (SSE)**
```
Content-Type: text/event-stream
Cache-Control: no-cache

data: {"type": "session", "session_id": "uuid"}

data: {"type": "content", "delta": "ETH saw "}

data: {"type": "content", "delta": "significant selling pressure today..."}

data: {"type": "citations", "citations": [
  {
    "title": "Ethereum Falls 8% Amid...",
    "source": "coindesk",
    "source_url": "https://coindesk.com/...",
    "published_at": "2026-03-06T08:00:00Z",
    "sentiment_label": "negative"
  }
]}

data: {"type": "disclaimer", "text": "⚠️ This is not financial advice. Always DYOR."}

data: {"type": "done", "message_id": "uuid", "tokens_used": 312, "llm_model": "gpt-4o", "latency_ms": 1840}

data: [DONE]
```

**Non-streaming Response 200**
```json
{
  "success": true,
  "data": {
    "session_id": "uuid",
    "message_id": "uuid",
    "content": "ETH saw significant selling pressure today...",
    "citations": [
      {
        "title": "Ethereum Falls 8%...",
        "source": "coindesk",
        "source_url": "https://...",
        "published_at": "2026-03-06T08:00:00Z",
        "sentiment_label": "negative"
      }
    ],
    "disclaimer": "⚠️ This is not financial advice. Always DYOR.",
    "llm_model": "gpt-4o",
    "tokens_used": 312,
    "latency_ms": 1840
  }
}
```

**Errors**:
- `UNAUTHORIZED` (401) — missing token
- `CHAT_LIMIT_REACHED` (429) — free tier 10 queries/day exceeded
- `LLM_UNAVAILABLE` (503) — all LLMs failed

---

## GET /chat/history

List chat sessions for current user.

**Query Params**: `?page=1&limit=20`

**Response 200**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "uuid",
        "title": "What is happening with ETH today?",
        "created_at": "2026-03-06T10:00:00Z",
        "message_count": 4
      }
    ],
    "total": 10,
    "page": 1,
    "limit": 20
  }
}
```

---

## GET /chat/history/{session_id}

Get full message history for a session.

**Response 200**
```json
{
  "success": true,
  "data": {
    "session_id": "uuid",
    "messages": [
      {
        "id": "uuid",
        "role": "user",
        "content": "What is happening with ETH today?",
        "created_at": "2026-03-06T10:00:00Z"
      },
      {
        "id": "uuid",
        "role": "assistant",
        "content": "ETH saw significant...",
        "citations": [ ... ],
        "llm_model": "gpt-4o",
        "created_at": "2026-03-06T10:00:02Z"
      }
    ]
  }
}
```

---

# News Endpoints

## GET /news

Paginated news feed with optional filters.

**Query Params**

| Param | Type | Default | Description |
|---|---|---|---|
| `page` | int | 1 | Page number |
| `limit` | int | 20 | Items per page (max: 100) |
| `symbol` | string | — | Filter by asset symbol (BTC, ETH...) |
| `sentiment` | string | — | positive \| neutral \| negative |
| `risk_level` | string | — | low \| medium \| high \| critical |
| `source` | string | — | coindesk \| cointelegraph \| ... |
| `since` | ISO8601 | — | Articles published after this datetime |
| `until` | ISO8601 | — | Articles published before this datetime |

**Response 200**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "uuid",
        "title": "Bitcoin falls below key support...",
        "summary": "BTC dropped 5% in 4 hours...",
        "source": "coindesk",
        "source_url": "https://coindesk.com/...",
        "published_at": "2026-03-06T10:00:00Z",
        "asset_symbols": ["BTC"],
        "sentiment_score": -0.72,
        "sentiment_label": "negative",
        "risk_level": "high"
      }
    ],
    "total": 1482,
    "page": 1,
    "limit": 20,
    "data_freshness": "real-time"
  }
}
```

Note: Free tier users receive `"data_freshness": "delayed_1h"` — data is 1 hour old.

---

## GET /news/{id}

Get full article detail.

**Response 200**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "title": "...",
    "content": "...",
    "summary": "...",
    "source": "coindesk",
    "source_url": "https://...",
    "published_at": "...",
    "asset_symbols": ["BTC"],
    "sentiment_score": -0.72,
    "sentiment_label": "negative",
    "risk_level": "high"
  }
}
```

**Errors**: `NOT_FOUND` (404)

---

## GET /news/search

Semantic search across indexed articles.

**Query Params**: `?q=ethereum+merge&limit=10&since_hours=48`

**Response 200**: Same structure as `GET /news`

---

# Sentiment Endpoints

## GET /sentiment

Current market sentiment overview.

**Response 200**
```json
{
  "success": true,
  "data": {
    "market_sentiment_score": -0.18,
    "market_sentiment_label": "negative",
    "computed_at": "2026-03-06T10:00:00Z",
    "top_assets": [
      {
        "symbol": "BTC",
        "sentiment_score": -0.24,
        "sentiment_label": "negative",
        "article_count_24h": 142
      },
      {
        "symbol": "ETH",
        "sentiment_score": -0.31,
        "sentiment_label": "negative",
        "article_count_24h": 98
      }
    ],
    "data_freshness": "real-time"
  }
}
```

---

## GET /sentiment/timeline

Sentiment over time for charting.

**Query Params**: `?symbol=BTC&period=24h&interval=1h`

| Param | Options | Default |
|---|---|---|
| `symbol` | any asset symbol, or omit for market | market |
| `period` | 6h, 24h, 7d, 30d | 24h |
| `interval` | 15m, 1h, 4h, 1d | 1h |

**Response 200**
```json
{
  "success": true,
  "data": {
    "symbol": "BTC",
    "period": "24h",
    "interval": "1h",
    "points": [
      {
        "timestamp": "2026-03-05T10:00:00Z",
        "sentiment_score": 0.12,
        "article_count": 14
      },
      {
        "timestamp": "2026-03-05T11:00:00Z",
        "sentiment_score": -0.08,
        "article_count": 22
      }
    ]
  }
}
```

---

# Alert Endpoints

## POST /alerts/rules

Create an alert rule. **Requires Pro or Enterprise tier.**

**Request**
```json
{
  "name": "BTC bearish alert",
  "asset_symbols": ["BTC"],
  "condition_type": "sentiment_drop",
  "threshold": -0.4,
  "timeframe_min": 60,
  "channels": ["websocket", "telegram"]
}
```

| `condition_type` | Description |
|---|---|
| `sentiment_drop` | Sentiment falls below threshold in timeframe |
| `negative_surge` | >N articles with negative label in timeframe |
| `critical_risk` | Any article with risk_level = "critical" |
| `volume_spike` | Article volume > 3x baseline in timeframe |

**Response 201**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "BTC bearish alert",
    "is_active": true,
    "created_at": "2026-03-06T10:00:00Z"
  }
}
```

**Errors**:
- `TIER_RESTRICTED` (403) — channel "telegram" requires Pro+; includes `"upgrade_url": "/pricing"`
- `VALIDATION_ERROR` (422) — invalid condition_type or threshold out of range

---

## GET /alerts/rules

List all alert rules for current user.

**Response 200**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "uuid",
        "name": "BTC bearish alert",
        "asset_symbols": ["BTC"],
        "condition_type": "sentiment_drop",
        "threshold": -0.4,
        "timeframe_min": 60,
        "channels": ["websocket", "telegram"],
        "is_active": true,
        "trigger_count": 3,
        "last_triggered_at": "2026-03-05T14:30:00Z"
      }
    ],
    "total": 2
  }
}
```

---

## PATCH /alerts/rules/{id}

Toggle alert rule on/off.

**Request**
```json
{
  "is_active": false
}
```

**Response 200**: Updated rule object

---

## DELETE /alerts/rules/{id}

Delete an alert rule.

**Response 204** (no body)

**Errors**: `NOT_FOUND` (404), `FORBIDDEN` (403) if not owner

---

## GET /alerts/history

Recent alert events triggered for current user.

**Query Params**: `?page=1&limit=20&rule_id=uuid`

**Response 200**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "uuid",
        "rule_id": "uuid",
        "rule_name": "BTC bearish alert",
        "triggered_at": "2026-03-06T09:15:00Z",
        "payload": {
          "sentiment_score": -0.52,
          "trending_articles": ["uuid1", "uuid2"]
        },
        "delivered_channels": ["websocket", "telegram"]
      }
    ],
    "total": 8,
    "page": 1,
    "limit": 20
  }
}
```

---

# User Endpoints

## GET /users/me

Get current user profile.

**Response 200**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "email": "alex@example.com",
    "full_name": "Alex Nguyen",
    "role": "pro",
    "is_verified": true,
    "telegram_linked": true,
    "subscription_status": "active",
    "created_at": "2026-01-15T00:00:00Z"
  }
}
```

---

## PUT /users/me

Update user profile.

**Request**
```json
{
  "full_name": "Alex N.",
  "telegram_chat_id": 123456789
}
```

**Response 200**: Updated user object

---

## GET /users/subscription

Get current subscription details.

**Response 200**
```json
{
  "success": true,
  "data": {
    "tier": "pro",
    "status": "active",
    "current_period_start": "2026-03-01T00:00:00Z",
    "current_period_end": "2026-04-01T00:00:00Z",
    "cancel_at_period_end": false,
    "plan": {
      "name": "Pro",
      "price_monthly": 29.00,
      "currency": "USD"
    }
  }
}
```

---

# Billing Endpoints

## POST /billing/checkout

Create Stripe Checkout session. Redirects user to Stripe.

**Request**
```json
{
  "tier": "pro",
  "billing_cycle": "monthly",
  "success_url": "https://app.cryptolens.ai/dashboard?payment=success",
  "cancel_url": "https://app.cryptolens.ai/pricing"
}
```

**Response 200**
```json
{
  "success": true,
  "data": {
    "checkout_url": "https://checkout.stripe.com/pay/cs_...",
    "session_id": "cs_..."
  }
}
```

---

## POST /billing/portal

Create Stripe Customer Portal session (manage subscription, invoices).

**Response 200**
```json
{
  "success": true,
  "data": {
    "portal_url": "https://billing.stripe.com/session/..."
  }
}
```

---

# System Endpoints

## GET /health

Health check — no auth required.

**Response 200**
```json
{
  "status": "healthy",
  "version": "1.0",
  "timestamp": "2026-03-06T10:00:00Z",
  "services": {
    "database": "healthy",
    "qdrant": "healthy",
    "redis": "healthy",
    "llm_openai": "healthy",
    "llm_gemini": "healthy"
  }
}
```

---

## GET /metrics

Prometheus metrics endpoint. **No auth required** (restrict via network in prod).

Returns standard Prometheus exposition format for scraping.

---

# WebSocket

## WS /ws/alerts

Real-time alert push channel.

**Connection**: `ws://localhost:8000/ws/alerts?token=<access_token>`

**Server → Client message**
```json
{
  "type": "alert",
  "alert_id": "uuid",
  "rule_name": "BTC bearish alert",
  "triggered_at": "2026-03-06T09:15:00Z",
  "message": "BTC sentiment dropped to -0.52 in the last hour",
  "asset_symbols": ["BTC"],
  "severity": "high"
}
```

**Keepalive ping/pong**: Server sends `{"type": "ping"}` every 30s; client should respond `{"type": "pong"}`.

---

# Rate Limits

| Tier | Requests/min | Chat queries/day | Notes |
|---|---|---|---|
| Free | 60 | 10 | Data delayed 1h |
| Pro | 600 | Unlimited | Real-time data |
| Enterprise | Unlimited | Unlimited | Priority routing |

Rate limit headers in every response:
```
X-RateLimit-Limit: 600
X-RateLimit-Remaining: 597
X-RateLimit-Reset: 1709719260
```

When exceeded:
```
HTTP 429 Too Many Requests
Retry-After: 45
```

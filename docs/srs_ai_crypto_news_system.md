
# Software Requirement Specification (SRS)
## CRYPTOLENS-AI — AI Crypto News Analysis & Alert System

| Field | Value |
|---|---|
| Version | 2.0 |
| Date | March 2026 |
| Author | AI Engineer |
| Standard | Based on IEEE 830 |
| Status | Active |

---

# Table of Contents

1. [System Overview](#1-system-overview)
2. [Functional Requirements](#2-functional-requirements)
3. [Use Cases](#3-use-cases)
4. [Non-Functional Requirements](#4-non-functional-requirements)
5. [Data Models](#5-data-models)
6. [API Contract](#6-api-contract)
7. [Security Requirements](#7-security-requirements)
8. [Compliance Requirements](#8-compliance-requirements)
9. [Error Handling](#9-error-handling)
10. [Background Workers](#10-background-workers)
11. [Monitoring & Observability](#11-monitoring--observability)
12. [Deployment Requirements](#12-deployment-requirements)
13. [Backup & Recovery](#13-backup--recovery)
14. [Test Requirements](#14-test-requirements)
15. [Data Flow](#15-data-flow)

---

# 1. System Overview

CRYPTOLENS-AI là một nền tảng SaaS phân tích tin tức crypto theo thời gian thực, sử dụng **Agentic RAG** (LangGraph) và **Multi-LLM Routing** (GPT-4o, Gemini 2.0 Flash, Llama 3 / Mistral).

**Tech Stack** (tham chiếu Architecture Doc v2.0):

| Layer | Technology |
|---|---|
| Backend API | FastAPI (Python 3.12) |
| Agentic RAG | LangGraph + LangChain |
| LLMs | OpenAI GPT-4o/4.1, Google Gemini 2.0 Flash, Llama 3 (self-hosted) |
| Embedding | OpenAI text-embedding-3-small / nomic-embed-text |
| Vector DB | Qdrant |
| Relational DB | PostgreSQL 16 |
| Cache / Queue | Redis 7 |
| Workers | Celery + Celery Beat |
| Frontend | React 18 + Vite + TypeScript + Tailwind |
| Auth | WebAuthn / Passkeys (`py-webauthn`) + JWT session tokens |
| Billing | Stripe |
| Observability | OpenTelemetry + Prometheus + Grafana + LangSmith |
| Deployment | Docker + Vercel (FE) + Railway/AWS (BE) |

---

# 2. Functional Requirements

## 2.1 News Ingestion

| ID | Requirement | Priority |
|---|---|---|
| FR-001 | Hệ thống phải thu thập tin tức tự động từ CoinDesk, CoinTelegraph, CryptoPanic, Messari, The Block, Decrypt mỗi 15 phút | Must Have |
| FR-002 | Hệ thống phải hỗ trợ thu thập sentiment từ X/Twitter API v2 và Reddit API | Should Have |
| FR-003 | Hệ thống phải loại bỏ duplicate bài viết dựa trên content hash (MD5) trước khi lưu | Must Have |
| FR-004 | Hệ thống phải chuẩn hóa dữ liệu tin tức về schema Article thống nhất (FR-001 Article Model) | Must Have |
| FR-005 | Mỗi bài viết phải được gắn tag asset_symbols (BTC, ETH...) thông qua NER hoặc keyword matching | Should Have |
| FR-006 | Hệ thống phải lưu raw article vào PostgreSQL trước khi bắt đầu xử lý embedding | Must Have |

## 2.2 Text Processing & Embedding

| ID | Requirement | Priority |
|---|---|---|
| FR-007 | Hệ thống phải chia bài viết thành chunks (chunk_size=500 tokens, overlap=50 tokens) | Must Have |
| FR-008 | Hệ thống phải tạo vector embedding cho từng chunk sử dụng `text-embedding-3-small` (primary) | Must Have |
| FR-009 | Hệ thống phải fallback sang `nomic-embed-text` nếu OpenAI API không khả dụng | Should Have |
| FR-010 | Embedding vector và metadata phải được lưu vào Qdrant trong collection `crypto_news_articles` | Must Have |
| FR-011 | Mỗi Qdrant point phải chứa payload: article_id, source, published_at, asset_symbols, sentiment_label, chunk_index, chunk_text | Must Have |

## 2.3 Sentiment Analysis

| ID | Requirement | Priority |
|---|---|---|
| FR-012 | Hệ thống phải tính sentiment_score (float -1.0 đến 1.0) cho mỗi bài viết | Must Have |
| FR-013 | Hệ thống phải gán sentiment_label: "positive" | "neutral" | "negative" | Must Have |
| FR-014 | Hệ thống phải tính risk_level: "low" | "medium" | "high" | "critical" | Must Have |
| FR-015 | Sentiment phải được tính bằng LLM (GPT-4o / Gemini 2.0 Flash) với structured output (JSON mode) | Must Have |
| FR-016 | Market sentiment tổng hợp (aggregate) phải được tính mỗi 1 giờ và cache vào Redis | Must Have |

## 2.4 RAG Chat Interface

| ID | Requirement | Priority |
|---|---|---|
| FR-017 | Hệ thống phải cung cấp chat endpoint `POST /api/v1/chat` với streaming response (SSE) | Must Have |
| FR-018 | Mỗi response phải kèm source citations (title, source, url, published_at) cho các tài liệu đã sử dụng | Must Have |
| FR-019 | RAG retrieval phải sử dụng hybrid search: vector similarity (Qdrant) + keyword search (BM25) | Must Have |
| FR-020 | Kết quả retrieval phải được rerank bằng CrossEncoder trước khi đưa vào LLM context | Should Have |
| FR-021 | LLM Router phải chọn model phù hợp dựa trên query complexity và user tier | Must Have |
| FR-022 | Hệ thống phải lưu conversation history vào PostgreSQL (bảng chat_sessions, chat_messages) | Must Have |
| FR-023 | Chat history phải bị xóa sau 30 ngày với Free tier, 1 năm với Pro/Enterprise (data retention) | Should Have |
| FR-024 | Response phải bao gồm financial disclaimer: "Not financial advice." | Must Have |

## 2.5 Sentiment Dashboard

| ID | Requirement | Priority |
|---|---|---|
| FR-025 | Dashboard phải hiển thị sentiment score tổng hợp theo thời gian (timeline chart) | Must Have |
| FR-026 | Dashboard phải hiển thị top 10 assets được nhắc đến nhiều nhất trong 24h | Must Have |
| FR-027 | Dashboard phải hiển thị trending news feed với sentiment badge (màu sắc theo label) | Must Have |
| FR-028 | Free tier nhận dữ liệu delay 1 giờ; Pro/Enterprise nhận real-time | Must Have |

## 2.6 Alert System

| ID | Requirement | Priority |
|---|---|---|
| FR-029 | Người dùng Pro/Enterprise phải có thể tạo alert rules với điều kiện: asset + sentiment threshold + timeframe | Must Have |
| FR-030 | Alert phải được deliver qua WebSocket (in-app) cho tất cả user tiers | Must Have |
| FR-031 | Alert phải được deliver qua Telegram bot cho Pro/Enterprise tier | Must Have |
| FR-032 | Alert phải được deliver qua Email cho Pro/Enterprise tier | Must Have |
| FR-033 | Enterprise tier phải hỗ trợ Webhook alert (custom URL) | Should Have |
| FR-034 | Alert history phải được lưu và hiển thị trong giao diện | Must Have |

## 2.7 Authentication & User Management (WebAuthn)

| ID | Requirement | Priority |
|---|---|---|
| FR-035 | Hệ thống phải xác thực người dùng bằng **WebAuthn / Passkeys** (W3C standard) — không lưu password | Must Have |
| FR-036 | **Registration flow**: `POST /auth/webauthn/register/begin` → server tạo random challenge (32 bytes) + `PublicKeyCredentialCreationOptions` → trình duyệt gọi `navigator.credentials.create()` → `POST /auth/webauthn/register/complete` xác minh và lưu public key → issue JWT | Must Have |
| FR-037 | **Authentication flow**: `POST /auth/webauthn/login/begin` → server tạo challenge + `PublicKeyCredentialRequestOptions` → trình duyệt gọi `navigator.credentials.get()` → `POST /auth/webauthn/login/complete` verify chữ ký → issue JWT | Must Have |
| FR-038 | WebAuthn challenge phải là cryptographically random (≥32 bytes), lưu trong Redis với TTL 5 phút, single-use (xóa ngay sau verify) | Must Have |
| FR-039 | `sign_count` của mỗi credential phải được kiểm tra sau mỗi lần authenticate — nếu server count > authenticator count thì reject (clone detection) | Must Have |
| FR-040-A | Hệ thống phải issue JWT access token (TTL: 15 phút) và refresh token (TTL: 7 ngày) sau khi WebAuthn xác minh thành công | Must Have |
| FR-040-B | User phải có thể quản lý passkeys: list (`GET /auth/credentials`), đặt device name (`PATCH`), xóa (`DELETE /auth/credentials/{id}`) | Should Have |
| FR-040-C | Hệ thống phải hỗ trợ Google OAuth2 như một phương thức đăng nhập **thay thế** cho users không có passkey-capable device | Should Have |
| FR-041-A | Mỗi user phải có role: free \| pro \| enterprise \| admin | Must Have |
| FR-041-B | Rate limiting phải được áp dụng theo tier: Free (60 req/min), Pro (600 req/min), Enterprise (unlimited) | Must Have |

## 2.8 Billing & Subscription (Stripe)

| ID | Requirement | Priority |
|---|---|---|
| FR-040 | Hệ thống phải tích hợp Stripe để quản lý subscription | Must Have |
| FR-041 | Stripe Webhook phải xử lý sự kiện: payment_succeeded, payment_failed, subscription_canceled | Must Have |
| FR-042 | User role phải được cập nhật tự động sau khi thanh toán thành công | Must Have |
| FR-043 | Khi subscription hết hạn, user phải tự động downgrade về Free tier | Must Have |

## 2.9 RAG Evaluation

| ID | Requirement | Priority |
|---|---|---|
| FR-044 | Hệ thống phải chạy RAGAS evaluation tự động mỗi 6 giờ trên sample queries | Should Have |
| FR-045 | RAGAS metrics (Faithfulness, Answer Relevancy, Context Recall, Context Precision) phải được lưu vào PostgreSQL | Should Have |
| FR-046 | Tất cả LLM interactions phải được trace và gửi đến LangSmith | Should Have |

---

# 3. Use Cases

## UC-001: User Queries Market Sentiment via Chat

| Field | Value |
|---|---|
| Actor | Authenticated User (Pro tier) |
| Precondition | User đã login; hệ thống đã index bài viết trong vòng 24h |
| Trigger | User gửi câu hỏi: "What is happening with ETH today?" |
| Main Flow | 1. Frontend gửi POST /api/v1/chat với message<br>2. LangGraph agent planner xác định cần hybrid search ETH news 24h<br>3. Qdrant trả về top-20 chunks liên quan<br>4. CrossEncoder reranker chọn top-5<br>5. LLM Router chọn Gemini 2.0 Flash (Pro tier, standard query)<br>6. LLM tạo response với source citations<br>7. Response streamed về frontend qua SSE<br>8. Conversation lưu vào PostgreSQL |
| Postcondition | Response có citations, financial disclaimer, latency < 3s |
| Exceptions | Nếu Qdrant unavailable → trả lỗi 503 với retry-after header |

## UC-002: Alert Triggered on Negative Sentiment

| Field | Value |
|---|---|
| Actor | System (alert_worker) |
| Precondition | User có alert rule: BTC, sentiment < -0.4, timeframe 1h |
| Trigger | Sentiment score BTC giảm từ 0.2 xuống -0.5 trong 1h |
| Main Flow | 1. alert_worker chạy mỗi 5 phút, evaluate tất cả active rules<br>2. Rule của user match<br>3. alert_worker tạo Alert record trong PostgreSQL<br>4. WebSocket push to user's active connections<br>5. Celery task gửi Telegram message (nếu user có Telegram linked)<br>6. Celery task gửi Email (nếu user enable email alerts) |
| Postcondition | User nhận alert trong < 5 phút sau khi rule match |

## UC-003: Free User Tries Pro Feature

| Field | Value |
|---|---|
| Actor | Free tier user |
| Precondition | User đã login với role = "free" |
| Trigger | User cố tạo Telegram alert |
| Main Flow | 1. POST /api/v1/alerts/rules với channel = "telegram"<br>2. Backend middleware kiểm tra user.role<br>3. Role = "free" → trả 403 Forbidden |
| Postcondition | Response: {"error": {"code": "TIER_RESTRICTED", "message": "Telegram alerts require Pro or Enterprise plan.", "upgrade_url": "/pricing"}} |

---

# 4. Non-Functional Requirements

## 4.1 Performance

| Requirement | Target |
|---|---|
| Chat response latency (P95) | < 3 seconds |
| API response latency (non-LLM) | < 200ms |
| News ingestion delay (publish → vector store) | < 15 minutes |
| Alert delivery delay (trigger → user) | < 5 minutes |
| Dashboard load time | < 1 second |

## 4.2 Availability & Reliability

| Requirement | Target |
|---|---|
| System uptime | 99.5% monthly |
| Max planned downtime | 30 min/month |
| Celery worker auto-restart | On crash (supervisor / Docker restart policy) |
| API health check | GET /api/v1/health responds 200 within 500ms |

## 4.3 Scalability

| Requirement | Detail |
|---|---|
| Backend | Horizontally scalable (stateless FastAPI instances) |
| Workers | Celery concurrency configurable per worker type |
| Vector DB | Qdrant supports distributed multi-node deployment |
| Database | PostgreSQL with read replicas on traffic increase |

## 4.4 Security

→ Xem [Mục 7. Security Requirements](#7-security-requirements) và [Architecture Doc mục 10](architecture_ai_crypto_news_system.md#10-security-architecture)

## 4.5 Maintainability

| Requirement | Detail |
|---|---|
| Code coverage | > 80% unit test coverage |
| Type safety | Full Python type hints via Pydantic |
| API versioning | /api/v1/ — backward compatible until officially deprecated |
| Environment config | All secrets via env vars, không hardcode |

---

# 5. Data Models

## 5.1 User

```sql
CREATE TABLE users (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email       VARCHAR(255) UNIQUE NOT NULL,
    -- NO password_hash: authentication via WebAuthn only (+ Google OAuth as alternative)
    full_name   VARCHAR(255),
    role        VARCHAR(20) NOT NULL DEFAULT 'free',  -- free|pro|enterprise|admin
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    telegram_chat_id BIGINT,
    stripe_customer_id VARCHAR(255),
    stripe_subscription_id VARCHAR(255),
    subscription_status VARCHAR(20),     -- active|past_due|canceled|trialing
    google_sub  VARCHAR(255),            -- Google OAuth subject ID (if linked)
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- WebAuthn credentials (one user can have multiple passkeys: phone, laptop, YubiKey)
CREATE TABLE webauthn_credentials (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    credential_id   TEXT NOT NULL UNIQUE,   -- base64url encoded credential ID
    public_key      BYTEA NOT NULL,         -- CBOR encoded public key
    sign_count      INTEGER NOT NULL DEFAULT 0,  -- replay attack detection
    device_name     VARCHAR(255),           -- user-assigned label, e.g. "MacBook Touch ID"
    aaguid          TEXT,                   -- authenticator model identifier (GUID)
    attestation     TEXT,                   -- none | indirect | direct | enterprise
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_used_at    TIMESTAMPTZ
);
CREATE INDEX idx_webauthn_credentials_user_id ON webauthn_credentials(user_id);
```

## 5.2 Article

```sql
CREATE TABLE articles (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title           TEXT NOT NULL,
    content         TEXT NOT NULL,
    summary         TEXT,
    source          VARCHAR(50) NOT NULL,      -- coindesk|cointelegraph|...
    source_url      TEXT NOT NULL UNIQUE,
    published_at    TIMESTAMPTZ NOT NULL,
    crawled_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    asset_symbols   TEXT[],                    -- ['BTC', 'ETH']
    sentiment_score FLOAT,                     -- -1.0 to 1.0
    sentiment_label VARCHAR(20),               -- positive|neutral|negative
    risk_level      VARCHAR(20),               -- low|medium|high|critical
    content_hash    VARCHAR(64) NOT NULL,      -- MD5 for dedup
    is_duplicate    BOOLEAN NOT NULL DEFAULT FALSE,
    embedding_id    VARCHAR(255),              -- Qdrant point ID
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_articles_published_at ON articles(published_at DESC);
CREATE INDEX idx_articles_asset_symbols ON articles USING GIN(asset_symbols);
CREATE INDEX idx_articles_sentiment_label ON articles(sentiment_label);
```

## 5.3 Chat Session & Messages

```sql
CREATE TABLE chat_sessions (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id    UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title      VARCHAR(255),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE chat_messages (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id    UUID NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role          VARCHAR(20) NOT NULL,  -- user|assistant|system
    content       TEXT NOT NULL,
    citations     JSONB,                 -- [{title, source, url, published_at}]
    llm_model     VARCHAR(50),           -- gpt-4o|gemini-2.0-flash|llama-3
    tokens_used   INTEGER,
    latency_ms    INTEGER,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

## 5.4 Alert Rule & Alert Event

```sql
CREATE TABLE alert_rules (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name            VARCHAR(255) NOT NULL,
    asset_symbols   TEXT[],
    condition_type  VARCHAR(50) NOT NULL,  -- sentiment_drop|negative_surge|...
    threshold       FLOAT NOT NULL,
    timeframe_min   INTEGER NOT NULL,      -- in minutes
    channels        TEXT[],               -- ['websocket', 'telegram', 'email']
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE alert_events (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rule_id      UUID NOT NULL REFERENCES alert_rules(id) ON DELETE CASCADE,
    user_id      UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    triggered_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    payload      JSONB NOT NULL,           -- snapshot of conditions that fired
    delivered_channels TEXT[]             -- which channels were successfully delivered
);
```

## 5.5 RAG Evaluation

```sql
CREATE TABLE rag_evaluations (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evaluated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    query           TEXT NOT NULL,
    faithfulness    FLOAT,
    answer_relevancy FLOAT,
    context_recall  FLOAT,
    context_precision FLOAT,
    latency_ms      INTEGER,
    llm_model       VARCHAR(50)
);
```

---

# 6. API Contract

Full OpenAPI spec: [docs/api_spec.md](api_spec.md)

## 6.1 Chat Endpoint

**Request**
```http
POST /api/v1/chat
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "message": "What is happening with ETH today?",
  "session_id": "uuid",        // optional — creates new session if omitted
  "stream": true               // SSE streaming response
}
```

**Response (streaming)**
```
Content-Type: text/event-stream

data: {"type": "content", "delta": "ETH saw..."}
data: {"type": "content", "delta": " significant..."}
data: {"type": "citations", "citations": [{"title": "...", "source": "coindesk", "url": "..."}]}
data: {"type": "done", "session_id": "uuid", "message_id": "uuid", "tokens_used": 312}
data: [DONE]
```

## 6.2 News Feed Endpoint

**Request**
```http
GET /api/v1/news?page=1&limit=20&symbol=BTC&sentiment=negative&since=2026-03-05T00:00:00Z
Authorization: Bearer <access_token>
```

**Response**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "uuid",
        "title": "Bitcoin falls below key support...",
        "summary": "BTC dropped...",
        "source": "coindesk",
        "source_url": "https://...",
        "published_at": "2026-03-06T10:00:00Z",
        "asset_symbols": ["BTC"],
        "sentiment_score": -0.72,
        "sentiment_label": "negative",
        "risk_level": "high"
      }
    ],
    "total": 142,
    "page": 1,
    "limit": 20
  }
}
```

## 6.3 Error Codes

| Code | HTTP Status | Description |
|---|---|---|
| `UNAUTHORIZED` | 401 | Missing or invalid JWT token |
| `FORBIDDEN` | 403 | Action not allowed for current user role |
| `TIER_RESTRICTED` | 403 | Feature requires higher subscription tier |
| `NOT_FOUND` | 404 | Resource does not exist |
| `VALIDATION_ERROR` | 422 | Request body/params fail Pydantic validation |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests for current tier |
| `LLM_UNAVAILABLE` | 503 | All LLM providers failed or rate limited |
| `VECTOR_DB_ERROR` | 503 | Qdrant connection failure |
| `INTERNAL_ERROR` | 500 | Unexpected server error |

---

# 7. Security Requirements

| ID | Requirement |
|---|---|
| SR-001 | Tất cả secrets (API keys, JWT secret, WebAuthn RP config) phải được lưu trong environment variables, không commit vào git |
| SR-002 | **Không lưu password** — xác thực hoàn toàn qua WebAuthn public-key cryptography; private key không bao giờ rời khỏi thiết bị của user |
| SR-002-B | WebAuthn challenge: cryptographically random ≥32 bytes; single-use; TTL 5 phút trong Redis; xóa ngay sau verify thành công hoặc hết hạn |
| SR-002-C | `sign_count` phải tăng sau mỗi lần authenticate; nếu server_count > authenticator_count → reject credential + alert user (possible passkey clone) |
| SR-002-D | `rpId` (Relying Party ID) phải khớp với production domain (`cryptolens.ai`); trong dev dùng `localhost` |
| SR-003 | JWT access token TTL: 15 phút; refresh token TTL: 7 ngày |
| SR-004 | Rate limiting phải được áp dụng tại API gateway sử dụng Redis token bucket |
| SR-005 | Tất cả input của user phải được validate bằng Pydantic strict models trước khi xử lý |
| SR-006 | LLM prompt injection phải được detect và block (guardrails layer trong LangGraph) |
| SR-007 | CORS phải chỉ allow origins từ whitelist (không dùng *) |
| SR-008 | Tất cả API calls đến LLM providers phải đi qua backend — không expose API keys ra frontend |
| SR-009 | SQL queries phải sử dụng SQLAlchemy ORM parameterized queries — không dùng raw SQL string formatting |
| SR-010 | Dependencies phải được scan bằng `pip-audit` trong CI pipeline |
| SR-011 | Sensitive endpoints (auth, billing) phải log tất cả access với IP, user_agent, timestamp |

---

# 8. Compliance Requirements

## 8.1 GDPR (EU Users)

| Requirement | Implementation |
|---|---|
| Right to deletion | API endpoint để delete toàn bộ user data (account, chat history, alert rules) |
| Data portability | Export endpoint trả về JSON của tất cả user data |
| Consent tracking | Log explicit consent khi đăng ký |
| Data minimization | Không lưu dữ liệu không cần thiết |
| Privacy policy | Link bắt buộc trong signup flow |

## 8.2 Financial Disclaimer

| Requirement | Implementation |
|---|---|
| FR-024 compliant | Mọi AI response phải kèm: "This is not financial advice. Always do your own research." |
| UI disclaimer | Hiển thị cố định trong Chat UI và Dashboard |
| Terms of Service | User phải accept ToS trước khi sử dụng |

## 8.3 Content Copyright

| Requirement | Implementation |
|---|---|
| Article attribution | Luôn hiển thị source name và link đến bài gốc |
| Content summarization | Chỉ lưu summary + metadata, không reproduce full article nếu vi phạm ToS của source |
| Robots.txt compliance | Crawler phải check robots.txt của từng domain |

---

# 9. Error Handling

## 9.1 LLM Failure Strategy

```
Primary LLM fails
      ↓
Retry 1x với same LLM (exponential backoff 1s)
      ↓
Fallback to Secondary LLM (GPT-4o → Gemini 2.0 Flash)
      ↓
Fallback to Tertiary LLM (Gemini → Llama 3 self-hosted)
      ↓
Return 503 với retry-after header
```

## 9.2 Qdrant Failure Strategy

```
Qdrant unavailable
      ↓
Return cached results từ Redis (TTL: 10 min)
     OR
Return 503 với informative error message
```

## 9.3 Celery Worker Failure

- Workers phải có `max_retries=3` với exponential backoff
- Failed tasks phải được đưa vào Dead Letter Queue
- DLQ phải được monitored và alert admin qua Telegram

---

# 10. Background Workers

| Worker | Queue | Concurrency | Schedule | Retry |
|---|---|---|---|---|
| news_crawler | news_crawler | 4 | Every 15 min | 3x, 60s backoff |
| embedding_worker | embedding_worker | 2 | Every 5 min | 3x, 30s backoff |
| sentiment_worker | sentiment_worker | 4 | Every 1 hour | 3x, 30s backoff |
| alert_worker | alert_worker | 2 | Every 5 min | 2x, 10s backoff |
| evaluation_worker | evaluation_worker | 1 | Every 6 hours | 1x |

---

# 11. Monitoring & Observability

| Metric | Tool | Alert Threshold |
|---|---|---|
| API latency P95 | Prometheus + Grafana | > 3s → alert |
| LLM token cost/hour | LangSmith | > $10/hour → alert |
| News ingestion delay | Custom metric | > 30 min → alert |
| Celery queue depth | Prometheus | > 1000 tasks → alert |
| Error rate | Prometheus | > 1% → alert |
| Qdrant indexing latency | Prometheus | > 5s → alert |
| RAG faithfulness score | PostgreSQL + Grafana | < 0.75 → alert |

---

# 12. Deployment Requirements

| Requirement | Detail |
|---|---|
| Containerization | Tất cả services phải chạy trong Docker containers |
| Environment parity | dev / staging / production sử dụng cùng Docker images |
| CI/CD | GitHub Actions: test → build → deploy on merge to main |
| Zero-downtime deploy | Blue-green deployment hoặc rolling update |
| Secrets | Never in Docker images; inject via environment variables |
| Frontend | Deploy to Vercel với automatic preview deployments |

---

# 13. Backup & Recovery

| Component | Backup Strategy | RPO | RTO |
|---|---|---|---|
| PostgreSQL | Automated daily backup + WAL streaming | 1 hour | 1 hour |
| Qdrant | Snapshot API — daily snapshot to object storage | 24 hours | 2 hours |
| Redis | RDB snapshot every 1 hour | 1 hour | 30 min |
| Code | Git (GitHub) | 0 (on commit) | 15 min |

**Recovery Procedure**: Documented trong `docs/runbooks/disaster-recovery.md`

---

# 14. Test Requirements

## 14.1 Unit Tests

- Coverage target: > 80%
- Tools: pytest + pytest-asyncio
- Mock: LLM calls, Qdrant queries, external API calls
- Location: `backend/tests/unit/`

## 14.2 Integration Tests

- Test real database interactions (PostgreSQL + Redis)
- Test Celery tasks với TestCase workers
- Location: `backend/tests/integration/`

## 14.3 End-to-End Tests

- Test critical user flows: register → login → chat → receive alert
- Tools: Playwright (frontend) + httpx (API)
- Run in CI on staging environment

## 14.4 Load Tests

- Tool: Locust
- Target: 100 concurrent users, chat endpoint < 5s latency
- Run monthly trước major releases

## 14.5 Security Tests

- `pip-audit` trong CI pipeline (FR per SR-010)
- OWASP ZAP scan trên staging trước production release
- Manual penetration test trước public launch

---

# 15. Data Flow

```
[External Source] —RSS/API—→ [Celery: news_crawler]
                                      ↓
                              [Dedup: Redis hash check]
                                      ↓
                             [Pydantic normalize → Article]
                                      ↓
                              [PostgreSQL: articles table]
                                      ↓
                         [Celery: embedding_worker triggered]
                                      ↓
                          [Text Chunker (chunk_size=500)]
                                      ↓
                    [Embedding: text-embedding-3-small / nomic]
                                      ↓
                   [Qdrant: upsert point with payload metadata]
                                      ↓
                       [Celery: sentiment_worker (scheduled)]
                                      ↓
                  [LLM: structured output → score + label + risk]
                                      ↓
                       [PostgreSQL: update article sentiment]
                                      ↓
                    [Celery: alert_worker evaluates active rules]
                                      ↓
                    [PostgreSQL: create alert_event if triggered]
                                      ↓
            [WebSocket / Telegram / Email delivery per rule config]

[User] —query—→ [FastAPI POST /api/v1/chat]
                        ↓
              [LangGraph: Query Planner Node]
                        ↓
            [Qdrant: hybrid search top-20 chunks]
                        ↓
            [CrossEncoder: rerank → top-5 contexts]
                        ↓
              [LangGraph: LLM Router Node]
                        ↓
         [GPT-4o | Gemini 2.0 Flash | Llama 3]
                        ↓
           [Structured Output: response + citations]
                        ↓
           [SSE Stream → React Frontend]
                        ↓
           [PostgreSQL: save chat_messages]
                        ↓
           [LangSmith: trace LLM interaction]
                        ↓
           [RAGAS: async eval sample]
```

# 11. Future Scalability

Possible upgrades:

- Pinecone vector database
- Kubernetes deployment
- streaming ingestion pipelines
- distributed worker clusters



# 🚀 AI Engineer Roadmap (Pro Version)
## CRYPTOLENS-AI — Real-Time Market Sentiment RAG System
Duration: **91 Days (13 Weeks)**

Roadmap này được thiết kế để follow trực tiếp trong **VS Code**.  
Dùng checkboxes để track progress.

---

# 🧠 System Architecture

```mermaid
flowchart LR
    A[News Sources RSS/API/Social] --> B[Celery Crawler Workers]
    B --> C[Text Chunking]
    C --> D[Embeddings — text-embedding-3-small]
    D --> E[Qdrant Vector DB]
    E --> F[LangGraph Agentic RAG]
    F --> G[Multi-LLM Router\nGPT-4o | Gemini | Llama 3]
    G --> H[FastAPI Backend /api/v1/]
    H --> I[React + Vite Dashboard]
    H --> J[Telegram / Email Alerts]
    F --> K[RAGAS Evaluation]
    H --> L[OpenTelemetry + Prometheus]
```

---

# 📁 Project Structure

```
CRYPTOLENS-AI/
│
├── backend/
│   ├── app/
│   │   ├── api/v1/          ← FastAPI routers
│   │   ├── services/        ← Business logic
│   │   ├── models/          ← SQLAlchemy models
│   │   ├── schemas/         ← Pydantic schemas
│   │   ├── core/            ← Config, security, deps
│   │   └── main.py
│   ├── workers/             ← Celery tasks
│   ├── rag/                 ← LangGraph agents
│   ├── embeddings/          ← Embedding service
│   ├── evaluation/          ← RAGAS eval
│   └── tests/
│
├── frontend/                ← React + Vite + Tailwind
├── docs/                    ← SRS, PRD, Architecture, ADRs
├── docker-compose.yml
└── .env.example
```

---

# WEEK 1 — Foundation & Environment

- [ ] **Day 1 — Project Setup**
  - Setup Python 3.12 virtual environment
  - Install: fastapi, uvicorn, pydantic, python-dotenv
  - Init Git repository với `.gitignore` chuẩn
  - Tạo `.env.example` với tất cả required env vars

- [ ] **Day 2 — Async Python**
  - Learn: `async/await`, `asyncio`, `httpx`
  - Viết async HTTP client để test RSS feed fetch
  - Project: `GET /health` endpoint chạy được

- [ ] **Day 3 — RSS & API Integration**
  - Kết nối CoinDesk RSS feed với `feedparser`
  - Kết nối CoinTelegraph RSS
  - LeetCode: Two Sum (warm-up)

- [ ] **Day 4 — Pydantic Data Models**
  - Xây dựng `Article` Pydantic schema (title, content, source, published_at, asset_symbols)
  - Normalize RSS data về Article schema
  - Learn: Pydantic v2 validators, model_config

- [ ] **Day 5 — PostgreSQL Setup**
  - Setup PostgreSQL với Docker
  - Install SQLAlchemy async + asyncpg
  - Tạo `articles` table migration (Alembic)
  - LeetCode: Contains Duplicate

- [ ] **Day 6 — Celery Background Workers**
  - Setup Redis + Celery
  - Tạo `news_crawler` Celery task
  - Test: crawl → normalize → save to PostgreSQL
  - Learn: Celery Beat scheduling

- [ ] **Day 7 — Review & Test**
  - End-to-end test: crawler chạy, articles vào DB
  - Code review & refactor theo clean architecture

---

# WEEK 2 — Vector Database (Qdrant)

- [ ] **Day 8 — Text Chunking**
  - Learn: text splitting strategies (recursive, token-based)
  - Implement `TextChunker` với `chunk_size=500, overlap=50`
  - LeetCode: Best Time to Buy/Sell Stock

- [ ] **Day 9 — OpenAI Embeddings**
  - Setup OpenAI client
  - Implement `EmbeddingService` với `text-embedding-3-small`
  - Implement fallback sang `nomic-embed-text` (Ollama)
  - Learn: batched embedding calls để giảm API cost

- [ ] **Day 10 — Qdrant Setup**
  - Setup Qdrant trong Docker (self-hosted)
  - Tạo collection `crypto_news_articles` với đúng schema
  - LeetCode: Valid Palindrome

- [ ] **Day 11 — Embedding Pipeline**
  - Build full pipeline: article → chunks → embeddings → Qdrant upsert
  - Implement payload metadata: source, published_at, asset_symbols, chunk_index
  - Celery: `embedding_worker` task

- [ ] **Day 12 — Deduplication**
  - Implement content hash (MD5) deduplication
  - Redis hash set để rapid dedup check
  - Test: chạy crawler 2 lần → không có duplicate vectors

- [ ] **Day 13 — CryptoPanic API**
  - Kết nối CryptoPanic REST API
  - Chuẩn hóa data về Article schema
  - Test full ingestion pipeline với 3 sources

- [ ] **Day 14 — Ingestion Pipeline Review**
  - Load test: crawl 200 articles → embed → store
  - Monitor: latency, Qdrant size, error rate
  - Fix bottlenecks

---

# WEEK 3 — Retrieval & Hybrid Search

- [ ] **Day 15 — Basic Vector Search**
  - Implement basic semantic search với Qdrant
  - `POST /api/v1/news/search?q=...` endpoint
  - LeetCode: Reverse Linked List

- [ ] **Day 16 — Metadata Filtering**
  - Implement Qdrant payload filters: by asset_symbol, published_at range, sentiment_label
  - Test: "ETH news in last 24h" query

- [ ] **Day 17 — Hybrid Search (BM25 + Vector)**
  - Implement BM25 keyword search (rank_bm25 library)
  - Combine vector + keyword scores (Reciprocal Rank Fusion)
  - LeetCode: Valid Parentheses

- [ ] **Day 18 — CrossEncoder Reranker**
  - Install `sentence-transformers` CrossEncoder
  - Implement reranker: vector search top-20 → rerank → top-5
  - Learn: why reranking matters for RAG quality

- [ ] **Day 19 — Query Expansion**
  - Implement multi-query expander: "BTC" → ["Bitcoin", "BTC price", "Bitcoin news"]
  - Test quality improvement vs single query

- [ ] **Day 20 — Retrieval Evaluation**
  - Build basic retrieval test set (10 queries + expected docs)
  - Measure: Precision@5, Recall@5 before/after reranking

- [ ] **Day 21 — Retrieval Optimization**
  - Tune chunk_size, overlap, top_k
  - Document optimal settings
  - LeetCode: Merge Intervals

---

# WEEK 4 — LangGraph Agentic RAG

- [ ] **Day 22 — LangGraph Introduction**
  - Learn: LangGraph StateGraph, nodes, edges, conditional routing
  - Build minimal graph: Query → Search → Generate
  - LeetCode: Climbing Stairs

- [ ] **Day 23 — RAG Agent Nodes**
  - Implement `QueryPlannerNode`: xác định type of query (asset-specific, market-wide, etc.)
  - Implement `HybridRetrieverNode`: calls Qdrant hybrid search
  - Implement `ContextBuilderNode`: format retrieved chunks + metadata

- [ ] **Day 24 — Multi-LLM Router**
  - Implement `LLMRouterNode`: route based on query complexity + user tier
  - GPT-4o: complex multi-hop queries, Enterprise/Pro priority
  - Gemini 2.0 Flash: standard queries, free tier
  - Llama 3 (Ollama): self-hosted fallback

- [ ] **Day 25 — Prompt Engineering**
  - Design system prompt cho crypto news analysis
  - Include: role, context format, citation format, financial disclaimer
  - Test: 20 manual queries, evaluate response quality

- [ ] **Day 26 — Streaming Response (SSE)**
  - Implement SSE streaming trong FastAPI `POST /api/v1/chat`
  - Stream: content chunks → citations → done event
  - Frontend test với curl

- [ ] **Day 27 — Conversation Memory**
  - Implement conversation history retrieval từ PostgreSQL
  - Include last N messages trong LangGraph state
  - Test: multi-turn conversation ("Tell me more about ETH" → references previous message)

- [ ] **Day 28 — Guardrails & Safety**
  - Implement prompt injection detection (guardrails layer)
  - Block queries về illegal activity, financial advice requests
  - Ensure financial disclaimer appended to every crypto-related response

---

# WEEK 5 — Sentiment Analysis & Alert System

- [ ] **Day 29 — Sentiment Analysis Worker**
  - Implement `sentiment_worker` Celery task
  - LLM structured output (JSON mode): sentiment_score, sentiment_label, risk_level
  - Update article record trong PostgreSQL sau khi scored

- [ ] **Day 30 — Market Sentiment Aggregation**
  - Compute aggregate market sentiment (weighted avg by recency)
  - Compute per-asset sentiment
  - Cache results trong Redis (TTL 1h)
  - `GET /api/v1/sentiment` endpoint

- [ ] **Day 31 — Sentiment Timeline**
  - `GET /api/v1/sentiment/timeline?symbol=BTC&period=24h`
  - Trả về time-series data cho frontend chart
  - LeetCode: Product of Array Except Self

- [ ] **Day 32 — Alert Rule Engine**
  - Design `alert_rules` + `alert_events` tables (SRS 5.4 schema)
  - Implement `alert_worker`: evaluate rules mỗi 5 phút
  - Conditions: sentiment_drop, negative_surge, critical_risk

- [ ] **Day 33 — WebSocket Alerts**
  - Implement WebSocket endpoint `/ws/alerts`
  - Connection manager (track active user connections)
  - Push alert events to connected users

- [ ] **Day 34 — Telegram Bot**
  - Setup Telegram Bot với python-telegram-bot
  - Implement `/start` → link Telegram account to user
  - Implement alert delivery via Bot.send_message()

- [ ] **Day 35 — Alert Integration Test**
  - End-to-end test: simulate sentiment drop → rule match → WebSocket push → Telegram delivery
  - Edge cases: user disconnected, Telegram not linked, rate limits

---

# WEEK 6 — WebAuthn Authentication & User Management

- [ ] **Day 36 — WebAuthn Registration**
  - Install `py-webauthn` library (`pip install py-webauthn`)
  - Tạo `webauthn_credentials` table (SRS 5.1 schema)
  - Implement `POST /auth/webauthn/register/begin`: generate challenge → store in Redis (TTL 5min) → return `PublicKeyCredentialCreationOptions`
  - Implement `POST /auth/webauthn/register/complete`: verify response với `py_webauthn.verify_registration_response()` → lưu credential_id + public_key + sign_count
  - Issue JWT access_token + refresh_token sau khi verify thành công

- [ ] **Day 37 — WebAuthn Authentication + JWT Middleware**
  - Implement `POST /auth/webauthn/login/begin`: generate challenge → Redis TTL 5min → return `PublicKeyCredentialRequestOptions`
  - Implement `POST /auth/webauthn/login/complete`: verify bằng `py_webauthn.verify_authentication_response()` → check sign_count → issue JWT
  - FastAPI dependency: `get_current_user` (JWT Bearer decode)
  - RBAC: free | pro | enterprise | admin roles; decorator `require_tier(min_tier="pro")`
  - LeetCode: Maximum Subarray

- [ ] **Day 38 — Rate Limiting**
  - Redis token bucket per user per tier
  - Free: 60 req/min | Pro: 600 req/min | Enterprise: unlimited
  - Return `429 RATE_LIMIT_EXCEEDED` với `Retry-After` header

- [ ] **Day 39 — User Profile & Settings**
  - `GET /api/v1/users/me` — profile
  - `PUT /api/v1/users/me` — update (name, telegram_chat_id, email_alerts)
  - Telegram account linking flow

- [ ] **Day 40 — Passkey Management + Google OAuth fallback**
  - Implement `GET /auth/credentials` — list user's registered passkeys (device_name, last_used_at)
  - Implement `PATCH /auth/credentials/{id}` — đặt tên passkey ("iPhone Face ID", "YubiKey")
  - Implement `DELETE /auth/credentials/{id}` — xóa passkey với bảo vệ: không xóa passkey cuối cùng nếu không có Google linked
  - Setup Google OAuth2 với `authlib` như phương thức đăng nhập thay thế: `GET /auth/google` → `GET /auth/google/callback` → issue JWT

- [ ] **Day 41 — Security Hardening**
  - CORS allowlist (không dùng *)
  - Input sanitization check
  - SQL injection review (SQLAlchemy ORM?)
  - `pip-audit` → fix any vulnerable deps

- [ ] **Day 42 — Auth & Security Review**
  - All endpoints properly protected
  - Tier restrictions working per US-007
  - Rate limiting E2E test

---

# WEEK 7 — Frontend — React + Vite

- [ ] **Day 43 — React Setup**
  - Init: React 18 + Vite + TypeScript + Tailwind CSS
  - Install: Zustand, TanStack Query, Recharts, axios/fetch
  - Setup: Vite proxy → backend API

- [ ] **Day 44 — WebAuthn UI (Frontend)**
  - Install `@simplewebauthn/browser` (official WebAuthn browser library)
  - Registration flow: email input → `startRegistration()` → POST complete → lưu JWT
  - Authentication flow: email input → `startAuthentication()` → POST complete → lưu JWT
  - JWT token storage: httpOnly cookie (recommended) hoặc memory (không dùng localStorage)
  - Auth state trong Zustand; auto-refresh token logic
  - Passkey management page: list devices, rename, delete

- [ ] **Day 45 — News Feed Component**
  - News feed trang chính
  - Article card: title, source badge, published_at, sentiment badge (color-coded)
  - Infinite scroll / pagination
  - LeetCode: Maximum Product Subarray

- [ ] **Day 46 — AI Chat Interface**
  - Chat UI (messages + input)
  - SSE streaming integration: render content as it streams
  - Citations panel: clickable source links
  - Financial disclaimer hiển thị

- [ ] **Day 47 — Sentiment Dashboard**
  - Recharts LineChart: sentiment timeline
  - Asset selector: BTC, ETH, SOL...
  - "Data delayed 1h" badge cho free users

- [ ] **Day 48 — Alerts Panel**
  - Alert rule create form
  - Active rules list với toggle on/off
  - Alert history table
  - WebSocket connection cho real-time push

- [ ] **Day 49 — Frontend Polishing**
  - Dark mode toggle (Tailwind)
  - Responsive design (mobile breakpoints)
  - Loading states, error states, empty states

---

# WEEK 8 — Stripe Billing & Subscription

- [ ] **Day 50 — Stripe Setup**
  - Setup Stripe account → Products: CRYPTOLENS_PRO, CRYPTOLENS_ENTERPRISE
  - Install: stripe Python SDK
  - Configure Stripe webhook endpoint

- [ ] **Day 51 — Stripe Checkout**
  - `POST /api/v1/billing/checkout` → tạo Stripe Checkout Session
  - Frontend: Stripe Checkout redirect
  - Test mode: card 4242 4242 4242 4242

- [ ] **Day 52 — Stripe Webhooks**
  - Handle: `checkout.session.completed` → upgrade user role
  - Handle: `customer.subscription.deleted` → downgrade to free
  - Handle: `invoice.payment_failed` → notify user
  - Stripe signature verification (security)

- [ ] **Day 53 — Pricing Page**
  - Frontend `/pricing` page
  - Feature comparison table (Free / Pro / Enterprise)
  - "Upgrade Now" CTA buttons
  - 14-day trial CTA

- [ ] **Day 54 — Subscription Status**
  - `GET /api/v1/users/subscription` endpoint
  - Frontend: subscription badge in header
  - Upgrade prompt khi hit tier limits (US-004, US-007)

- [ ] **Day 55 — Billing Portal**
  - Stripe Customer Portal link (manage subscription, invoices)
  - `POST /api/v1/billing/portal` → Stripe Portal session

- [ ] **Day 56 — Billing E2E Test**
  - Test full flow: register → trial → upgrade → downgrade
  - Test webhook reliability

---

# WEEK 9 — Testing & Code Quality

- [ ] **Day 57 — Unit Test Setup**
  - Setup pytest + pytest-asyncio
  - Mock: OpenAI client, Qdrant client, external APIs
  - Target: 80% coverage

- [ ] **Day 58 — Service Unit Tests**
  - Test `EmbeddingService` (mock OpenAI)
  - Test `SentimentWorker` (mock LLM)
  - Test `AlertRuleEngine`

- [ ] **Day 59 — API Unit Tests**
  - Test all FastAPI endpoints với TestClient
  - Test auth middleware: 401, 403, 429 responses
  - LeetCode: Coin Change

- [ ] **Day 60 — Integration Tests**
  - Test full ingestion pipeline dengan test database (PostgreSQL)
  - Test RAG chat end-to-end (mock LLM, real Qdrant)
  - Test Stripe webhook handlers

- [ ] **Day 61 — Frontend Tests**
  - Vitest unit tests cho React components
  - Test: chat input, news feed rendering, auth forms

- [ ] **Day 62 — Load Testing**
  - Setup Locust
  - Scenario: 50 concurrent users → `/api/v1/chat` → measure P95 latency
  - Target: P95 < 3s

- [ ] **Day 63 — Code Refactor & Tech Debt**
  - Review all TODO comments
  - Extract reusable utilities
  - Ensure all env vars documented in `.env.example`

---

# WEEK 10 — Docker & CI/CD

- [ ] **Day 64 — Docker Compose**
  - Write `docker-compose.yml` với tất cả services: backend, workers, beat, postgres, qdrant, redis, prometheus, grafana
  - Environment variable injection
  - Volume mounts cho data persistence

- [ ] **Day 65 — Dockerfile Optimization**
  - Multi-stage Dockerfile cho backend (builder + runtime)
  - Minimize image size (< 500MB)
  - Non-root user trong container (security)

- [ ] **Day 66 — GitHub Actions CI**
  - Pipeline: on push → lint (ruff) → type check (mypy) → unit tests → pip-audit
  - Cache pip dependencies
  - Badge: build passing

- [ ] **Day 67 — GitHub Actions CD**
  - Deploy pipeline: on merge to main → build Docker image → push to registry → deploy
  - Railway deployment integration
  - Vercel deployment (frontend automatic)

- [ ] **Day 68 — Environment Management**
  - staging environment setup
  - `.env.staging` vs `.env.production` separation
  - Secrets via GitHub Actions Secrets

- [ ] **Day 69 — Database Migrations**
  - Alembic migration workflow trong CI/CD
  - `alembic upgrade head` trong deploy script
  - Rollback procedure documented

- [ ] **Day 70 — Production Deploy**
  - Deploy backend to Railway (hoặc AWS ECS)
  - Deploy frontend to Vercel
  - Monitor first 24h: errors, latency, costs
  - Domain + HTTPS setup

---

# WEEK 11 — Observability & LLMOps

- [ ] **Day 71 — Structured Logging**
  - Loguru structured JSON logs
  - Log fields: request_id, user_id, latency_ms, llm_model, tokens_used
  - Log levels per environment

- [ ] **Day 72 — OpenTelemetry**
  - Setup OpenTelemetry SDK (Python auto-instrumentation)
  - FastAPI traces → Jaeger (local dev)
  - Span attributes: user_id, query_length, retrieval_count

- [ ] **Day 73 — Prometheus Metrics**
  - Expose `/api/v1/metrics` endpoint (Prometheus format)
  - Custom metrics: chat_requests_total, llm_token_usage_total, ingestion_delay_seconds
  - Celery queue depth metrics

- [ ] **Day 74 — Grafana Dashboards**
  - Import Grafana dashboard JSON
  - Panels: request latency, error rate, LLM cost, ingestion pipeline, alert delivery
  - Alerts: Grafana alert rules → Telegram notification

- [ ] **Day 75 — LangSmith Setup**
  - Configure LangSmith tracing per LangGraph run
  - Tag traces: user_id, session_id, tier
  - Monitor: token usage, latency per node, error rate

- [ ] **Day 76 — RAGAS Evaluation Pipeline**
  - Setup RAGAS với test question set (50 queries)
  - Evaluate: Faithfulness, Answer Relevancy, Context Recall, Context Precision
  - Store results trong PostgreSQL `rag_evaluations` table

- [ ] **Day 77 — Cost Monitoring**
  - Track OpenAI API cost per user, per day
  - Alert khi cost > threshold per hour
  - LLM cost breakdown trong Grafana

---

# WEEK 12 — Advanced AI Features

- [ ] **Day 78 — Prompt Caching**
  - Implement semantic caching với Redis
  - Cache key: hash(query + recent context)
  - TTL: 10 phút (crypto news stale quickly)
  - Measure: cache hit rate target > 15%

- [ ] **Day 79 — Structured Outputs**
  - Ensure all LLM calls sử dụng structured output (Pydantic models via `response_format`)
  - Schemas: `SentimentOutput`, `NewsAnalysisOutput`, `ChatResponseOutput`

- [ ] **Day 80 — Self-Evaluation Node (LangGraph)**
  - Add `EvaluationNode` vào LangGraph graph
  - LLM checks: "Is this response faithful to the retrieved context?"
  - Retry với better prompt nếu faithfulness < threshold

- [ ] **Day 81 — Entity Extraction (NER)**
  - Extract asset symbols (BTC, ETH, SOL...) từ article text
  - Extract people, organizations, events
  - Store as structured metadata trong PostgreSQL

- [ ] **Day 82 — Social Media Sentiment**
  - Kết nối X/Twitter API v2 Filtered Stream
  - Kết nối Reddit API (r/CryptoCurrency, r/Bitcoin)
  - Weight social sentiment trong market aggregate

- [ ] **Day 83 — Sentiment Correlation**
  - Fetch price data từ CoinGecko API
  - Compute correlation: sentiment score vs price movement
  - Visualization trong dashboard

- [ ] **Day 84 — Advanced Alerts**
  - Alert condition: volume spike (articles > 3x baseline)
  - Alert condition: entity-specific (key person mention)
  - Email delivery với HTML template (SendGrid/SES)

---

# WEEK 13 — SaaS Launch Preparation

- [ ] **Day 85 — Admin Dashboard**
  - Admin-only: `/admin` route (role=admin guard)
  - User management: list users, change roles, deactivate
  - System health: worker status, queue depth, DB connections
  - Cost monitoring: LLM spend per day

- [ ] **Day 86 — Onboarding Flow**
  - Welcome email sequence (Day 1, Day 3, Day 7)
  - In-app onboarding tour (React Joyride)
  - Empty state guides: "Create your first alert"

- [ ] **Day 87 — GDPR Compliance**
  - `DELETE /api/v1/users/me` — full data deletion
  - `GET /api/v1/users/me/export` — JSON data export
  - Cookie consent banner
  - Privacy policy and Terms of Service pages

- [ ] **Day 88 — Security Final Audit**
  - OWASP ZAP scan on staging
  - `pip-audit` → 0 critical vulnerabilities
  - API key rotation procedure documented
  - Penetration test checklist completed

- [ ] **Day 89 — Performance Final Tuning**
  - Load test với 100 concurrent users
  - Qdrant index tuning (HNSW ef, m parameters)
  - PostgreSQL query explain (add missing indexes)
  - Redis cache warming

- [ ] **Day 90 — Documentation & README**
  - Update README.md với quickstart guide
  - API documentation (auto-generated từ FastAPI /docs)
  - Architecture diagrams finalized
  - Runbooks: deployment, rollback, disaster recovery

- [ ] **Day 91 — Launch 🚀**
  - Product Hunt / Twitter announcement
  - Monitor: errors, signup rate, payment conversion
  - Set up alerting cho business metrics (new signups, upgrades)
  - 14-day trial activation monitoring

---

# 📚 Learning Resources

## Core Technologies
- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **Qdrant**: https://qdrant.tech/documentation/
- **FastAPI**: https://fastapi.tiangolo.com
- **Celery**: https://docs.celeryq.dev

## LLMs & Embeddings
- **OpenAI API**: https://platform.openai.com/docs
- **Google Gemini**: https://ai.google.dev/docs
- **Ollama (Llama 3)**: https://ollama.ai/docs

## RAG & Evaluation
- **RAGAS**: https://docs.ragas.io
- **LangSmith**: https://docs.smith.langchain.com
- **DeepEval**: https://docs.confident-ai.com

## Infrastructure
- **Qdrant Docker**: https://qdrant.tech/documentation/guides/installation/
- **Redis Docs**: https://redis.io/docs
- **Docker**: https://docs.docker.com
- **GitHub Actions**: https://docs.github.com/en/actions

## Billing
- **Stripe**: https://stripe.com/docs
- **Stripe Webhooks**: https://stripe.com/docs/webhooks

## Observability
- **OpenTelemetry Python**: https://opentelemetry.io/docs/languages/python/
- **Prometheus**: https://prometheus.io/docs
- **Grafana**: https://grafana.com/docs

---

# 🎯 Final Skills After Completion

After completing this roadmap you will be proficient in:

- **Agentic RAG** systems với LangGraph (stateful multi-step agents)
- **Multi-LLM routing** (OpenAI, Google, open-source)
- **Production Vector DB** (Qdrant — hybrid search, payload filtering, HNSW)
- **LLMOps** (LangSmith tracing, RAGAS evaluation, prompt versioning)
- **Backend Engineering** (FastAPI, Celery, PostgreSQL, Redis)
- **SaaS product development** (Stripe billing, subscription management, RBAC)
- **DevOps** (Docker, GitHub Actions CI/CD, Railway/AWS deployment)
- **Observability** (OpenTelemetry, Prometheus, Grafana)
- **Security** (JWT auth, RBAC, OWASP, rate limiting)
- **Real-time systems** (WebSocket, SSE streaming, Celery Beat)

**Target Role**: AI Engineer (RAG / LLMOps / AI Agents) — SaaS Product Builder



Ông muốn chơi "hardcore" luôn đúng không? Đã hiểu. Để trở thành một **AI Engineer** thực thụ, ông không chỉ cần biết gọi API mà phải có tư duy tối ưu hóa bộ nhớ và thời gian (Big O).

Tôi đã "độ" lại một lộ trình **"LeetCode-A-Day"** gồm 91 bài, chia theo từng chặng để bổ trợ trực tiếp cho kiến thức kỹ thuật của dự án CryptoLens.

---

# ⚔️ 91-Day LeetCode Integration (The Grind Edition)

Mỗi ngày, hãy dành ra 30-45 phút trước khi code dự án để giải quyết một bài. Tôi đã sắp xếp chúng theo độ khó tăng dần và tính liên quan.

### 🟡 Chặng 1: Foundation (Tuần 1 - 3)

*Mục tiêu: Nhuần nhuyễn mảng, chuỗi và logic cơ bản để xử lý tin tức thô.*

| Ngày | Bài LeetCode | Chủ đề | Liên quan đến Dự án |
| --- | --- | --- | --- |
| **1-7** | Two Sum (1), Valid Anagram (242), Contains Duplicate (217), Best Time to Buy/Sell Stock (121), Valid Palindrome (125), Invert Binary Tree (226), Valid Parentheses (20) | **Arrays & Simple Logic** | Khởi động, kiểm tra dữ liệu trùng lặp trong RSS. |
| **8-14** | Binary Search (704), Flood Fill (733), Lowest Common Ancestor (235), Balanced Binary Tree (110), Linked List Cycle (141), Implement Queue using Stacks (232), Ransom Note (383) | **Search & Data Structures** | Tư duy về tìm kiếm tin tức và hàng đợi (Queue) trong Celery. |
| **15-21** | Climbing Stairs (70), Longest Palindrome (409), Reverse Linked List (206), Majority Element (169), Add Binary (67), Diameter of Binary Tree (543), Middle of the Linked List (876) | **Strings & Pointers** | Xử lý chuỗi văn bản tin tức dài và tối ưu bộ nhớ. |

---

### 🟠 Chặng 2: Data Mastery (Tuần 4 - 6)

*Mục tiêu: Xử lý các cấu trúc dữ liệu phức tạp cho Retrieval Layer và User Auth.*

| Ngày | Bài LeetCode | Chủ đề | Liên quan đến Dự án |
| --- | --- | --- | --- |
| **22-28** | Maximum Depth of Binary Tree (104), Contains Duplicate II (219), Roman to Integer (13), Backspace String Compare (844), Longest Common Prefix (14), Balanced Binary Tree (110) | **Trees & Strings** | Xử lý Metadata và cấu trúc dữ liệu phân cấp trong RAG. |
| **29-35** | Same Tree (100), Symmetric Tree (101), Linked List Cycle (141), Merge Two Sorted Lists (21), Move Zeroes (283), Intersection of Two Linked Lists (160) | **Linked Lists** | Logic nối chuỗi hội thoại (Chat Memory) và lịch sử chat. |
| **36-42** | Subtree of Another Tree (572), Squares of a Sorted Array (977), First Bad Version (278), Longest Repeating Character Replacement (424) | **Sliding Window** | Kỹ thuật **Chunking** tin tức (Sliding window over text). |

---

### 🔴 Chặng 3: System Logic (Tuần 7 - 9)

*Mục tiêu: Giải quyết bài toán Reranking, Caching và Billing.*

| Ngày | Bài LeetCode | Chủ đề | Liên quan đến Dự án |
| --- | --- | --- | --- |
| **43-49** | Group Anagrams (49), Top K Frequent Elements (347), Product of Array Except Self (238), Longest Consecutive Sequence (128), 3Sum (15) | **Hashing & Sorting** | Gom nhóm tin tức tương đồng và tìm các Token (BTC, ETH) hot nhất. |
| **50-56** | LRU Cache (146), LFU Cache (460), Container With Most Water (11), Find Minimum in Rotated Sorted Array (153), Search in Rotated Sorted Array (33) | **Advanced Caching** | Xây dựng Semantic Cache bằng Redis. |
| **57-63** | Min Stack (155), Evaluate Reverse Polish Notation (150), Daily Temperatures (739), Trapping Rain Water (42) | **Stacks & Monotonic** | Theo dõi biến động Sentiment theo thời gian. |

---

### 🟣 Chặng 4: Agentic & Production (Tuần 10 - 13)

*Mục tiêu: Đỉnh cao về Graph và Dynamic Programming cho LangGraph Agents.*

| Ngày | Bài LeetCode | Chủ đề | Liên quan đến Dự án |
| --- | --- | --- | --- |
| **64-70** | Course Schedule (207), Course Schedule II (210), Clone Graph (133), Number of Islands (200), Pacific Atlantic Water Flow (417) | **Graphs (BFS/DFS)** | Logic điều hướng trong **LangGraph Agents** (Phát hiện vòng lặp vô hạn). |
| **71-77** | Word Search (79), Kth Smallest Element in a BST (230), Binary Tree Right Side View (199), Word Break (139), Partition Equal Subset Sum (416) | **Backtracking & DP** | Tối ưu hóa việc gọi LLM và tự sửa lỗi (Self-Correction). |
| **78-84** | Sliding Window Maximum (239), Median from Data Stream (295), Merge k Sorted Lists (23), Smallest K elements (Heap) | **Heaps / Hard** | Reranking hàng ngàn bài báo thời gian thực. |
| **85-91** | Longest Increasing Subsequence (300), Coin Change (322), Unique Paths (62), Edit Distance (72) | **Dynamic Programming** | Tính toán độ tương đồng giữa câu trả lời AI và nguồn tin. |

---

### 💡 Lời khuyên cho ông trong Ngày 2 này:

Hôm nay là **Day 2**, ông hãy "khai đao" bằng bài **Two Sum (1)** hoặc **Valid Anagram (242)**. Nó không quá khó nhưng sẽ giúp ông làm nóng não trước khi "vật lộn" với `async/await` của `httpx`.

> **Nhắc nhở:** Hãy dùng **Python** để giải LeetCode luôn nhé, vì dự án này của mình thuần Python. Cố gắng viết code LeetCode theo kiểu "Clean Code" như cách mình đang dựng dự án.

Ông có muốn tôi bổ sung bài giải mẫu của bài **Two Sum** theo phong cách Pythonic (sử dụng Hash Map) để ông thấy nó giúp ích gì cho việc check trùng tin tức không?
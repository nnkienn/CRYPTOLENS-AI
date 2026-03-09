# CRYPTOLENS-AI

**AI-powered crypto news analysis & alert platform**  
Real-time market sentiment · Agentic RAG chat · Multi-LLM routing · WebSocket + Telegram alerts

[![Build](https://img.shields.io/github/actions/workflow/status/your-org/cryptolens-ai/ci.yml?branch=main)](https://github.com/your-org/cryptolens-ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## What is CRYPTOLENS-AI?

CRYPTOLENS-AI aggregates crypto news from CoinDesk, CoinTelegraph, CryptoPanic, Messari, The Block, and more — then analyzes it with AI to give traders and investors a real-time pulse on market sentiment. Users can chat with the AI, create smart alert rules, and receive notifications via Telegram or WebSocket — all powered by an Agentic RAG pipeline built on LangGraph + Qdrant.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI (Python 3.12) + async/await |
| Agentic RAG | LangGraph + LangChain |
| LLMs | OpenAI GPT-4o/4.1, Google Gemini 2.0 Flash, Llama 3 (self-hosted) |
| Embedding | OpenAI text-embedding-3-small |
| Vector DB | Qdrant |
| Relational DB | PostgreSQL 16 |
| Cache / Queue broker | Redis 7 |
| Background workers | Celery + Celery Beat |
| Frontend | React 18 + Vite + TypeScript + Tailwind CSS |
| Auth | **WebAuthn / Passkeys** (`py-webauthn` backend + `@simplewebauthn/browser` frontend) + JWT session |
| Billing | Stripe |
| Observability | OpenTelemetry + Prometheus + Grafana + LangSmith |
| Deployment | Docker Compose (dev) / Railway + Vercel (prod) |

---

## Project Structure

```
CRYPTOLENS-AI/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # FastAPI routers (chat, news, sentiment, alerts, auth, billing)
│   │   ├── services/        # Business logic
│   │   ├── models/          # SQLAlchemy ORM models
│   │   ├── schemas/         # Pydantic request/response schemas
│   │   ├── core/            # Config, security (JWT + WebAuthn), dependencies
│   │   └── main.py          # FastAPI app entrypoint
│   ├── workers/             # Celery tasks (crawler, embedding, sentiment, alert workers)
│   ├── rag/                 # LangGraph agent nodes and graph
│   ├── embeddings/          # Embedding service (OpenAI + fallback)
│   ├── evaluation/          # RAGAS evaluation pipeline
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/
├── frontend/                # React + Vite + Tailwind
├── docs/
│   ├── architecture_ai_crypto_news_system.md
│   ├── prd_ai_crypto_news_system.md
│   ├── srs_ai_crypto_news_system.md
│   ├── ai_engineer_pro_roadmap.md
│   ├── api_spec.md
│   └── adr/
│       ├── adr-001-vector-database.md
│       ├── adr-002-llm-providers.md
│       └── adr-003-rag-framework.md
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Quickstart (Local Development)

### Prerequisites

- Docker Desktop (latest)
- Python 3.12
- Node.js 20+
- OpenAI API key
- Google AI API key (optional)

### 1. Clone & configure environment

```bash
git clone https://github.com/your-org/cryptolens-ai.git
cd cryptolens-ai
cp .env.example .env
# Edit .env — fill in OPENAI_API_KEY, GOOGLE_API_KEY, and other required values
```

### 2. Start infrastructure services

```bash
docker compose up postgres qdrant redis -d
```

### 3. Backend setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start FastAPI dev server
uvicorn app.main:app --reload --port 8000
```

### 4. Start Celery workers

```bash
# In a separate terminal (venv activated)
celery -A app.workers worker --loglevel=info -Q news_crawler,embedding_worker,sentiment_worker,alert_worker
celery -A app.workers beat --loglevel=info
```

### 5. Frontend setup

```bash
cd frontend
npm install
npm run dev   # starts at http://localhost:5173
```

### 6. Verify everything works

```bash
curl http://localhost:8000/api/v1/health
# Expected: {"status": "healthy", "version": "1.0"}
```

API docs available at: http://localhost:8000/docs

---

## Full Docker Compose (All Services)

```bash
docker compose up --build
```

Services started:
- `backend` → http://localhost:8000
- `frontend` → http://localhost:5173
- `postgres` → localhost:5432
- `qdrant` → http://localhost:6333
- `redis` → localhost:6379
- `grafana` → http://localhost:3000
- `prometheus` → http://localhost:9090

---

## Environment Variables

See `.env.example` for the full list. Key variables:

```env
# LLM
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AI...

# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/cryptolens
QDRANT_URL=http://localhost:6333
REDIS_URL=redis://localhost:6379

# Auth — WebAuthn + JWT
JWT_SECRET_KEY=your-secret-key-minimum-32-chars
JWT_ALGORITHM=HS256
WEBAUTHN_RP_ID=localhost               # production: cryptolens.ai
WEBAUTHN_RP_NAME=CRYPTOLENS-AI
WEBAUTHN_ORIGIN=http://localhost:5173  # production: https://cryptolens.ai

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Observability
LANGSMITH_API_KEY=ls__...
LANGSMITH_PROJECT=cryptolens-ai

# App
APP_ENV=development
APP_CORS_ORIGINS=http://localhost:5173
```

---

## API Overview

Base URL: `http://localhost:8000/api/v1`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/auth/webauthn/register/begin` | Registration challenge | No |
| POST | `/auth/webauthn/register/complete` | Verify passkey → JWT | No |
| POST | `/auth/webauthn/login/begin` | Authentication challenge | No |
| POST | `/auth/webauthn/login/complete` | Verify signature → JWT | No |
| GET | `/auth/google` | Google OAuth2 (alternative) | No |
| POST | `/chat` | AI chat (SSE streaming) | JWT |
| GET | `/news` | Paginated news feed | JWT |
| GET | `/sentiment` | Market sentiment overview | JWT |
| GET | `/sentiment/timeline` | Sentiment time-series | JWT |
| POST | `/alerts/rules` | Create alert rule | JWT (Pro+) |
| GET | `/alerts/history` | Alert event history | JWT |
| POST | `/billing/checkout` | Stripe checkout session | JWT |
| GET | `/health` | Health check | No |

Full API spec: [docs/api_spec.md](docs/api_spec.md)  
Interactive docs (dev): http://localhost:8000/docs

---

## Running Tests

```bash
cd backend

# Unit tests
pytest tests/unit/ -v

# Integration tests (requires running postgres + qdrant)
pytest tests/integration/ -v

# All tests with coverage
pytest --cov=app --cov-report=html

# Security audit
pip-audit
```

---

## Documentation

| Doc | Description |
|---|---|
| [Architecture](docs/architecture_ai_crypto_news_system.md) | System design, data flow, deployment |
| [PRD](docs/prd_ai_crypto_news_system.md) | Product requirements, pricing, user stories |
| [SRS](docs/srs_ai_crypto_news_system.md) | Functional requirements, data models, API contracts |
| [Roadmap](docs/ai_engineer_pro_roadmap.md) | 91-day learning & build plan |
| [API Spec](docs/api_spec.md) | Full API contract |
| [ADR-001](docs/adr/adr-001-vector-database.md) | Why Qdrant |
| [ADR-002](docs/adr/adr-002-llm-providers.md) | Multi-LLM strategy |
| [ADR-003](docs/adr/adr-003-rag-framework.md) | LangGraph for Agentic RAG |

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'feat: add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## ⚠️ Disclaimer

CRYPTOLENS-AI provides AI-generated analysis for **informational purposes only**. Nothing in this platform constitutes financial advice. Always do your own research (DYOR) before making any investment decisions.

---

## License

MIT License — see [LICENSE](LICENSE) for details.

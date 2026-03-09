
# Product Requirement Document (PRD)
## CRYPTOLENS-AI — AI Crypto News Analysis & Alert System

| Field | Value |
|---|---|
| Version | 2.0 |
| Date | March 2026 |
| Owner | AI Engineer |
| Status | Active |
| Type | SaaS B2C / B2B |

### Version History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | Jan 2026 | AI Engineer | Initial draft |
| 2.0 | March 2026 | AI Engineer | Added SaaS pricing, monetization, user stories, MoSCoW, compliance, risk matrix, competitive analysis |

---

# Table of Contents

1. [Product Overview](#1-product-overview)
2. [Problem Statement](#2-problem-statement)
3. [Product Goals & Success Metrics](#3-product-goals--success-metrics)
4. [Stakeholders](#4-stakeholders)
5. [Target Users & Personas](#5-target-users--personas)
6. [Competitive Analysis](#6-competitive-analysis)
7. [Key Features (MoSCoW)](#7-key-features-moscow)
8. [User Stories](#8-user-stories)
9. [Monetization Model & Pricing Tiers](#9-monetization-model--pricing-tiers)
10. [MVP Scope](#10-mvp-scope)
11. [Future Roadmap](#11-future-roadmap)
12. [Compliance & Legal](#12-compliance--legal)
13. [Risk Matrix](#13-risk-matrix)
14. [Open Questions](#14-open-questions)

---

# 1. Product Overview

**CRYPTOLENS-AI** là một nền tảng SaaS phân tích tin tức crypto theo thời gian thực, sử dụng **Agentic RAG** (Retrieval Augmented Generation với LangGraph) và **Multi-LLM Routing** (OpenAI GPT-4o, Google Gemini 2.0 Flash, Llama 3 / Mistral) để:

- **Thu thập** tin tức thị trường từ nhiều nguồn đáng tin cậy (CoinDesk, CoinTelegraph, CryptoPanic, Messari, The Block, Decrypt, X/Twitter, Reddit)
- **Phân tích** sentiment thị trường theo từng asset và toàn thị trường
- **Tóm tắt** rủi ro và sự kiện quan trọng
- **Cảnh báo** người dùng theo thời gian thực qua WebSocket, Telegram, Email
- **Cho phép** người dùng chat AI với nguồn tin đã được kiểm chứng (RAG với citations)

**Vision**: Trở thành "Bloomberg Terminal" giá rẻ dành cho crypto retail traders và investors — cung cấp AI-powered intelligence trong tầm tay.

---

# 2. Problem Statement

### Thị trường

Thị trường crypto năm 2026:
- Tổng market cap > $3 Trillion
- >500 triệu users on-chain toàn cầu
- Hàng nghìn bài viết, tweet, post mỗi ngày về crypto

### Vấn đề cốt lõi

| Vấn đề | Tác động |
|---|---|
| Lượng tin tức quá lớn để theo dõi thủ công | Trader bỏ lỡ tin quan trọng |
| Nhiều nguồn tin nhiễu, tin giả, clickbait | Quyết định sai dựa trên thông tin sai |
| Thông tin phân tán qua nhiều kênh | Tốn thời gian tổng hợp |
| Không có phân tích sentiment thực tế | Khó đánh giá "mood" của thị trường |
| Không có cảnh báo rủi ro sớm | Phản ứng chậm với biến động |

### Tại sao AI là giải pháp đúng (March 2026)

- LLM (GPT-4o, Gemini 2.0 Flash) đã đủ mạnh và rẻ để phân tích tin tức real-time
- RAG đảm bảo AI chỉ nói về tin tức thực tế, không hallucinate
- Qdrant vector DB cho phép search ngữ nghĩa cực nhanh (<50ms)
- LLMOps tooling (LangSmith, RAGAS) giờ đã mature đủ cho production

---

# 3. Product Goals & Success Metrics

## 3.1 Business Goals

| Goal | Metric | Target (12 months post-launch) |
|---|---|---|
| Grow paying users | Number of Pro/Enterprise subscribers | 500 paying users |
| Achieve MRR | Monthly Recurring Revenue | $15,000 MRR |
| Product-Market Fit | NPS score | > 40 |
| Retention | Monthly churn rate | < 5% |
| Activation | Free-to-Pro conversion | > 5% |

## 3.2 Product Quality Metrics

| Metric | Target |
|---|---|
| Chat response latency (P95) | < 3 seconds |
| News freshness (publish → index) | < 15 minutes |
| Sentiment accuracy vs human label | > 82% |
| System uptime | 99.5% monthly |
| RAG Faithfulness score (RAGAS) | > 0.85 |
| Alert delivery latency | < 5 minutes |

## 3.3 User Success Metrics

| Metric | Target |
|---|---|
| Daily Active Users (DAU) / Monthly Active Users (MAU) | > 20% |
| Avg chat queries per user per day (Pro) | > 3 |
| Alert rules created per Pro user | > 2 |
| User returns within 7 days after signup | > 60% |

---

# 4. Stakeholders

| Stakeholder | Role | Interest |
|---|---|---|
| Product Owner | AI Engineer | Định hướng sản phẩm |
| Backend Engineer | AI Engineer | FastAPI, Celery, RAG pipeline |
| Frontend Engineer | AI Engineer | React dashboard |
| DevOps | AI Engineer | Docker, CI/CD, deployment |
| End Users | Traders / Investors / Researchers | Phân tích thị trường, cảnh báo |
| LLM Providers | OpenAI, Google | API cost partners |
| Payment Provider | Stripe | Billing & subscription |

---

# 5. Target Users & Personas

## Persona 1 — Alex, Retail Crypto Trader

| Field | Detail |
|---|---|
| Age | 28 |
| Occupation | Software engineer, trades crypto part-time |
| Goals | Không bỏ lỡ tin quan trọng trong khi đang làm việc |
| Pain Points | Không có thời gian đọc hết tin; bị "FUD" bởi clickbait |
| Tech Savvy | High |
| Willingness to Pay | $20-$30/month nếu thực sự hữu ích |
| Primary Features Needed | Telegram alerts, chat AI, sentiment dashboard |
| Tier | Pro |

## Persona 2 — Maria, Crypto Fund Analyst

| Field | Detail |
|---|---|
| Age | 35 |
| Occupation | Research analyst tại một crypto fund nhỏ |
| Goals | Cần phân tích tổng hợp tin tức hàng ngày; theo dõi nhiều assets cùng lúc |
| Pain Points | Phải đọc nhiều nguồn; không có tool tổng hợp tốt |
| Tech Savvy | High |
| Willingness to Pay | $200-$500/month (budget công ty) |
| Primary Features Needed | Portfolio tracker, custom webhooks, API access, advanced analytics |
| Tier | Enterprise |

## Persona 3 — Ben, Crypto Researcher / Academic

| Field | Detail |
|---|---|
| Age | 26 |
| Occupation | PhD student nghiên cứu market sentiment |
| Goals | Phân tích xu hướng sentiment theo thời gian |
| Pain Points | Không có dữ liệu sentiment có cấu trúc |
| Tech Savvy | Very High |
| Willingness to Pay | Prefer free; có thể trả $10/month |
| Primary Features Needed | Sentiment timeline, data export, API access |
| Tier | Free / Pro |

---

# 6. Competitive Analysis

| Product | Strengths | Weaknesses | CRYPTOLENS-AI Advantage |
|---|---|---|---|
| **LunarCrush** | Social volume data, established | Expensive ($50-$500/mo), no AI chat | AI chat + Agentic RAG, lower price |
| **Santiment** | On-chain data, professional | Very expensive, complex UI | Simpler UX, AI-native |
| **CryptoPanic** | Real-time news aggregation | No AI analysis, no chat | AI analysis, RAG chat, alerts |
| **Messari** | Deep research content | Premium ($300+/mo), content not AI-native | Real-time AI analysis, RAG retrieval |
| **ChatGPT + web search** | Flexible, general AI | No specialized crypto data, no real-time index, hallucination | Specialized RAG, verified sources, citations |
| **Perplexity AI** | Good web search RAG | Not crypto-specialized, no custom alerts | Domain-specific, custom alert rules |

**Positioning**: AI-native crypto intelligence platform với giá cả phải chăng — giữa Perplexity AI (general) và LunarCrush (expensive, no AI chat).

---

# 7. Key Features (MoSCoW)

## Must Have (MVP)

| Feature | Description |
|---|---|
| News Aggregation | Thu thập tự động từ CoinDesk, CoinTelegraph, CryptoPanic, The Block, Decrypt |
| AI RAG Chat | Chat AI với citations từ news được index; SSE streaming |
| Sentiment Analysis | Sentiment score + label cho mỗi bài viết và market tổng thể |
| Sentiment Dashboard | Timeline chart, trending assets, news feed với sentiment badges |
| WebSocket Alerts | In-app real-time alerts (tất cả tiers) |
| User Auth | **WebAuthn Passkeys** (passwordless) + JWT session; user roles (free/pro/enterprise) |
| Subscription (Stripe) | Free / Pro tier; Stripe checkout |
| Basic Rate Limiting | Per-tier rate limits |
| Financial Disclaimer | Disclaimer trong mọi AI response |

## Should Have (v1.1)

| Feature | Description |
|---|---|
| Telegram Alerts | Alert delivery qua Telegram bot (Pro+) |
| Email Alerts | Alert delivery qua Email (Pro+) |
| Social Sentiment | X/Twitter + Reddit sentiment data |
| Multi-LLM Routing | Automatic routing GPT-4o / Gemini 2.0 Flash / Llama 3 |
| RAG Evaluation | RAGAS metrics tracking, LangSmith integration |
| Data Export | Export sentiment data, news feed (Pro+) |
| Google OAuth | Social login (alternative cho users không có passkey device) |

## Could Have (v1.2)

| Feature | Description |
|---|---|
| Portfolio Tracker | Theo dõi portfolio vs news sentiment |
| Custom Webhook Alerts | Webhook delivery (Enterprise) |
| Admin Dashboard | User management, system health, cost monitoring |
| Multiple Assets Watch | Watch list với alerts per asset |
| Sentiment Correlation Analysis | BTC price vs sentiment correlation chart |

## Won't Have (này sinh ra đây không làm)

| Feature | Reason |
|---|---|
| Trading execution / order placement | Regulatory complexity, out of scope |
| On-chain data analysis | Too complex for MVP, separate product |
| Mobile native app (iOS/Android) | Web-first; mobile later |
| Multi-language support (non-English news) | Embedding + LLM cost; later phase |

---

# 8. User Stories

## Epic: News Aggregation

**US-001** (FR-001, Must Have)
> As a **retail trader**, I want to see a feed of the latest crypto news from multiple sources, so that I don't have to visit multiple news sites.

**Acceptance Criteria:**
- News feed loads within 1 second
- Shows at minimum CoinDesk, CoinTelegraph, CryptoPanic articles
- Each article shows: title, source, published_at, sentiment badge
- Feed updates without page refresh (WebSocket or polling every 60s)
- Free tier: news delayed 1 hour; Pro: real-time

---

**US-002** (FR-003, Must Have)
> As a **system admin**, I want duplicate articles automatically removed, so that users don't see the same news twice.

**Acceptance Criteria:**
- Duplicate detection based on content hash (MD5)
- Duplicate articles marked `is_duplicate=true` but not deleted (audit trail)
- Deduplication happens before embedding — no duplicate vectors in Qdrant

## Epic: AI Chat

**US-003** (FR-017, FR-018, Must Have)
> As a **crypto investor**, I want to ask the AI "What happened with SOL in the last 24 hours?" and get a response with source links, so that I can quickly understand the situation without reading 10 articles.

**Acceptance Criteria:**
- Response includes summary of relevant news
- Response cites minimum 3 sources with title + URL
- Response time P95 < 3 seconds
- Response ends with: "⚠️ This is not financial advice."
- Chat history saved and retrievable

---

**US-004** (FR-021, Must Have)
> As a **free tier user**, I want to be able to use the AI chat with lower rate limits, so that I can evaluate the product before upgrading.

**Acceptance Criteria:**
- Free users: 10 chat messages per day
- On limit exceeded: user sees friendly message with upgrade CTA
- Error code: `TIER_RESTRICTED` with `upgrade_url: /pricing`

## Epic: Sentiment Analysis

**US-005** (FR-025, FR-026, FR-027, Must Have)
> As a **retail trader**, I want to see a market sentiment chart for the last 24 hours, so that I can understand whether the market mood is improving or deteriorating.

**Acceptance Criteria:**
- Line chart shows sentiment score (-1.0 to 1.0) on Y-axis, time on X-axis
- Pro: updated every 15 min; Free: updated every 1 hour (with label "Data delayed 1h")
- Shows overall market + top 5 assets
- Color coded: positive (green) / neutral (gray) / negative (red)

## Epic: Alerts

**US-006** (FR-029, FR-030, FR-031, Must Have for Pro)
> As a **Pro subscriber**, I want to create an alert for "BTC negative sentiment drops below -0.4 in 1 hour", so that I get notified immediately when market turns bearish.

**Acceptance Criteria:**
- Alert rule form: asset selector, condition (sentiment </>), threshold, timeframe
- Alert delivered via in-app WebSocket within 5 minutes of trigger
- Alert delivered via Telegram within 5 minutes if Telegram linked
- Alert history available in UI for last 30 days

---

**US-007** (UC-003, Must Have)
> As a **free user trying to create a Telegram alert**, I want to see a clear upgrade message, so that I understand what tier is needed.

**Acceptance Criteria:**
- Error response: 403 with `code: TIER_RESTRICTED`, human-readable message
- UI shows modal: "Telegram alerts require Pro plan" + "Upgrade Now" button pointing to `/pricing`

## Epic: Subscription & Billing

**US-008** (FR-040, FR-041, Must Have)
> As a **free user who wants to upgrade**, I want to click "Upgrade to Pro" and complete payment via Stripe in under 2 minutes, so that I can immediately access Pro features.

**Acceptance Criteria:**
- Stripe Checkout page opens in < 1 second
- After successful payment: user role updated to "pro" within 60 seconds
- User receives confirmation email from Stripe
- Stripe webhook handles: `checkout.session.completed` → update `users.role`

---

**US-009** (FR-043, Must Have)
> As a **Pro subscriber who cancels**, I want my account to automatically downgrade to Free at the end of the billing period, so that I don't lose access abruptly.

**Acceptance Criteria:**
- Stripe sends `customer.subscription.deleted` event
- Webhook: update `users.role = 'free'` at subscription end date (not immediately)
- User receives email notification 7 days before cancellation takes effect

---

# 9. Monetization Model & Pricing Tiers

## 9.1 Pricing Tiers

| Feature | Free | Pro ($29/mo) | Enterprise ($199/mo) |
|---|---|---|---|
| **News Feed** | ✅ (1h delay) | ✅ Real-time | ✅ Real-time |
| **AI Chat** | 10 queries/day | Unlimited | Unlimited |
| **LLM Model** | Gemini 2.0 Flash | GPT-4o routing | GPT-4o priority |
| **Sentiment Dashboard** | ✅ (1h delay) | ✅ Real-time | ✅ Real-time |
| **In-app Alerts** | ✅ (3 rules max) | ✅ Unlimited | ✅ Unlimited |
| **Telegram Alerts** | ❌ | ✅ | ✅ |
| **Email Alerts** | ❌ | ✅ | ✅ |
| **Custom Webhook** | ❌ | ❌ | ✅ |
| **API Access** | ❌ | ❌ | ✅ |
| **Data Export (CSV/JSON)** | ❌ | ✅ | ✅ |
| **Chat History Retention** | 7 days | 1 year | Unlimited |
| **Sources** | 5 sources | All sources | All sources + social |
| **Asset Watch** | 3 assets | 20 assets | Unlimited |
| **Rate Limit** | 60 req/min | 600 req/min | Unlimited |
| **Support** | Community | Email (48h) | Priority (4h SLA) |

## 9.2 Annual Discount

- Pro Annual: $290/year (save $58, ~16% discount)
- Enterprise Annual: $1,990/year (save $398, ~16% discount)

## 9.3 Revenue Model

| Revenue Stream | Description |
|---|---|
| Subscription (primary) | Pro + Enterprise monthly/annual subscriptions |
| Enterprise custom | Custom contract cho quỹ/tổ chức (>$500/mo) |
| API licensing (future) | Bán raw sentiment data API |

## 9.4 Unit Economics (Estimates)

| Item | Free | Pro | Enterprise |
|---|---|---|---|
| LLM cost/user/month | ~$0.10 | ~$3.50 | ~$8 |
| Infrastructure cost/user/month | ~$0.20 | ~$0.50 | ~$1 |
| Gross Margin | N/A | ~85% | ~95% |

## 9.5 Stripe Integration

- Product: CRYPTOLENS_PRO, CRYPTOLENS_ENTERPRISE
- Billing: Stripe Billing (monthly + annual)
- Webhook events handled: `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`, `invoice.payment_failed`, `invoice.payment_succeeded`
- Free trial: 14 ngày Pro trial khi đăng ký (không cần thẻ)

---

# 10. MVP Scope

MVP (Target: 12 tuần từ start) bao gồm:

| Component | Scope |
|---|---|
| News Sources | CoinDesk, CoinTelegraph, CryptoPanic, The Block, Decrypt (5 sources RSS) |
| AI Chat | RAG chat với GPT-4o/Gemini 2.0 Flash routing, streaming, citations |
| Sentiment | Score + label per article, market aggregate, timeline chart |
| Alerts | In-app WebSocket alerts; Telegram alerts (Pro) |
| Auth | Email/password + JWT |
| Billing | Stripe — Free + Pro tiers |
| Deployment | Docker + Vercel + Railway |
| Observability | LangSmith + Loguru |

**Out of scope for MVP**: Social media sentiment, Enterprise tier, mobile app, API access, portfolio tracker, admin dashboard.

---

# 11. Future Roadmap

## v1.1 (Q2 2026)

- Social media sentiment (X/Twitter + Reddit)
- Email alerts (Pro)
- Google OAuth social login
- RAG evaluation (RAGAS) dashboard
- Admin panel (user management, cost monitoring)
- Data export (CSV/JSON)

## v1.2 (Q3 2026)

- Enterprise tier launch (custom webhooks, API access)
- Portfolio tracker (watch list + sentiment correlation)
- Multi-asset sentiment comparison chart
- Self-hosted Llama 3 worker für privacy-conscious Enterprise clients
- Localization (Vietnamese, Chinese)

## v2.0 (Q4 2026)

- AI Trading Signals (LLM + sentiment + price correlation — with regulatory disclaimer)
- Mobile web PWA
- White-label solution cho crypto exchanges
- On-chain data integration (Nansen, Glassnode APIs)

---

# 12. Compliance & Legal

## 12.1 Financial Disclaimer

- **Bắt buộc** trong mọi AI response (FR-024): *"⚠️ This analysis is for informational purposes only and does not constitute financial advice. Always DYOR (Do Your Own Research)."*
- Disclaimer phải hiển thị cố định trong Chat UI và Dashboard footer
- Terms of Service phải nêu rõ: hệ thống không chịu trách nhiệm về quyết định đầu tư

## 12.2 GDPR Compliance (EU Users)

| Right | Implementation |
|---|---|
| Right to be forgotten | DELETE /api/v1/users/me — xóa toàn bộ data |
| Data portability | GET /api/v1/users/me/export — JSON export |
| Consent | Explicit checkbox khi đăng ký |
| Data minimization | Chỉ lưu dữ liệu cần thiết |
| Privacy Policy | Cần có trước public launch |
| Cookie consent | Cookie banner theo GDPR |

## 12.3 News Content Copyright

- Chỉ lưu **headline + summary + metadata** — không reproduce full article nếu nguồn không cho phép
- Luôn link back đến bài gốc
- Crawler phải check và tôn trọng `robots.txt`
- Cần Terms of Use với các news sources (đặc biệt Messari, The Block)

## 12.4 Data Residency

- User data (PostgreSQL): EU-region cho EU users (Railway EU / AWS eu-west-1)
- Vector data (Qdrant Cloud): configurable region
- LLM API calls: OpenAI/Google — data processed theo ToS của họ; Enterprise users cần acknowledge

---

# 13. Risk Matrix

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| OpenAI API cost spike | Medium | High | Multi-LLM routing → Gemini/Llama fallback; budget alerts |
| X/Twitter API pricing increase | High | Medium | Design as optional feature; Reddit als alternative |
| News source blocks crawler | Medium | Medium | User-agent rotation; respect robots.txt; use official APIs |
| Qdrant Cloud outage | Low | High | Fallback to Redis cache; degraded mode without vector search |
| LLM hallucination với crypto advice | Medium | Very High | RAG citations mandatory; financial disclaimer; prompt guardrails |
| GDPR fine (EU users) | Low | Very High | Full GDPR implementation before EU marketing |
| Churn: users don't find value | Medium | High | 14-day Pro trial; onboarding flow; product analytics |
| Competitor copies features | High | Medium | Speed of execution; community; brand moat |
| Stripe payment failure | Low | High | Retry logic; dunning emails; grace period |
| Security breach (API keys leaked) | Low | Critical | Secrets management; regular rotation; pip-audit in CI |

---

# 14. Open Questions

| Question | Owner | Due |
|---|---|---|
| Có cần business license cho crypto advisory service ở Việt Nam? | Product Owner | Before launch |
| Messari API — có ToS điều khoản cho AI/RAG usage không? | Product Owner | Q2 2026 |
| 14-day trial có cần thẻ tín dụng không? | Product Owner | Before MVP |
| Enterprise SLA — uptime guarantee contract cần legal review? | Product Owner | Before Enterprise launch |
| On-premise deployment option có cần thiết cho Enterprise không? | Product Owner | Q3 2026 |


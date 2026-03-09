# ADR-002: Multi-LLM Provider Strategy

| Field | Value |
|---|---|
| Date | March 2026 |
| Status | Accepted |
| Deciders | AI Engineer |
| Replaces | Single LLM (GPT-4o only in v1.0) |

---

## Context

CRYPTOLENS-AI cần LLM cho 3 use cases chính:

1. **RAG Chat**: Generate analysis responses từ retrieved context (latency-sensitive)
2. **Sentiment Analysis**: Structured output — score, label, risk_level (throughput-sensitive)
3. **Query Planning**: Classify query type, expand queries (fast, cheap)

Với single LLM provider (GPT-4o only):
- Cost cao với high volume users
- Single point of failure nếu OpenAI có outage
- Không phù hợp cho Free tier (margin âm)
- Enterprise clients có thể yêu cầu no-external-API-call (data privacy)

---

## Decision

**Implement Multi-LLM Routing** với chiến lược sau:

| LLM | Primary Use Case | Routing Trigger |
|---|---|---|
| OpenAI GPT-4o / GPT-4.1 | Complex analysis, Pro/Enterprise chat | Complex query, Enterprise user |
| Google Gemini 2.0 Flash | Standard queries, Free tier, Sentiment | Standard query, Free tier, high-volume |
| Llama 3 / Mistral (self-hosted via Ollama) | Privacy-sensitive, offline fallback | Enterprise on-premise, all-LLMs-fail |

---

## Options Considered

### Option A: OpenAI GPT-4o Only (v1.0)

**Pros**: Highest quality, simplest implementation

**Cons**:
- ~$15/1M output tokens — expensive for Free tier
- Single point of failure
- No privacy option for Enterprise
- Cannot control costs per user tier

### Option B: Anthropic Claude 3.5/3.7

**Pros**: Strong reasoning, good for long context

**Cons**:
- Similar pricing to GPT-4o
- No open-source version available
- Still single-vendor dependency

### Option C: Multi-LLM Routing ✅ (chosen)

**Components**:
- **OpenAI GPT-4o/4.1**: Primary for complex, high-value queries
- **Google Gemini 2.0 Flash**: Cost-effective ($0.60/1M output tokens vs GPT-4o $15), fast (sub-1s responses), excellent for standard sentiment analysis
- **Llama 3 / Mistral (Ollama)**: Self-hosted, zero API cost, for: privacy-sensitive Enterprise, fallback when APIs fail

**Pros**:
- Cost control: route Free tier → Gemini 2.0 Flash (25x cheaper than GPT-4o)
- Resilience: if OpenAI API down → fallback to Gemini → fallback to Llama
- Privacy: Enterprise can opt for 100% self-hosted Llama
- Quality: Pro/Enterprise get GPT-4o for best results

**Cons**:
- More complex implementation (LLM Router node in LangGraph)
- Output consistency may vary across models
- Need to maintain compatibility with all 3 model APIs
- Llama requires GPU or powerful CPU server

---

## LLM Router Logic

Implemented as a LangGraph node (`LLMRouterNode`):

```python
def route_llm(state: AgentState) -> str:
    user_tier = state["user"].role
    query_complexity = state["query_complexity"]  # "simple" | "complex"

    if user_tier == "free":
        return "gemini_2_flash"

    if user_tier in ("pro", "enterprise"):
        if query_complexity == "complex":
            return "gpt_4o"
        else:
            return "gemini_2_flash"

    # Fallback
    return "gemini_2_flash"
```

**Fallback chain on API failure**:
```
Primary LLM fails
       ↓ (retry 1x, 1s backoff)
Secondary LLM
       ↓ (retry 1x, 1s backoff)
Llama 3 (self-hosted)
       ↓ (if Ollama unavailable)
Return 503 LLM_UNAVAILABLE
```

---

## Cost Projection

| Scenario | LLM Used | Est. Cost/User/Month |
|---|---|---|
| Free user (10 queries/day) | Gemini 2.0 Flash | ~$0.05 |
| Pro user (50 queries/day) | 70% Gemini, 30% GPT-4o | ~$3.50 |
| Enterprise user (200 queries/day) | 50% Gemini, 50% GPT-4o | ~$15 |

---

## Consequences

### Positive
- Free tier viable with positive margin
- 99.9%+ LLM availability (3 providers)
- Enterprise data privacy option
- Cost scales properly with tier

### Negative
- 3 API keys to manage (OpenAI, Google, Ollama endpoint)
- Response format normalization needed (each LLM has different API)
- Ollama requires server infrastructure for self-hosted operation
- Gemini output quality slightly lower for complex multi-hop reasoning

---

## Implementation Notes

Use LangChain's `ChatOpenAI`, `ChatGoogleGenerativeAI`, `ChatOllama` with unified `.invoke()` interface:

```python
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_models import ChatOllama

LLM_REGISTRY = {
    "gpt_4o": ChatOpenAI(model="gpt-4o", streaming=True),
    "gemini_2_flash": ChatGoogleGenerativeAI(model="gemini-2.0-flash", streaming=True),
    "llama_3": ChatOllama(model="llama3", streaming=True),
}
```

All responses must go through `StructuredOutputParser` to normalize format regardless of which LLM generated them.

---

## Review Date

Review Q3 2026 — evaluate if Anthropic Claude should be added (strong for long context analysis). Also review cost actuals vs projections after 3 months of production traffic.

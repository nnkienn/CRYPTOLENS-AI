# ADR-003: RAG Framework — LangGraph for Agentic RAG

| Field | Value |
|---|---|
| Date | March 2026 |
| Status | Accepted |
| Deciders | AI Engineer |
| Replaces | Simple LangChain pipeline (v1.0) |

---

## Context

CRYPTOLENS-AI cần orchestrate một RAG pipeline với các yêu cầu sau:

- **Multi-step reasoning**: Một số queries cần nhiều bước (plan → retrieve → evaluate → re-retrieve → generate)
- **Conditional routing**: Route sang different LLMs, different retrieval strategies dựa trên context
- **Self-evaluation**: Agent cần tự check xem response có faithful không, có cần retry không
- **State management**: Maintain conversation state, query plan, retrieved context across steps
- **Streaming**: SSE streaming từ LLM đến client

Với simple LangChain LCEL (Linear Expression Language) pipeline (v1.0):
- Không có conditional branching
- Không có state management
- Không thể loop/retry nếu retrieval quality thấp
- Không thể implement multi-step query planning

---

## Decision

**Sử dụng LangGraph** để orchestrate Agentic RAG thay vì simple LangChain pipeline.

---

## Options Considered

### Option A: Simple LangChain LCEL Pipeline (v1.0)

```python
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```

**Pros**: Simple, fast to implement, minimal code

**Cons**:
- Linear only — no branching, no loops
- No state between steps
- Cannot implement: query planning, self-evaluation, multi-hop retrieval
- Not suitable for complex agentic workflows

### Option B: Custom Agent Loop (no framework)

**Pros**: Full control

**Cons**:
- High implementation effort
- No tooling (debugging, visualization)
- Reinventing the wheel

### Option C: LangGraph ✅ (chosen)

LangGraph là extension của LangChain dành riêng cho **stateful multi-step agents**.

```python
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    query: str
    query_type: str          # simple | complex | multi-hop
    user: UserContext
    retrieved_chunks: list
    context: str
    response: str
    citations: list
    evaluation: dict         # faithfulness check result
    retry_count: int

graph = StateGraph(AgentState)
graph.add_node("query_planner", query_planner_node)
graph.add_node("hybrid_retriever", hybrid_retriever_node)
graph.add_node("reranker", reranker_node)
graph.add_node("context_builder", context_builder_node)
graph.add_node("guardrails", guardrails_node)
graph.add_node("llm_router", llm_router_node)
graph.add_node("generator", generator_node)
graph.add_node("evaluator", evaluator_node)

graph.add_conditional_edges(
    "query_planner",
    should_expand_query,
    {"expand": "multi_query_expander", "direct": "hybrid_retriever"}
)
graph.add_conditional_edges(
    "evaluator",
    should_retry,
    {"retry": "hybrid_retriever", "done": END}
)
```

**Pros**:
- Stateful: full state maintained across all nodes
- Conditional routing: different paths for different query types
- Loops: self-evaluation node can loop back to retrieval if quality low
- Streaming: built-in SSE streaming support
- Visualizable: graph can be rendered as diagram
- LangSmith integration: each node traced separately
- Active development: LangGraph v0.2+ is production-stable as of 2026

**Cons**:
- Steeper learning curve than simple LCEL
- More code than simple pipeline
- Graph debugging can be complex for new developers

---

## LangGraph vs Alternatives (2026)

| Framework | Status (March 2026) | Best For |
|---|---|---|
| LangGraph | Stable, widely adopted | Complex agentic RAG, stateful agents |
| LangChain LCEL | Stable | Simple linear pipelines |
| CrewAI | Stable | Multi-agent collaboration |
| AutoGen (Microsoft) | Stable | Conversational multi-agent |
| LlamaIndex Workflows | Stable | Document Q&A, simple RAG |

**Verdict**: LangGraph is the right choice dla complex RAG with branching, loops, and state management.

---

## Graph Design

```
START
  ↓
QueryPlannerNode — determines query complexity and type
  ↓ (conditional)
  ├── [complex] → MultiQueryExpanderNode
  └── [simple]  ↓
              HybridRetrieverNode — Qdrant dense + BM25 sparse
                  ↓
              RerankerNode — CrossEncoder top-20 → top-5
                  ↓
              ContextBuilderNode — format context + metadata
                  ↓
              GuardrailsNode — injection detection, safety check
                  ↓ (conditional)
              ├── [unsafe] → SafeResponseNode → END
              └── [safe]  ↓
                        LLMRouterNode — select GPT-4o | Gemini | Llama
                            ↓
                        GeneratorNode — streaming LLM call
                            ↓
                        EvaluatorNode — RAGAS faithfulness check
                            ↓ (conditional)
                        ├── [low_quality, retry < 2] → HybridRetrieverNode (loop)
                        └── [pass] → END
```

---

## Consequences

### Positive
- Full agentic capability: query planning, self-healing, conditional routing
- Each node is independently testable
- LangSmith traces each node → easy debugging
- Self-evaluation node prevents low-quality responses from reaching users
- Streaming works naturally via LangGraph streaming mode

### Negative
- Developers must learn LangGraph API (StateGraph, nodes, edges)
- Complex graphs are harder to understand for new contributors
- Longer initial implementation time vs simple LCEL (Week 4 in roadmap)
- State schema must be carefully designed upfront (TypedDict)

---

## Migration from v1.0

v1.0 used a simple LCEL chain (never fully implemented — was prototype only). No migration needed — starting fresh with LangGraph from Week 4 of the roadmap.

---

## Review Date

Review Q4 2026 — evaluate if CrewAI multi-agent should be added for use cases requiring multiple specialized agents (e.g., a dedicated "Breaking News Detector" agent + "Sentiment Analyst" agent running in parallel).

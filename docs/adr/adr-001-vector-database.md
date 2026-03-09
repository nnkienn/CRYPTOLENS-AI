# ADR-001: Vector Database — Qdrant

| Field | Value |
|---|---|
| Date | March 2026 |
| Status | Accepted |
| Deciders | AI Engineer |
| Replaces | ChromaDB (v1.0) |

---

## Context

CRYPTOLENS-AI cần một vector database để lưu trữ và tìm kiếm embedding vectors của crypto news articles. Requirements:

- Hybrid search (dense vector + sparse/keyword)
- Payload filtering (by asset_symbol, published_at, sentiment_label)
- Production-grade reliability và performance
- Self-hostable (cost control) nhưng có managed cloud option
- High ingestion throughput (hàng nghìn articles/ngày)
- Sub-100ms query latency

---

## Decision

**Chọn Qdrant** thay vì ChromaDB (v1.0) hoặc Pinecone.

---

## Options Considered

### Option A: ChromaDB (current v1.0)

**Pros**:
- Đơn giản, Python-native API
- Tốt cho prototyping và local development
- Không cần infrastructure riêng (embedded mode)

**Cons**:
- Không có production-grade distributed mode (tính đến March 2026)
- Payload filtering kém linh hoạt hơn Qdrant
- Không hỗ trợ hybrid search natively
- Performance kém hơn với large-scale collections
- Không có managed cloud service đáng tin cậy

### Option B: Pinecone (fully managed)

**Pros**:
- Fully managed — không cần ops
- Excellent performance và reliability
- Good hybrid search support

**Cons**:
- Đắt hơn đáng kể ($70+/month cho production)
- Vendor lock-in — không self-hostable
- Data leaves your infrastructure (compliance risk cho Enterprise)
- Free tier giới hạn mạnh (1 index, 1GB)

### Option C: Qdrant ✅ (chosen)

**Pros**:
- HNSW indexing — state-of-the-art ANN search performance
- Native hybrid search (dense + sparse vectors)
- Rich payload filtering với Qdrant Filter API
- Self-hostable với Docker (cost control dev)
- Qdrant Cloud (managed) cho production với free tier đủ cho MVP
- Horizontal scaling với distributed mode
- Active development (v1.x updates monthly as of 2026)
- gRPC + REST APIs
- No vendor lock-in — chuyển giữa self-host và cloud dễ dàng

**Cons**:
- Phức tạp hơn ChromaDB để setup
- Cần maintain nếu self-hosted
- Qdrant Cloud free tier: 1GB (đủ cho MVP ~500K chunks)

---

## Consequences

### Positive
- Hybrid search (dense + BM25 sparse) cải thiện retrieval quality đáng kể so với pure vector search
- Payload filtering cho phép query: "BTC articles in last 24h with negative sentiment" trong 1 Qdrant query
- Production pathway rõ ràng: Qdrant Cloud (MVP) → self-hosted cluster (scale)
- Enterprise clients có thể yêu cầu on-premise deployment — Qdrant self-hosted đáp ứng

### Negative
- Phải migrate existing ChromaDB data (không có data trong v1.0, chỉ là prototype)
- SRS và Architecture docs phải cập nhật (đã done trong v2.0)
- Developers cần học Qdrant Python client API

---

## Implementation Notes

```python
# Collection schema
qdrant_client.create_collection(
    collection_name="crypto_news_articles",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
    sparse_vectors_config={
        "bm25": SparseVectorParams()  # for keyword search
    }
)

# Upsert with payload
qdrant_client.upsert(
    collection_name="crypto_news_articles",
    points=[
        PointStruct(
            id=str(uuid4()),
            vector=dense_embedding,
            payload={
                "article_id": str(article.id),
                "source": article.source,
                "published_at": article.published_at.isoformat(),
                "asset_symbols": article.asset_symbols,
                "sentiment_label": article.sentiment_label,
                "risk_level": article.risk_level,
                "chunk_index": chunk_index,
                "chunk_text": chunk_text
            }
        )
    ]
)
```

---

## Review Date

Review nếu Qdrant không đáp ứng performance requirements khi collection > 10M vectors, hoặc nếu Pinecone significantly reduces pricing.

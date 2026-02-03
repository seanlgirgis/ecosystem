# Spec: Phase 1 - SecondBrain API

**Status:** IMPLEMENTED  
**Original Target:** Week 1  
**Implemented:** 2026-02-03  
**Spec Version:** 1.0 (Retroactive documentation)

---

## 1. Purpose

Build the immortal knowledge layer. SecondBrain remembers everything, caches AI responses to reduce API costs, and enables semantic search across accumulated knowledge.

---

## 2. Requirements

### 2.1 Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| R1 | Store arbitrary data by unique key (remember) | P0 |
| R2 | Retrieve data by exact key (recall) | P0 |
| R3 | Cache AI responses with TTL (cache_store) | P0 |
| R4 | Retrieve cached responses by similarity (cache_get) | P0 |
| R5 | Semantic search across knowledge (search_knowledge) | P1 |
| R6 | Log all AI interactions (log_interaction) | P1 |
| R7 | Cache hit analytics (get_cache_stats) | P2 |

### 2.2 Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| N1 | Cache lookup under 100ms | P0 |
| N2 | Graceful degradation if Qdrant unavailable | P0 |
| N3 | Data persists across restarts | P0 |
| N4 | 90%+ cache similarity threshold | P0 |
| N5 | Embeddings generated locally (no API calls) | P1 |

---

## 3. Architecture

### 3.1 Storage Stack

```
API Layer (remember, recall, cache_store, cache_get)
         |
    +----+----+
    |         |
 Local      Vector
 Pickle     Qdrant
 Files      DB
    |         |
    +----+----+
         |
   Local Embeddings
   Ollama (nomic)
```

### 3.2 Storage Responsibilities

| Component | Purpose | If Unavailable |
|-----------|---------|----------------|
| Pickle | Fast local persistence | N/A (primary) |
| Qdrant | Semantic similarity search | Falls back to pickle exact-match |
| Ollama | Generate embeddings | Falls back to hash-based matching |

### 3.3 File Locations

```
C:\ecosystem\data\              (gitignored - local state)
├── cache\cache.pkl             (Cached AI responses)
├── memory\memory.pkl            (Permanent knowledge)
└── memory\conversations.pkl    (Conversation history)
```

---

## 4. Interface Specification

### 4.1 Core API

```python
def remember(key: str, value: Any, metadata: dict = None) -> bool:
    """Store permanent knowledge.
    
    Args:
        key: Unique identifier (e.g., "client_acme")
        value: Serializable data
        metadata: Optional context (source, tags, timestamp)
    
    Returns:
        True if stored successfully
    """


def recall(key: str) -> Optional[dict]:
    """Retrieve knowledge by exact key.
    
    Returns:
        Dict with value, metadata, timestamps, or None
    """


def cache_store(query: str, response: str, model: str = "unknown",
                ttl: int = 86400) -> bool:
    """Cache AI response for cost reduction.
    
    Args:
        query: Original query text
        response: AI response to cache
        model: Which model generated it
        ttl: Time-to-live in seconds (default 24h)
    """


def cache_get(query: str, similarity_threshold: float = 0.90) -> Optional[str]:
    """Find cached response by similarity.
    
    Args:
        query: Current query
        similarity_threshold: Minimum match (0.0-1.0)
    
    Returns:
        Cached response if match found and not expired
    """
```

### 4.2 Secondary API

```python
def search_knowledge(query: str, limit: int = 5) -> list:
    """Semantic search across all stored knowledge."""


def get_cache_stats() -> dict:
    """Analytics: hits, savings, hit rate."""


def log_interaction(query: str, response: str, model: str,
                    cost: float = 0.0) -> str:
    """Log conversation for analysis."""
```

---

## 5. Data Models

### 5.1 MemoryRecord

```python
@dataclass
class MemoryRecord:
    key: str
    value: Any
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
```

### 5.2 CachedResponse

```python
@dataclass
class CachedResponse:
    query_hash: str
    query_text: str
    response: str
    model: str
    hit_count: int
    expires_at: Optional[datetime]
```

---

## 6. Implementation Details

### 6.1 Caching Strategy

1. Exact Match First: Check cache.pkl by query hash
2. Similarity Fallback: Query Qdrant with embedding
3. TTL Enforcement: Reject expired entries
4. Hit Counting: Track cache effectiveness

### 6.2 Embedding Generation

- Model: nomic-embed-text via Ollama
- Vector Size: 384 dimensions
- Cache: In-memory embedding cache to avoid recomputation
- Fallback: If Ollama unavailable, use hash-based matching only

### 6.3 Error Handling

| Error | Behavior |
|-------|----------|
| Qdrant down | Continue with pickle-only |
| Ollama down | Hash-based matching only |
| Disk full | Raise exception (cannot recover) |
| Corrupt pickle | Start fresh (log warning) |

---

## 7. Acceptance Criteria

- [x] remember() stores and recall() retrieves correctly
- [x] cache_store() + cache_get() round-trip works
- [x] Cache respects TTL (expired entries rejected)
- [x] Similarity matching finds 90%+ matches
- [x] Graceful degradation without Qdrant/Ollama
- [x] Data persists across Python restarts
- [x] All functions have type hints and docstrings
- [x] Unit tests pass (test_secondbrain.py)

---

## 8. Dependencies

```
requirements.txt:
- qdrant-client>=1.7.0    (vector DB)
- requests>=2.31.0        (Ollama HTTP API)
- pydantic>=2.0.0         (data validation)
- numpy>=1.24.0           (vector ops)
```

External services (Docker):
- Qdrant (port 6333) - optional
- Ollama (port 11434) - optional

---

## 9. Out of Scope (Explicitly)

- Encryption at rest (future consideration)
- Distributed storage (single machine)
- Web API/HTTP interface (local Python only)
- Automatic conflict resolution (last-write-wins)
- Compression (pickle handles this)

---

## 10. Test Plan

```python
# test_secondbrain.py
def test_remember_recall():
    remember("test", {"data": 123})
    result = recall("test")
    assert result["value"]["data"] == 123

def test_cache_roundtrip():
    cache_store("query", "response")
    assert cache_get("query") == "response"

def test_cache_similarity():
    cache_store("What is Python?", "A language")
    result = cache_get("What is Python programming?", threshold=0.85)
    assert result is not None
```

---

## 11. References

- Implementation: secondbrain/api/memory.py
- Storage: secondbrain/storage/vector_store.py
- Ingest: secondbrain/ingest/chat_logger.py
- Utils: shared/utils/embeddings.py
- Tests: test_secondbrain.py

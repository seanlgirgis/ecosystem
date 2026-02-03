"""Memory API Core

The primary interface for SecondBrain. All knowledge storage and retrieval
flows through these four functions.

Interface:
    remember(key: str, value: Any, metadata: dict = None) -> bool
    recall(key: str) -> Optional[MemoryRecord]
    cache_store(query_hash: str, response: str, ttl: int = 86400) -> bool
    cache_get(query_hash: str, similarity_threshold: float = 0.90) -> Optional[str]
"""

import json
import pickle
from datetime import datetime, timedelta
from typing import Any, Optional
from pathlib import Path

from shared.utils.embeddings import get_embedding, hash_text
from shared.models.schemas import MemoryRecord, CachedResponse

# Storage paths - SEPARATE FROM CODE (gitignored)
DATA_ROOT = Path("C:/ecosystem/data")
STORAGE_ROOT = Path("C:/ecosystem/secondbrain/storage")
MEMORY_FILE = DATA_ROOT / "memory" / "memory.pkl"
CACHE_FILE = DATA_ROOT / "cache" / "cache.pkl"

# In-memory stores (persisted to disk)
_memory_store: dict = {}
_cache_store: dict = {}


def _ensure_storage():
    """Ensure storage directory exists and load persisted data."""
    global _memory_store, _cache_store
    
    # Create data directories (gitignored, separate from code)
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    (DATA_ROOT / "memory").mkdir(exist_ok=True)
    (DATA_ROOT / "cache").mkdir(exist_ok=True)
    
    if MEMORY_FILE.exists():
        try:
            with open(MEMORY_FILE, "rb") as f:
                _memory_store = pickle.load(f)
        except Exception:
            _memory_store = {}
    
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "rb") as f:
                _cache_store = pickle.load(f)
        except Exception:
            _cache_store = {}


def _persist_memory():
    """Persist memory to disk."""
    with open(MEMORY_FILE, "wb") as f:
        pickle.dump(_memory_store, f)


def _persist_cache():
    """Persist cache to disk."""
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(_cache_store, f)


def remember(key: str, value: Any, metadata: dict = None) -> bool:
    """Store a memory permanently.
    
    Args:
        key: Unique identifier for this memory
        value: The data to store (serializable)
        metadata: Optional context (timestamp, source, tags, etc.)
    
    Returns:
        True if stored successfully
    """
    _ensure_storage()
    
    record = MemoryRecord(
        key=key,
        value=value,
        metadata=metadata or {},
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    _memory_store[key] = record
    _persist_memory()
    
    # Also store in vector DB for semantic search
    try:
        from secondbrain.storage.vector_store import get_store
        store = get_store()
        
        # Create searchable text representation
        text_repr = f"{key}: {json.dumps(value, default=str)}"
        vector = get_embedding(text_repr)
        
        store.upsert(
            collection=store.COLLECTION_KNOWLEDGE,
            id=key,
            vector=vector,
            payload={
                "key": key,
                "value": value,
                "metadata": record.metadata,
                "updated_at": record.updated_at.isoformat()
            }
        )
    except Exception as e:
        # Vector storage is optional - don't fail if Qdrant unavailable
        print(f"Vector storage failed (non-critical): {e}")
    
    return True


def recall(key: str) -> Optional[dict]:
    """Retrieve a memory by exact key.
    
    Args:
        key: The memory's unique identifier
    
    Returns:
        The stored value with metadata, or None
    """
    _ensure_storage()
    
    record = _memory_store.get(key)
    if record is None:
        return None
    
    return {
        "key": record.key,
        "value": record.value,
        "metadata": record.metadata,
        "created_at": record.created_at,
        "updated_at": record.updated_at
    }


def cache_store(query: str, response: str, model: str = "unknown",
                ttl: int = 86400) -> bool:
    """Cache an AI response for cost reduction.
    
    Args:
        query: The original query text
        response: The AI response to cache
        model: Which model generated the response
        ttl: Time-to-live in seconds (default: 24 hours)
    
    Returns:
        True if cached successfully
    """
    _ensure_storage()
    
    query_hash = hash_text(query)
    expires_at = datetime.now() + timedelta(seconds=ttl)
    
    cached = CachedResponse(
        query_hash=query_hash,
        query_text=query[:1000],  # Truncate for storage
        response=response,
        model=model,
        expires_at=expires_at
    )
    
    _cache_store[query_hash] = cached
    _persist_cache()
    
    # Also store in vector DB for similarity search
    try:
        from secondbrain.storage.vector_store import get_store
        store = get_store()
        
        vector = get_embedding(query)
        
        store.upsert(
            collection=store.COLLECTION_QUERIES,
            id=query_hash,
            vector=vector,
            payload={
                "query_text": cached.query_text,
                "response": cached.response,
                "model": cached.model,
                "expires_at": expires_at.isoformat()
            }
        )
    except Exception as e:
        print(f"Vector cache storage failed (non-critical): {e}")
    
    return True


def cache_get(query: str, similarity_threshold: float = 0.90) -> Optional[str]:
    """Retrieve a cached response if similar enough.
    
    Args:
        query: The current query text
        similarity_threshold: Minimum similarity score (0-1)
    
    Returns:
        Cached response if found and valid, else None
    """
    _ensure_storage()
    
    query_hash = hash_text(query)
    
    # First: Check exact match in local cache
    cached = _cache_store.get(query_hash)
    if cached:
        if cached.expires_at and datetime.now() < cached.expires_at:
            cached.hit_count += 1
            _persist_cache()
            return cached.response
        else:
            # Expired - remove it
            del _cache_store[query_hash]
            _persist_cache()
    
    # Second: Check vector similarity in Qdrant
    try:
        from secondbrain.storage.vector_store import get_store
        store = get_store()
        
        query_vector = get_embedding(query)
        results = store.search(
            collection=store.COLLECTION_QUERIES,
            vector=query_vector,
            limit=1,
            threshold=similarity_threshold
        )
        
        if results:
            payload = results[0]["payload"]
            expires_str = payload.get("expires_at")
            
            if expires_str:
                expires = datetime.fromisoformat(expires_str)
                if datetime.now() < expires:
                    return payload.get("response")
    except Exception as e:
        print(f"Vector cache lookup failed (non-critical): {e}")
    
    return None


def get_cache_stats() -> dict:
    """Get cache statistics.
    
    Returns:
        Stats dict with count, hit rate, etc.
    """
    _ensure_storage()
    
    total = len(_cache_store)
    hits = sum(c.hit_count for c in _cache_store.values())
    expired = sum(
        1 for c in _cache_store.values()
        if c.expires_at and datetime.now() > c.expires_at
    )
    
    return {
        "total_cached": total,
        "total_hits": hits,
        "expired_entries": expired,
        "active_entries": total - expired
    }


def search_knowledge(query: str, limit: int = 5) -> list:
    """Search knowledge base by semantic similarity.
    
    Args:
        query: Search query
        limit: Max results
    
    Returns:
        List of matching knowledge entries
    """
    try:
        from secondbrain.storage.vector_store import get_store
        store = get_store()
        
        query_vector = get_embedding(query)
        results = store.search(
            collection=store.COLLECTION_KNOWLEDGE,
            vector=query_vector,
            limit=limit,
            threshold=0.7
        )
        
        return [
            {
                "key": r["payload"].get("key"),
                "value": r["payload"].get("value"),
                "score": r["score"]
            }
            for r in results
        ]
    except Exception as e:
        print(f"Knowledge search failed: {e}")
        return []

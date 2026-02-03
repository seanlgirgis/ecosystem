"""Vector Store

Qdrant integration for similarity search.
"""

import hashlib
from typing import List, Optional, Dict, Any
from pathlib import Path

# Lazy imports - only load when needed
_qdrant_client = None

def _get_qdrant_client():
    global _qdrant_client
    if _qdrant_client is None:
        from qdrant_client import QdrantClient
        _qdrant_client = QdrantClient
    return _qdrant_client


class VectorStore:
    """Qdrant-based vector storage."""
    
    COLLECTION_QUERIES = "queries"
    COLLECTION_DOCUMENTS = "documents"
    COLLECTION_KNOWLEDGE = "knowledge"
    
    # Embedding dimension (using all-MiniLM-L6-v2 = 384)
    VECTOR_SIZE = 384
    
    def __init__(self, host: str = "localhost", port: int = 6333):
        self.host = host
        self.port = port
        self._client = None
    
    def connect(self) -> bool:
        """Establish connection to Qdrant."""
        try:
            QdrantClient = _get_qdrant_client()
            self._client = QdrantClient(host=self.host, port=self.port)
            self._ensure_collections()
            return True
        except Exception as e:
            print(f"Failed to connect to Qdrant: {e}")
            return False
    
    def _ensure_collections(self) -> None:
        """Create collections if they don't exist."""
        from qdrant_client.models import Distance, VectorParams
        
        collections = [
            self.COLLECTION_QUERIES,
            self.COLLECTION_DOCUMENTS,
            self.COLLECTION_KNOWLEDGE
        ]
        
        for collection in collections:
            try:
                self._client.get_collection(collection)
            except Exception:
                self._client.create_collection(
                    collection_name=collection,
                    vectors_config=VectorParams(
                        size=self.VECTOR_SIZE,
                        distance=Distance.COSINE
                    )
                )
    
    def upsert(self, collection: str, id: str, vector: List[float],
               payload: Dict[str, Any]) -> bool:
        """Store a vector with metadata."""
        if self._client is None:
            if not self.connect():
                return False
        
        try:
            from qdrant_client.models import PointStruct
            self._client.upsert(
                collection_name=collection,
                points=[PointStruct(id=id, vector=vector, payload=payload)]
            )
            return True
        except Exception as e:
            print(f"Failed to upsert: {e}")
            return False
    
    def search(self, collection: str, vector: List[float],
               limit: int = 5, threshold: float = 0.0) -> List[dict]:
        """Search for similar vectors."""
        if self._client is None:
            if not self.connect():
                return []
        
        try:
            results = self._client.search(
                collection_name=collection,
                query_vector=vector,
                limit=limit,
                score_threshold=threshold
            )
            return [
                {
                    "id": r.id,
                    "score": r.score,
                    "payload": r.payload
                }
                for r in results
            ]
        except Exception as e:
            print(f"Search failed: {e}")
            return []
    
    def delete(self, collection: str, id: str) -> bool:
        """Delete a vector by ID."""
        if self._client is None:
            return False
        
        try:
            from qdrant_client.models import PointIdsList
            self._client.delete(
                collection_name=collection,
                points_selector=PointIdsList(points=[id])
            )
            return True
        except Exception as e:
            print(f"Delete failed: {e}")
            return False


# Global instance
_store: Optional[VectorStore] = None


def get_store() -> VectorStore:
    """Get or create the global vector store."""
    global _store
    if _store is None:
        _store = VectorStore()
    return _store

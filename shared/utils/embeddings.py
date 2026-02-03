"""Embedding utilities

Generate embeddings using local Ollama (no external API calls).
"""

import hashlib
from typing import List, Optional

# Cache for embeddings to avoid recomputation
_embedding_cache: dict = {}

def get_embedding(text: str, model: str = "nomic-embed-text") -> List[float]:
    """Generate embedding using Ollama.
    
    Args:
        text: Text to embed
        model: Ollama embedding model
    
    Returns:
        Embedding vector
    """
    import requests
    
    # Check cache
    cache_key = hashlib.md5(f"{model}:{text}".encode()).hexdigest()
    if cache_key in _embedding_cache:
        return _embedding_cache[cache_key]
    
    try:
        response = requests.post(
            "http://localhost:11434/api/embeddings",
            json={"model": model, "prompt": text}
        )
        response.raise_for_status()
        embedding = response.json()["embedding"]
        
        # Cache result
        _embedding_cache[cache_key] = embedding
        return embedding
    except Exception as e:
        print(f"Embedding generation failed: {e}")
        # Return zero vector as fallback
        return [0.0] * 384


def hash_text(text: str) -> str:
    """Generate hash for text lookup."""
    return hashlib.sha256(text.encode()).hexdigest()[:16]

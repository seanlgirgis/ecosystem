"""Chat Logger

Captures Kimi/Claude/ChatGPT interactions for caching and analysis.
"""

import json
import pickle
from datetime import datetime
from pathlib import Path
from typing import Optional, List

from shared.utils.embeddings import hash_text, get_embedding
from secondbrain.api.memory import cache_store, cache_get, remember

# Storage - SEPARATE FROM CODE (gitignored)
DATA_ROOT = Path("C:/ecosystem/data")
STORAGE_ROOT = Path("C:/ecosystem/secondbrain/storage")
CONVERSATIONS_FILE = DATA_ROOT / "memory" / "conversations.pkl"

# In-memory conversations
_conversations: List[dict] = []


def _ensure_storage():
    """Ensure storage directory exists and load persisted data."""
    global _conversations
    
    # Create data directories (gitignored, separate from code)
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    (DATA_ROOT / "memory").mkdir(exist_ok=True)
    
    if CONVERSATIONS_FILE.exists():
        try:
            with open(CONVERSATIONS_FILE, "rb") as f:
                _conversations = pickle.load(f)
        except Exception:
            _conversations = []


def _persist_conversations():
    """Persist conversations to disk."""
    with open(CONVERSATIONS_FILE, "wb") as f:
        pickle.dump(_conversations, f)


class ChatLogger:
    """Logs AI conversations for caching and cost tracking."""
    
    def __init__(self, storage_path: str = None):
        self.storage_path = storage_path or str(STORAGE_ROOT)
        _ensure_storage()
    
    def log(self, query: str, response: str, model: str, 
            cost: float = 0.0, cached: bool = False) -> str:
        """Log a conversation exchange.
        
        Args:
            query: The user's prompt
            response: The AI's response
            model: Which model was used
            cost: API cost in USD
            cached: Whether this was a cache hit
        
        Returns:
            Record ID of the logged entry
        """
        record_id = hash_text(f"{datetime.now().isoformat()}:{query[:50]}")
        
        record = {
            "id": record_id,
            "timestamp": datetime.now(),
            "query": query,
            "query_hash": hash_text(query),
            "response": response,
            "model": model,
            "cost": 0.0 if cached else cost,
            "cached": cached
        }
        
        _conversations.append(record)
        _persist_conversations()
        
        # Store in SecondBrain memory for long-term reference
        remember(
            key=f"conversation:{record_id}",
            value={
                "query": query[:500],
                "response": response[:1000],
                "model": model
            },
            metadata={
                "type": "conversation",
                "model": model,
                "has_cost": cost > 0
            }
        )
        
        return record_id
    
    def find_similar(self, query: str, 
                     threshold: float = 0.90) -> Optional[dict]:
        """Find a similar cached conversation.
        
        Args:
            query: The current query
            threshold: Minimum similarity (0-1)
        
        Returns:
            Cached entry if found, else None
        """
        return cache_get(query, similarity_threshold=threshold)
    
    def get_stats(self, days: int = 30) -> dict:
        """Get conversation statistics.
        
        Args:
            days: Lookback period
        
        Returns:
            Stats dict
        """
        from datetime import timedelta
        
        cutoff = datetime.now() - timedelta(days=days)
        recent = [c for c in _conversations if c["timestamp"] > cutoff]
        
        total_cost = sum(c["cost"] for c in recent)
        cached_count = sum(1 for c in recent if c["cached"])
        total_count = len(recent)
        
        # Cost savings from caching
        avg_cost_per_call = total_cost / max(total_count - cached_count, 1)
        savings = cached_count * avg_cost_per_call
        
        return {
            "period_days": days,
            "total_conversations": total_count,
            "cached_responses": cached_count,
            "api_calls": total_count - cached_count,
            "total_cost_usd": round(total_cost, 4),
            "estimated_savings_usd": round(savings, 4),
            "cache_hit_rate": round(cached_count / max(total_count, 1), 2),
            "by_model": self._breakdown_by_model(recent)
        }
    
    def _breakdown_by_model(self, conversations: List[dict]) -> dict:
        """Breakdown stats by model."""
        breakdown = {}
        for c in conversations:
            model = c["model"]
            if model not in breakdown:
                breakdown[model] = {"count": 0, "cost": 0.0}
            breakdown[model]["count"] += 1
            breakdown[model]["cost"] += c["cost"]
        return breakdown


# Global instance
_logger: Optional[ChatLogger] = None


def get_logger() -> ChatLogger:
    """Get or create the global chat logger."""
    global _logger
    if _logger is None:
        _logger = ChatLogger()
    return _logger


def log_interaction(query: str, response: str, model: str, 
                    cost: float = 0.0) -> str:
    """Convenience function to log an interaction."""
    logger = get_logger()
    return logger.log(query, response, model, cost)

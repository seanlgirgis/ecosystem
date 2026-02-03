"""SecondBrain — Immortal Knowledge Layer

Store knowledge, cache API responses, remember everything.

Public API:
    from secondbrain import remember, recall, cache_store, cache_get
    from secondbrain import search_knowledge, get_cache_stats
    from secondbrain import log_interaction
"""

from .api import (
    remember, 
    recall, 
    cache_store, 
    cache_get,
    search_knowledge,
    get_cache_stats
)
from .ingest import log_interaction

__version__ = "1.0.0"
__all__ = [
    "remember", 
    "recall", 
    "cache_store", 
    "cache_get",
    "search_knowledge",
    "get_cache_stats",
    "log_interaction"
]

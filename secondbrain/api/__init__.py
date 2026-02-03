"""SecondBrain API

Public interface: remember(), recall(), cache_store(), cache_get(),
search_knowledge(), get_cache_stats()
"""

from .memory import (
    remember, 
    recall, 
    cache_store, 
    cache_get,
    search_knowledge,
    get_cache_stats
)

__all__ = [
    "remember", 
    "recall", 
    "cache_store", 
    "cache_get",
    "search_knowledge",
    "get_cache_stats"
]

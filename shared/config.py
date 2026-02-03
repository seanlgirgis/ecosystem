"""Unified Configuration

Central configuration for all components.

Loads from:
1. Environment variables
2. .env file
3. Default values

Usage:
    >>> from shared.config import Config
    >>> cfg = Config()
    >>> cfg.qdrant_host
    'localhost'
"""

import os
from pathlib import Path
from typing import Optional


class Config:
    """Application configuration."""
    
    # Paths
    PROJECT_ROOT: Path = Path("C:/ecosystem")
    STORAGE_PATH: Path = Path("C:/ecosystem/secondbrain/storage")
    
    # Qdrant
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_GRPC_PORT: int = 6334
    
    # Ollama
    OLLAMA_HOST: str = "http://localhost:11434"
    
    # Models
    LOCAL_REASONING_MODEL: str = "qwen2.5:32b-instruct"
    LOCAL_FAST_MODEL: str = "llama3.1:8b-instruct"
    LOCAL_LIGHT_MODEL: str = "phi3:mini"
    
    # API Keys (load from env)
    OPENROUTER_API_KEY: Optional[str] = None
    UPWORK_API_KEY: Optional[str] = None
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    
    # Feature Flags
    ENABLE_TELEGRAM: bool = True
    ENABLE_CACHING: bool = True
    CACHE_SIMILARITY_THRESHOLD: float = 0.90
    
    def __init__(self):
        """Load configuration from environment."""
        self._load_from_env()
    
    def _load_from_env(self) -> None:
        """Override defaults with environment variables."""
        self.QDRANT_HOST = os.getenv("QDRANT_HOST", self.QDRANT_HOST)
        self.QDRANT_PORT = int(os.getenv("QDRANT_PORT", self.QDRANT_PORT))
        self.OLLAMA_HOST = os.getenv("OLLAMA_HOST", self.OLLAMA_HOST)
        
        self.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
        self.UPWORK_API_KEY = os.getenv("UPWORK_API_KEY")
        self.TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
        
        self.ENABLE_TELEGRAM = os.getenv("ENABLE_TELEGRAM", "true").lower() == "true"
        self.ENABLE_CACHING = os.getenv("ENABLE_CACHING", "true").lower() == "true"
        self.CACHE_SIMILARITY_THRESHOLD = float(
            os.getenv("CACHE_SIMILARITY_THRESHOLD", "0.90")
        )


# Global instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get or create global config."""
    global _config
    if _config is None:
        _config = Config()
    return _config

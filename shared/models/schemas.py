"""Pydantic Schemas

Shared data models used across components.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum

# Using dataclasses for simplicity (can migrate to Pydantic later)
from dataclasses import dataclass, field


class MessageRole(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class ChatMessage:
    """Single chat message."""
    role: MessageRole
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Conversation:
    """Full conversation thread."""
    id: str
    messages: List[ChatMessage] = field(default_factory=list)
    model: str = "unknown"
    total_tokens: int = 0
    cost_usd: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class MemoryRecord:
    """Stored memory in SecondBrain."""
    key: str
    value: Any
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class CachedResponse:
    """Cached AI response."""
    query_hash: str
    query_text: str
    response: str
    model: str
    similarity_hash: Optional[str] = None
    hit_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None


@dataclass
class VectorDocument:
    """Document stored in vector DB."""
    id: str
    collection: str
    vector: List[float]
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class SkillResult:
    """Result from skill execution."""
    success: bool
    skill: str
    action: str
    data: Any = None
    error: Optional[str] = None
    execution_time_ms: int = 0

"""ClawBot Core

Bot framework and skill registry.
"""

from .bot import ClawBot
from .skill_registry import SkillRegistry, get_registry

__all__ = ["ClawBot", "SkillRegistry", "get_registry"]

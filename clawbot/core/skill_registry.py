"""Skill Registry

Manages swappable skills. Skills are self-contained packages that add
capabilities to ClawBot.

A skill is a Python package with:
- __init__.py (exports Skill class)
- skill.py (main implementation)
- config.yaml (skill configuration)
- tests/ (unit tests)

Skills discover themselves automatically when placed in clawbot/skills/.
"""

import importlib
from pathlib import Path
from typing import Dict, Any, Optional, List, Type


class SkillRegistry:
    """Registry for ClawBot skills."""
    
    SKILLS_PATH = Path(__file__).parent.parent / "skills"
    
    def __init__(self):
        """Initialize registry."""
        self._skills: Dict[str, Any] = {}
        self._discover_skills()
    
    def _discover_skills(self) -> None:
        """Auto-discover available skills from filesystem."""
        if not self.SKILLS_PATH.exists():
            return
        
        for skill_dir in self.SKILLS_PATH.iterdir():
            if skill_dir.is_dir() and not skill_dir.name.startswith("_"):
                # Found potential skill
                pass  # TODO: Implement discovery
    
    def list_available(self) -> List[str]:
        """List all available skills.
        
        Returns:
            List of skill names
        """
        raise NotImplementedError("Stage 7 implementation pending")
    
    def load(self, skill_name: str) -> Any:
        """Load and instantiate a skill.
        
        Args:
            skill_name: Name of skill to load
        
        Returns:
            Skill instance
        """
        raise NotImplementedError("Stage 7 implementation pending")
    
    def get_metadata(self, skill_name: str) -> dict:
        """Get skill metadata (name, version, description, dependencies).
        
        Args:
            skill_name: Skill to query
        
        Returns:
            Metadata dictionary
        """
        raise NotImplementedError("Stage 7 implementation pending")


# Global instance
_registry: Optional[SkillRegistry] = None


def get_registry() -> SkillRegistry:
    """Get or create the global skill registry."""
    global _registry
    if _registry is None:
        _registry = SkillRegistry()
    return _registry

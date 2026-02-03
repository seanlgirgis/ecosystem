"""ClawBot — Skill Executor (AI Employee)

Execute skills, take actions, interface with user.

Usage:
    from clawbot import ClawBot
    bot = ClawBot()
    bot.load_skill("environment")
"""

from .core import ClawBot

__version__ = "1.0.0"
__all__ = ["ClawBot"]

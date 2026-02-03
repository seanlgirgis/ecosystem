"""Lead Generation Skills

Upwork and LinkedIn lead generation.
"""

from .upwork import UpworkLeadGenSkill, UpworkJob
from .linkedin import LinkedInLeadGenSkill, LinkedInJob

__all__ = [
    "UpworkLeadGenSkill", "UpworkJob",
    "LinkedInLeadGenSkill", "LinkedInJob"
]

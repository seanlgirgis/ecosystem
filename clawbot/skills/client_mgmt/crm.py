"""Client CRM

Track clients, proposals, interactions.

Simple but effective client management for freelance business.

Entities:
- Client: Company/person information
- Project: Work engagements
- Proposal: Quotes sent
- Interaction: Calls, emails, meetings
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ProjectStatus(Enum):
    LEAD = "lead"
    PROPOSAL_SENT = "proposal_sent"
    NEGOTIATING = "negotiating"
    ACTIVE = "active"
    COMPLETED = "completed"
    LOST = "lost"


@dataclass
class Client:
    """Client entity."""
    id: str
    name: str
    contact_name: str
    email: str
    phone: Optional[str] = None
    company: Optional[str] = None
    website: Optional[str] = None
    notes: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)


@dataclass
class Project:
    """Project entity."""
    id: str
    client_id: str
    name: str
    description: str
    status: ProjectStatus
    budget: Optional[float] = None
    hourly_rate: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Proposal:
    """Proposal/quote entity."""
    id: str
    client_id: str
    project_name: str
    amount: float
    description: str
    sent_date: datetime
    status: str  # sent, accepted, rejected, expired
    valid_until: Optional[datetime] = None


class CRMSkill:
    """Client relationship management skill."""
    
    SKILL_NAME = "client_mgmt"
    SKILL_VERSION = "1.0.0"
    
    def __init__(self, brain_api=None):
        """Initialize skill.
        
        Args:
            brain_api: SecondBrain API for persistence
        """
        self.brain = brain_api
    
    def add_client(self, client: Client) -> bool:
        """Add new client to CRM.
        
        Args:
            client: Client to add
        
        Returns:
            True if added
        """
        raise NotImplementedError("Stage 7 implementation pending")
    
    def get_client(self, client_id: str) -> Optional[Client]:
        """Get client by ID.
        
        Args:
            client_id: Client identifier
        
        Returns:
            Client or None
        """
        raise NotImplementedError("Stage 7 implementation pending")
    
    def list_clients(self, tags: List[str] = None) -> List[Client]:
        """List clients, optionally filtered by tags.
        
        Args:
            tags: Filter by tags
        
        Returns:
            List of clients
        """
        raise NotImplementedError("Stage 7 implementation pending")
    
    def create_project(self, project: Project) -> bool:
        """Create new project.
        
        Args:
            project: Project to create
        
        Returns:
            True if created
        """
        raise NotImplementedError("Stage 7 implementation pending")
    
    def generate_proposal(self, client_id: str, project_description: str,
                          similar_projects: int = 3) -> Proposal:
        """Generate proposal based on similar past projects.
        
        Args:
            client_id: Target client
            project_description: What they need
            similar_projects: How many past projects to reference
        
        Returns:
            Generated proposal
        """
        raise NotImplementedError("Stage 7 implementation pending")
    
    def get_pipeline(self) -> Dict[ProjectStatus, List[Project]]:
        """Get all projects grouped by status.
        
        Returns:
            Pipeline dict
        """
        raise NotImplementedError("Stage 7 implementation pending")

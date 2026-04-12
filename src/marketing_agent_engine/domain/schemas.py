"""
Base Pydantic schemas for the Marketing Agent Engine domain layer.
All domain models inherit from these base types.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, computed_field


class ClusterSlug(str, Enum):
    SHK_E = "SHK+E"
    DACH_UND_HOLZ = "Dach_und_Holz"
    BAUGEWERBE = "Baugewerbe"
    UNBEKANNT = "unbekannt"


class SkillDomain(str, Enum):
    CONTENT_CREATION = "content_creation"
    SEO = "seo"
    SOCIAL_MEDIA = "social_media"
    EMAIL_MARKETING = "email_marketing"
    PAID_ADS = "paid_ads"
    ANALYTICS = "analytics"
    DESIGN = "design"
    COPYWRITING = "copywriting"
    PROJECT_MANAGEMENT = "project_management"
    STRATEGY = "strategy"
    TECHNICAL = "technical"
    UNKNOWN = "unknown"


class AIReadiness(str, Enum):
    PIONEER = "AI-Pioneer"    # Level 4 — Prompt-Engineering, AI-Tools produktiv
    EXPERIENCED = "AI-Erfahren"  # Level 3 — regelmäßige AI-Nutzung
    READY = "AI-Bereit"      # Level 2 — gelegentliche AI-Nutzung
    NOVICE = "AI-Novice"     # Level 1 — wenig/keine AI-Erfahrung

    @property
    def level(self) -> int:
        return {
            AIReadiness.PIONEER: 4,
            AIReadiness.EXPERIENCED: 3,
            AIReadiness.READY: 2,
            AIReadiness.NOVICE: 1,
        }[self]

    def meets(self, required: "AIReadiness") -> bool:
        """Returns True if this readiness level meets or exceeds the required level."""
        return self.level >= required.level


class TaskCategory(str, Enum):
    WORDPRESS = "WordPress/Webmaster"
    HUBSPOT = "HubSpot/Marketing-Automation"
    PRINT_GRAPHIC = "Print/Graphic"
    SOCIAL_MEDIA = "Social-Media"
    EVENT_MESSE = "Event/Messe"
    SEO_CONTENT = "SEO/Content-Strategie"
    INTERNAL_COMM = "Interne Kommunikation"
    COORDINATION = "Koordination/Projektmanagement"
    LANDING_PAGES = "Landing-Pages/Design"
    CAMPAIGN_EMAIL = "Kampagne/Email-Marketing"
    OTHER = "Other"


class AssigneeRecommendation(BaseModel):
    employee_id: str
    display_name: str
    confidence: float = Field(ge=0.0, le=1.0)
    matched_skills: list[str] = Field(default_factory=list)
    reason: str = ""
    ai_readiness: Optional[str] = None


class PlausibilityVerdict(str, Enum):
    PLAUSIBLE = "plausible"
    QUESTIONABLE = "questionable"
    IMPLAUSIBLE = "implausible"
    UNKNOWN = "unknown"


class AssigneePlausibilityResult(BaseModel):
    verdict: PlausibilityVerdict
    employee_id: Optional[str] = None
    display_name: Optional[str] = None
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    explanation: str = ""
    ai_readiness: Optional[str] = None
    human_review_required: bool = False


class CompletenessFlag(BaseModel):
    criterion: str
    passed: bool
    value: Optional[Any] = None
    note: str = ""


class CompletenessResult(BaseModel):
    score: float = Field(ge=0.0, le=1.0)
    flags: list[CompletenessFlag] = Field(default_factory=list)
    missing: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

    @computed_field  # type: ignore[misc]
    @property
    def passed(self) -> bool:
        return self.score >= 0.8


class BusinessUnitMatch(BaseModel):
    slug: str
    display_name: str
    cluster: ClusterSlug
    confidence: float = Field(ge=0.0, le=1.0)
    matched_by: str = ""


class RoutingResult(BaseModel):
    business_unit: Optional[BusinessUnitMatch] = None
    cluster: ClusterSlug = ClusterSlug.UNBEKANNT
    cluster_coordinator_id: Optional[str] = None
    confidence: float = Field(ge=0.0, le=1.0)
    resolution_path: list[str] = Field(default_factory=list)

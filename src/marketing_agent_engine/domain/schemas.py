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


class AssigneeRecommendation(BaseModel):
    employee_id: str
    display_name: str
    confidence: float = Field(ge=0.0, le=1.0)
    matched_skills: list[str] = Field(default_factory=list)
    reason: str = ""


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

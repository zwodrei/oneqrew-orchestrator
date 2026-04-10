"""
Employee data, skill matrix, and employee domain models.

All employee records are sourced from internal HR data.
Employee IDs match Asana user GIDs where applicable.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from .schemas import SkillDomain


class Employee(BaseModel):
    employee_id: str
    display_name: str
    email: str
    asana_gid: Optional[str] = None
    cluster_slugs: list[str] = Field(default_factory=list)
    business_unit_slugs: list[str] = Field(default_factory=list)
    skill_domains: list[SkillDomain] = Field(default_factory=list)
    skill_tags: list[str] = Field(default_factory=list)
    is_coordinator: bool = False
    is_active: bool = True
    notes: str = ""


# ---------------------------------------------------------------------------
# Employee registry
# ---------------------------------------------------------------------------

EMPLOYEES: list[Employee] = [
    Employee(
        employee_id="emp_001",
        display_name="Anna Müller",
        email="a.mueller@example.com",
        cluster_slugs=["SHK+E"],
        business_unit_slugs=["shk_heizung", "shk_sanitaer"],
        skill_domains=[
            SkillDomain.CONTENT_CREATION,
            SkillDomain.COPYWRITING,
            SkillDomain.SEO,
        ],
        skill_tags=["blog", "landingpage", "produkttext", "seo-onpage"],
        is_coordinator=False,
        is_active=True,
    ),
    Employee(
        employee_id="emp_002",
        display_name="Ben Schmidt",
        email="b.schmidt@example.com",
        cluster_slugs=["SHK+E"],
        business_unit_slugs=["shk_elektro", "shk_klima"],
        skill_domains=[
            SkillDomain.SOCIAL_MEDIA,
            SkillDomain.PAID_ADS,
            SkillDomain.ANALYTICS,
        ],
        skill_tags=["instagram", "facebook-ads", "google-ads", "tracking"],
        is_coordinator=True,
        is_active=True,
        notes="SHK+E cluster coordinator",
    ),
    Employee(
        employee_id="emp_003",
        display_name="Clara Weber",
        email="c.weber@example.com",
        cluster_slugs=["Dach_und_Holz"],
        business_unit_slugs=["dach_ziegel", "dach_flachdach", "holzbau"],
        skill_domains=[
            SkillDomain.CONTENT_CREATION,
            SkillDomain.EMAIL_MARKETING,
            SkillDomain.DESIGN,
        ],
        skill_tags=["newsletter", "email-kampagne", "canva", "bildbearbeitung"],
        is_coordinator=False,
        is_active=True,
    ),
    Employee(
        employee_id="emp_004",
        display_name="David Klein",
        email="d.klein@example.com",
        cluster_slugs=["Dach_und_Holz"],
        business_unit_slugs=["dach_ziegel", "holzbau", "dach_abdichtung"],
        skill_domains=[
            SkillDomain.SEO,
            SkillDomain.ANALYTICS,
            SkillDomain.TECHNICAL,
        ],
        skill_tags=["seo-onpage", "seo-offpage", "google-analytics", "search-console"],
        is_coordinator=True,
        is_active=True,
        notes="Dach_und_Holz cluster coordinator",
    ),
    Employee(
        employee_id="emp_005",
        display_name="Eva Braun",
        email="e.braun@example.com",
        cluster_slugs=["Baugewerbe"],
        business_unit_slugs=["bau_rohbau", "bau_ausbau", "bau_tiefbau"],
        skill_domains=[
            SkillDomain.PROJECT_MANAGEMENT,
            SkillDomain.STRATEGY,
            SkillDomain.COPYWRITING,
        ],
        skill_tags=["kampagnenplanung", "briefing", "redaktionsplan", "texterstellung"],
        is_coordinator=True,
        is_active=True,
        notes="Baugewerbe cluster coordinator",
    ),
    Employee(
        employee_id="emp_006",
        display_name="Felix Hoffmann",
        email="f.hoffmann@example.com",
        cluster_slugs=["Baugewerbe"],
        business_unit_slugs=["bau_ausbau", "bau_malerarbeiten"],
        skill_domains=[
            SkillDomain.DESIGN,
            SkillDomain.SOCIAL_MEDIA,
            SkillDomain.CONTENT_CREATION,
        ],
        skill_tags=["grafik", "instagram", "tiktok", "video", "reel"],
        is_coordinator=False,
        is_active=True,
    ),
    Employee(
        employee_id="emp_007",
        display_name="Greta Fischer",
        email="g.fischer@example.com",
        cluster_slugs=["SHK+E", "Dach_und_Holz", "Baugewerbe"],
        business_unit_slugs=[],
        skill_domains=[
            SkillDomain.STRATEGY,
            SkillDomain.ANALYTICS,
            SkillDomain.PROJECT_MANAGEMENT,
        ],
        skill_tags=["jahresplanung", "reporting", "kpi", "budget", "koordination"],
        is_coordinator=False,
        is_active=True,
        notes="Cross-cluster strategist and analyst",
    ),
]

# Lookup maps built at module load time for O(1) access
_BY_ID: dict[str, Employee] = {e.employee_id: e for e in EMPLOYEES}
_BY_EMAIL: dict[str, Employee] = {e.email.lower(): e for e in EMPLOYEES}
_BY_ASANA_GID: dict[str, Employee] = {
    e.asana_gid: e for e in EMPLOYEES if e.asana_gid
}


def get_employee_by_id(employee_id: str) -> Optional[Employee]:
    return _BY_ID.get(employee_id)


def get_employee_by_email(email: str) -> Optional[Employee]:
    return _BY_EMAIL.get(email.lower())


def get_employee_by_asana_gid(gid: str) -> Optional[Employee]:
    return _BY_ASANA_GID.get(gid)


def get_active_employees() -> list[Employee]:
    return [e for e in EMPLOYEES if e.is_active]


def get_employees_by_cluster(cluster_slug: str) -> list[Employee]:
    return [e for e in EMPLOYEES if cluster_slug in e.cluster_slugs and e.is_active]


def get_coordinator_for_cluster(cluster_slug: str) -> Optional[Employee]:
    for e in EMPLOYEES:
        if e.is_coordinator and cluster_slug in e.cluster_slugs and e.is_active:
            return e
    return None

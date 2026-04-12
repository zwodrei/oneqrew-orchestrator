"""
Employee data, skill matrix, and employee domain models.

Real team members of the Marketing team.
Employee IDs match internal identifiers.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from .schemas import AIReadiness, SkillDomain


class Employee(BaseModel):
    employee_id: str
    display_name: str
    email: str
    asana_gid: Optional[str] = None
    cluster_slugs: list[str] = Field(default_factory=list)
    business_unit_slugs: list[str] = Field(default_factory=list)
    skill_domains: list[SkillDomain] = Field(default_factory=list)
    skill_tags: list[str] = Field(default_factory=list)
    ai_readiness: AIReadiness = AIReadiness.READY
    is_coordinator: bool = False
    is_active: bool = True
    notes: str = ""


# ---------------------------------------------------------------------------
# Employee registry — 14 real team members
# ---------------------------------------------------------------------------

EMPLOYEES: list[Employee] = [
    Employee(
        employee_id="emp_001",
        display_name="Maren Hoyer",
        email="m.hoyer@example.com",
        cluster_slugs=["SHK+E"],
        skill_domains=[
            SkillDomain.EMAIL_MARKETING,
            SkillDomain.CONTENT_CREATION,
            SkillDomain.PROJECT_MANAGEMENT,
        ],
        skill_tags=["kampagnen", "einladungen", "messe-partnerschaften", "landing-pages", "kampagnen-koordination"],
        ai_readiness=AIReadiness.READY,
        is_coordinator=True,
        notes="Marketing-Business-Partnerin SHK+E. Koordiniert Kampagnen, Messe-Einladungen und Landing-Pages.",
    ),
    Employee(
        employee_id="emp_002",
        display_name="Sara Niklassik",
        email="s.niklassik@example.com",
        cluster_slugs=["Dach_und_Holz"],
        skill_domains=[
            SkillDomain.PROJECT_MANAGEMENT,
            SkillDomain.EMAIL_MARKETING,
            SkillDomain.CONTENT_CREATION,
        ],
        skill_tags=["referenzen", "schulungen", "termine", "partnerschaften", "messe-organisation"],
        ai_readiness=AIReadiness.READY,
        is_coordinator=True,
        notes="Marketing-Business-Partnerin Dach & Holz. Koordiniert Schulungen, Partnerschaften und Messen.",
    ),
    Employee(
        employee_id="emp_003",
        display_name="Matteo Diehl",
        email="m.diehl@example.com",
        cluster_slugs=["SHK+E", "Dach_und_Holz", "Baugewerbe"],
        skill_domains=[
            SkillDomain.EMAIL_MARKETING,
            SkillDomain.TECHNICAL,
            SkillDomain.ANALYTICS,
        ],
        skill_tags=["hubspot", "webhook", "automation", "double-opt-in", "kontaktformular", "redirect"],
        ai_readiness=AIReadiness.EXPERIENCED,
        is_coordinator=False,
        notes="HubSpot-Spezialist. Primäransprechpartner für alle Automation-Aufgaben.",
    ),
    Employee(
        employee_id="emp_004",
        display_name="Finja Witt",
        email="f.witt@example.com",
        cluster_slugs=["SHK+E", "Dach_und_Holz", "Baugewerbe"],
        skill_domains=[
            SkillDomain.DESIGN,
            SkillDomain.EMAIL_MARKETING,
            SkillDomain.PAID_ADS,
        ],
        skill_tags=["landing-page", "layout", "grafik", "sea", "mailing", "banner"],
        ai_readiness=AIReadiness.READY,
        is_coordinator=False,
        notes="Grafikdesignerin & Junior Marketing-Automation. Landing-Pages und Design-Assets.",
    ),
    Employee(
        employee_id="emp_005",
        display_name="Ines Müller",
        email="i.mueller@example.com",
        cluster_slugs=["SHK+E", "Dach_und_Holz", "Baugewerbe"],
        skill_domains=[
            SkillDomain.DESIGN,
            SkillDomain.CONTENT_CREATION,
            SkillDomain.EMAIL_MARKETING,
        ],
        skill_tags=["landing-page", "produktseite", "subscription", "event-grafik", "hubspot"],
        ai_readiness=AIReadiness.READY,
        is_coordinator=False,
        notes="Grafikdesignerin & Landing-Page-Creator. Pflegt Landing-Pages und Produktseiten.",
    ),
    Employee(
        employee_id="emp_006",
        display_name="Laura Piccolomo",
        email="l.piccolomo@example.com",
        cluster_slugs=["SHK+E", "Dach_und_Holz", "Baugewerbe"],
        skill_domains=[
            SkillDomain.SEO,
            SkillDomain.CONTENT_CREATION,
            SkillDomain.COPYWRITING,
            SkillDomain.STRATEGY,
        ],
        skill_tags=["seo", "keyword-recherche", "content-strategie", "custom-gpt", "ai-texte"],
        ai_readiness=AIReadiness.EXPERIENCED,
        is_coordinator=False,
        notes="Senior SEO & Content-Strategist. Nutzt Custom-GPT für Textproduktion.",
    ),
    Employee(
        employee_id="emp_007",
        display_name="Lina Weiß",
        email="l.weiss@example.com",
        cluster_slugs=["SHK+E", "Dach_und_Holz", "Baugewerbe"],
        skill_domains=[
            SkillDomain.DESIGN,
            SkillDomain.COPYWRITING,
        ],
        skill_tags=["print", "logo", "e-mail-signatur", "messe-grafik", "qrewnet", "print-leitfaden"],
        ai_readiness=AIReadiness.NOVICE,
        is_coordinator=False,
        notes="Grafikdesignerin Print-Design. AI-Novice — human_review_required bei AI-Tasks.",
    ),
    Employee(
        employee_id="emp_008",
        display_name="Sandra Hoppe",
        email="s.hoppe@example.com",
        cluster_slugs=["SHK+E", "Dach_und_Holz", "Baugewerbe"],
        skill_domains=[
            SkillDomain.DESIGN,
            SkillDomain.TECHNICAL,
            SkillDomain.CONTENT_CREATION,
            SkillDomain.STRATEGY,
        ],
        skill_tags=["ui-ux", "prompt-engineering", "ai-tools", "fotografie", "stock", "full-stack-design", "skript"],
        ai_readiness=AIReadiness.PIONEER,
        is_coordinator=False,
        notes="Senior Full-Stack-Marketing-Designerin & AI-Pioneer. Bevorzugt für AI-intensive Design-Aufgaben.",
    ),
    Employee(
        employee_id="emp_009",
        display_name="André Köhler",
        email="a.koehler@example.com",
        cluster_slugs=["SHK+E", "Dach_und_Holz", "Baugewerbe"],
        skill_domains=[
            SkillDomain.PROJECT_MANAGEMENT,
        ],
        skill_tags=["messe", "event", "tickets", "debriefing", "budget", "logistik"],
        ai_readiness=AIReadiness.NOVICE,
        is_coordinator=False,
        notes="Messe- & Eventmanager. AI-Novice — human_review_required bei AI-Tasks.",
    ),
    Employee(
        employee_id="emp_010",
        display_name="Christina Helms",
        email="c.helms@example.com",
        cluster_slugs=["SHK+E", "Dach_und_Holz", "Baugewerbe"],
        skill_domains=[
            SkillDomain.PROJECT_MANAGEMENT,
        ],
        skill_tags=["networking", "event", "speaker", "raumausstattung", "technik", "messe"],
        ai_readiness=AIReadiness.NOVICE,
        is_coordinator=False,
        notes="Messe- & Eventmanagerin. AI-Novice — human_review_required bei AI-Tasks.",
    ),
    Employee(
        employee_id="emp_011",
        display_name="Madelin Grohmann",
        email="m.grohmann@example.com",
        cluster_slugs=["SHK+E", "Dach_und_Holz", "Baugewerbe"],
        skill_domains=[
            SkillDomain.SOCIAL_MEDIA,
            SkillDomain.CONTENT_CREATION,
            SkillDomain.EMAIL_MARKETING,
        ],
        skill_tags=["social-media", "instagram", "linkedin", "ugc", "messe-beiträge", "hubspot"],
        ai_readiness=AIReadiness.READY,
        is_coordinator=False,
        notes="Social-Media-Managerin & Content-Creator. Primäransprechpartnerin für Social-Media.",
    ),
    Employee(
        employee_id="emp_012",
        display_name="Janosch Niemeyer",
        email="j.niemeyer@example.com",
        cluster_slugs=["SHK+E", "Dach_und_Holz", "Baugewerbe"],
        skill_domains=[
            SkillDomain.TECHNICAL,
            SkillDomain.CONTENT_CREATION,
        ],
        skill_tags=["wordpress", "plugin", "wpforms", "blog", "landing-page-template", "filter", "php"],
        ai_readiness=AIReadiness.READY,
        is_coordinator=False,
        notes="Webmaster & WordPress-Dev. Primäransprechpartner für WordPress-Aufgaben.",
    ),
    Employee(
        employee_id="emp_013",
        display_name="Susanne Arasin",
        email="s.arasin@example.com",
        cluster_slugs=["SHK+E", "Dach_und_Holz", "Baugewerbe"],
        skill_domains=[
            SkillDomain.CONTENT_CREATION,
            SkillDomain.COPYWRITING,
            SkillDomain.EMAIL_MARKETING,
        ],
        skill_tags=["intranet", "interne-kommunikation", "newsletter", "faq", "marketingseiten"],
        ai_readiness=AIReadiness.READY,
        is_coordinator=False,
        notes="Interne Kommunikation. Zuständig für Intranet, FAQs und interne Newsletters.",
    ),
    Employee(
        employee_id="emp_014",
        display_name="Philipp Ehring",
        email="p.ehring@example.com",
        cluster_slugs=["SHK+E", "Dach_und_Holz", "Baugewerbe"],
        skill_domains=[
            SkillDomain.PROJECT_MANAGEMENT,
            SkillDomain.CONTENT_CREATION,
            SkillDomain.PAID_ADS,
        ],
        skill_tags=["koordination", "bu-info", "namensänderung", "landing-page", "sea", "mailing"],
        ai_readiness=AIReadiness.READY,
        is_coordinator=True,
        notes="Cross-Cluster-Koordinator. Querschnittsthemen über alle Business Units.",
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

"""
Skill matching: resolve SkillDomain from task text, recommend assignees,
and evaluate plausibility of an existing assignee.
"""

from __future__ import annotations

import re
from typing import Optional

from .employees import EMPLOYEES, Employee, get_employee_by_id
from .schemas import (
    AIReadiness,
    AssigneeRecommendation,
    AssigneePlausibilityResult,
    PlausibilityVerdict,
    SkillDomain,
)


# ---------------------------------------------------------------------------
# Keyword → SkillDomain mapping
# ---------------------------------------------------------------------------

_SKILL_KEYWORDS: dict[SkillDomain, list[str]] = {
    SkillDomain.CONTENT_CREATION: [
        "artikel", "blog", "beitrag", "content", "text", "story",
        "landingpage", "landing page", "advertorial",
    ],
    SkillDomain.SEO: [
        "seo", "suchmaschinenoptimierung", "keyword", "meta", "backlink",
        "ranking", "search console", "onpage", "offpage",
    ],
    SkillDomain.SOCIAL_MEDIA: [
        "instagram", "facebook", "linkedin", "tiktok", "social media",
        "social", "post", "reel", "story", "community", "ugc",
    ],
    SkillDomain.EMAIL_MARKETING: [
        "newsletter", "email", "e-mail", "mailing", "kampagne", "mailchimp",
        "klaviyo", "klickrate", "double opt in", "einladungs",
    ],
    SkillDomain.PAID_ADS: [
        "google ads", "facebook ads", "meta ads", "paid", "cpc", "cpm",
        "performance marketing", "anzeige", "werbeanzeige", "sea",
    ],
    SkillDomain.ANALYTICS: [
        "analytics", "tracking", "reporting", "auswertung", "kpi",
        "google analytics", "matomo", "conversion", "daten",
    ],
    SkillDomain.DESIGN: [
        "design", "grafik", "canva", "figma", "banner", "visual",
        "bildbearbeitung", "infografik", "mockup", "logo", "print",
        "ui", "ux", "layout",
    ],
    SkillDomain.COPYWRITING: [
        "text", "copy", "texter", "headline", "slogan", "werbetexter",
        "produkttext", "beschreibung",
    ],
    SkillDomain.PROJECT_MANAGEMENT: [
        "projektmanagement", "koordination", "briefing", "redaktionsplan",
        "planung", "deadline", "zeitplan", "messe", "event", "debriefing",
    ],
    SkillDomain.STRATEGY: [
        "strategie", "jahresplanung", "roadmap", "budget", "konzept",
        "analyse", "marktanalyse", "content-strategie",
    ],
    SkillDomain.TECHNICAL: [
        "cms", "wordpress", "website", "webseite", "html", "css",
        "entwicklung", "technisch", "integration", "plugin", "webhook",
        "hubspot", "automation", "wpforms",
    ],
}


def _tokenize(text: str) -> str:
    return re.sub(r"[^\w\s]", " ", text.lower())


def resolve_skill_domain(
    title: str,
    description: str = "",
) -> list[SkillDomain]:
    """
    Return a ranked list of matching SkillDomains based on keyword frequency.
    At minimum returns [SkillDomain.UNKNOWN] when nothing matches.
    """
    combined = _tokenize(f"{title} {description}")
    scores: dict[SkillDomain, int] = {}

    for domain, keywords in _SKILL_KEYWORDS.items():
        hit = sum(1 for kw in keywords if kw in combined)
        if hit > 0:
            scores[domain] = hit

    if not scores:
        return [SkillDomain.UNKNOWN]

    return sorted(scores, key=lambda d: scores[d], reverse=True)


def _employee_skill_score(employee: Employee, required_domains: list[SkillDomain]) -> tuple[float, list[str]]:
    """
    Returns (score 0..1, matched_skill_tags).
    """
    if not required_domains:
        return 0.0, []

    matched_domains = [d for d in required_domains if d in employee.skill_domains]
    domain_score = len(matched_domains) / len(required_domains)
    return domain_score, [d.value for d in matched_domains]


def recommend_assignees(
    title: str,
    description: str = "",
    cluster_slug: Optional[str] = None,
    top_n: int = 3,
    min_ai_readiness: Optional[AIReadiness] = None,
) -> list[AssigneeRecommendation]:
    """
    Return up to top_n recommended employees ordered by skill match confidence.
    Optionally filters by cluster_slug and min_ai_readiness.
    """
    required_domains = resolve_skill_domain(title, description)
    candidates = [e for e in EMPLOYEES if e.is_active]
    if cluster_slug:
        candidates = [e for e in candidates if cluster_slug in e.cluster_slugs] or candidates
    if min_ai_readiness:
        candidates = [e for e in candidates if e.ai_readiness.meets(min_ai_readiness)] or candidates

    results: list[AssigneeRecommendation] = []
    for emp in candidates:
        score, matched = _employee_skill_score(emp, required_domains)
        if score > 0:
            results.append(
                AssigneeRecommendation(
                    employee_id=emp.employee_id,
                    display_name=emp.display_name,
                    confidence=round(score, 3),
                    matched_skills=matched,
                    reason=f"Matches {len(matched)}/{len(required_domains)} required skill domains",
                    ai_readiness=emp.ai_readiness.value,
                )
            )

    results.sort(key=lambda r: r.confidence, reverse=True)
    return results[:top_n]


def evaluate_assignee_plausibility(
    employee_id: str,
    title: str,
    description: str = "",
    required_ai_readiness: Optional[AIReadiness] = None,
) -> AssigneePlausibilityResult:
    """
    Evaluate whether the given employee is a plausible assignee for the task.
    Also checks AI readiness if required_ai_readiness is specified.
    """
    emp = get_employee_by_id(employee_id)
    if emp is None:
        return AssigneePlausibilityResult(
            verdict=PlausibilityVerdict.UNKNOWN,
            explanation=f"Employee '{employee_id}' not found in registry.",
        )

    required_domains = resolve_skill_domain(title, description)
    if required_domains == [SkillDomain.UNKNOWN]:
        # Still check AI readiness even if skill domain is unknown
        human_review_required = False
        ai_note = ""
        if required_ai_readiness and not emp.ai_readiness.meets(required_ai_readiness):
            human_review_required = True
            ai_note = (
                f" AI-Readiness unzureichend: {emp.ai_readiness.value} "
                f"(benötigt: {required_ai_readiness.value}) → human_review_required."
            )
        if emp.ai_readiness == AIReadiness.NOVICE:
            human_review_required = True
            ai_note = f" {emp.display_name} ist AI-Novice → human_review_required."
        return AssigneePlausibilityResult(
            verdict=PlausibilityVerdict.UNKNOWN,
            employee_id=employee_id,
            display_name=emp.display_name,
            ai_readiness=emp.ai_readiness.value,
            human_review_required=human_review_required,
            explanation=(
                "Could not determine required skill domains from task text."
                + ai_note
            ),
        )

    matched = [d for d in required_domains if d in emp.skill_domains]
    missing = [d for d in required_domains if d not in emp.skill_domains]
    ratio = len(matched) / len(required_domains)

    # Check AI readiness
    human_review_required = False
    ai_note = ""
    if required_ai_readiness and not emp.ai_readiness.meets(required_ai_readiness):
        human_review_required = True
        ai_note = (
            f" AI-Readiness unzureichend: {emp.ai_readiness.value} "
            f"(benötigt: {required_ai_readiness.value}) → human_review_required."
        )

    if emp.ai_readiness == AIReadiness.NOVICE:
        human_review_required = True
        ai_note = f" {emp.display_name} ist AI-Novice → human_review_required."

    if ratio >= 0.6:
        verdict = PlausibilityVerdict.PLAUSIBLE
        explanation = f"{emp.display_name} covers {len(matched)}/{len(required_domains)} required domains.{ai_note}"
    elif ratio >= 0.3:
        verdict = PlausibilityVerdict.QUESTIONABLE
        explanation = (
            f"{emp.display_name} partially matches ({len(matched)}/{len(required_domains)} domains). "
            f"Missing: {', '.join(d.value for d in missing)}.{ai_note}"
        )
    else:
        verdict = PlausibilityVerdict.IMPLAUSIBLE
        explanation = (
            f"{emp.display_name} matches only {len(matched)}/{len(required_domains)} required domains. "
            f"Missing: {', '.join(d.value for d in missing)}.{ai_note}"
        )

    return AssigneePlausibilityResult(
        verdict=verdict,
        employee_id=employee_id,
        display_name=emp.display_name,
        matched_skills=[d.value for d in matched],
        missing_skills=[d.value for d in missing],
        explanation=explanation,
        ai_readiness=emp.ai_readiness.value,
        human_review_required=human_review_required,
    )


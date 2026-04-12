"""
Task categorization: assigns a TaskCategory to a ticket based on keyword patterns.

Rules:
  - Uses regex patterns on title + description
  - Returns the most likely TaskCategory or TaskCategory.OTHER
  - Also determines ai_readiness_required based on category and content
"""

from __future__ import annotations

import re
from typing import Optional

from .schemas import AIReadiness, TaskCategory

# ---------------------------------------------------------------------------
# Keyword patterns per category
# ---------------------------------------------------------------------------

_CATEGORY_PATTERNS: list[tuple[TaskCategory, list[str]]] = [
    (TaskCategory.WORDPRESS, [
        r"(?i)wordpress", r"(?i)wp\b", r"(?i)wpforms", r"(?i)plugin",
        r"(?i)blog.?(anpass|update|template)", r"(?i)webmaster",
        r"(?i)filterfunktion", r"(?i)php", r"(?i)template",
    ]),
    (TaskCategory.HUBSPOT, [
        r"(?i)hubspot", r"(?i)webhook", r"(?i)automation", r"(?i)automatisierung",
        r"(?i)double.opt.in", r"(?i)kontaktformular", r"(?i)redirect",
        r"(?i)crm", r"(?i)marketing.automation",
    ]),
    (TaskCategory.SOCIAL_MEDIA, [
        r"(?i)instagram", r"(?i)facebook", r"(?i)linkedin", r"(?i)tiktok",
        r"(?i)social.media", r"(?i)\bpost\b", r"(?i)reel", r"(?i)ugc",
        r"(?i)community.management", r"(?i)social.post",
    ]),
    (TaskCategory.SEO_CONTENT, [
        r"(?i)\bseo\b", r"(?i)suchmaschinenoptimierung", r"(?i)keyword.recherche",
        r"(?i)content.strategie", r"(?i)backlink", r"(?i)ranking",
        r"(?i)search.console", r"(?i)meta.beschreibung",
    ]),
    (TaskCategory.EVENT_MESSE, [
        r"(?i)\bmesse", r"(?i)event\b", r"(?i)veranstaltung",
        r"(?i)networking", r"(?i)speaker", r"(?i)debriefing",
        r"(?i)standbau", r"(?i)messeauftritt", r"(?i)einladung",
    ]),
    (TaskCategory.PRINT_GRAPHIC, [
        r"(?i)\bprint\b", r"(?i)logo", r"(?i)grafik", r"(?i)e.mail.signatur",
        r"(?i)messe.grafik", r"(?i)print.leitfaden", r"(?i)corporate.design",
        r"(?i)qrewnet", r"(?i)infografik", r"(?i)banner",
    ]),
    (TaskCategory.INTERNAL_COMM, [
        r"(?i)intranet", r"(?i)interne.kommunikation", r"(?i)interne.news",
        r"(?i)\bfaq\b", r"(?i)mitarbeiter.information", r"(?i)interner.newsletter",
    ]),
    (TaskCategory.LANDING_PAGES, [
        r"(?i)landing.page", r"(?i)landingpage", r"(?i)produktseite",
        r"(?i)subscription.site", r"(?i)layout.korrektur", r"(?i)ui.fix",
        r"(?i)ui.fehler",
    ]),
    (TaskCategory.CAMPAIGN_EMAIL, [
        r"(?i)kampagne\b", r"(?i)newsletter\b", r"(?i)mailing\b",
        r"(?i)e.mail.marketing", r"(?i)email.kampagne",
        r"(?i)einladungs.mail",
    ]),
    (TaskCategory.COORDINATION, [
        r"(?i)koordination", r"(?i)projektmanagement", r"(?i)briefing",
        r"(?i)redaktionsplan", r"(?i)bu.info", r"(?i)namensänderung",
        r"(?i)querschnitt",
    ]),
]

# AI-readiness keywords — if matched, ai_readiness_required = AI-Erfahren or higher
_AI_INTENSIVE_PATTERNS = [
    r"(?i)custom.gpt", r"(?i)prompt.engineering", r"(?i)ai.text",
    r"(?i)generative.ki", r"(?i)ki.bild", r"(?i)dall.e",
    r"(?i)midjourney", r"(?i)ai.generiert", r"(?i)automation.complex",
]

_AI_BASIC_PATTERNS = [
    r"(?i)\bki\b", r"(?i)\bai\b", r"(?i)chatgpt", r"(?i)gpt",
    r"(?i)ai.unterstützung", r"(?i)ai.tool",
]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def categorize_task(title: str, description: str = "") -> TaskCategory:
    """
    Assign a TaskCategory to a ticket based on keyword patterns in title + description.
    Returns TaskCategory.OTHER if no pattern matches.
    """
    combined = f"{title} {description}"
    best_category = TaskCategory.OTHER
    best_score = 0

    for category, patterns in _CATEGORY_PATTERNS:
        score = sum(1 for p in patterns if re.search(p, combined))
        if score > best_score:
            best_score = score
            best_category = category

    return best_category


def determine_ai_readiness_required(
    title: str,
    description: str = "",
    category: Optional[TaskCategory] = None,
) -> AIReadiness:
    """
    Determine the minimum AI readiness required for this task.

    Returns:
      - AI-Pioneer   if highly AI-intensive (Prompt-Engineering, Dall-E, etc.)
      - AI-Erfahren  if AI tools or automation are needed
      - AI-Bereit    for most standard digital tasks
      - AI-Novice    for purely manual/print tasks
    """
    combined = f"{title} {description}"

    # Check for AI-intensive patterns
    if any(re.search(p, combined) for p in _AI_INTENSIVE_PATTERNS):
        return AIReadiness.EXPERIENCED

    # Check for basic AI patterns
    if any(re.search(p, combined) for p in _AI_BASIC_PATTERNS):
        return AIReadiness.READY

    # Category-based defaults
    if category in (TaskCategory.HUBSPOT, TaskCategory.SEO_CONTENT):
        return AIReadiness.READY

    if category in (TaskCategory.PRINT_GRAPHIC, TaskCategory.EVENT_MESSE):
        return AIReadiness.NOVICE

    return AIReadiness.READY

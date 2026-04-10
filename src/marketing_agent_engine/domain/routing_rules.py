"""
Routing rules: resolve a free-text ticket title/description to a BusinessUnit
and Cluster using keyword scoring, alias matching, and cluster-level fallback.
"""

from __future__ import annotations

import re
from typing import Optional

from .business_units import BUSINESS_UNITS, BusinessUnit, get_business_unit_by_slug
from .clusters import CLUSTERS, get_cluster_coordinator_id
from .employees import get_coordinator_for_cluster
from .schemas import BusinessUnitMatch, ClusterSlug, RoutingResult


def _tokenize(text: str) -> list[str]:
    """Lowercase, strip punctuation, split on whitespace."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    return text.split()


def _score_business_unit(tokens: list[str], bu: BusinessUnit) -> float:
    """
    Score a business unit against a token list.
    Returns a value in [0.0, 1.0] reflecting how well the tokens match.
    """
    if not tokens:
        return 0.0

    all_terms = [t.lower() for t in bu.key_terms + bu.aliases + [bu.display_name]]
    hit_count = sum(1 for t in tokens if t in all_terms)
    # Partial phrase matching: check if any key term appears as substring
    joined = " ".join(tokens)
    for term in all_terms:
        if len(term) > 3 and term in joined:
            hit_count += 0.5

    return min(hit_count / max(len(all_terms), 1), 1.0)


def _score_cluster(tokens: list[str], cluster_slug: ClusterSlug) -> float:
    from .clusters import get_cluster_key_terms
    key_terms = get_cluster_key_terms(cluster_slug)
    if not key_terms:
        return 0.0
    joined = " ".join(tokens)
    hit_count = sum(1 for t in key_terms if t.lower() in joined)
    return min(hit_count / len(key_terms), 1.0)


def resolve_business_unit(
    title: str,
    description: str = "",
    asana_project_gid: Optional[str] = None,
) -> Optional[BusinessUnitMatch]:
    """
    Attempt to resolve the most likely BusinessUnit from title + description.
    Returns None when no unit scores above the minimum threshold.
    """
    MIN_CONFIDENCE = 0.05

    # GID shortcut
    if asana_project_gid:
        for bu in BUSINESS_UNITS:
            if bu.asana_project_gid and bu.asana_project_gid == asana_project_gid:
                return BusinessUnitMatch(
                    slug=bu.slug,
                    display_name=bu.display_name,
                    cluster=bu.cluster,
                    confidence=1.0,
                    matched_by="asana_project_gid",
                )

    combined = f"{title} {description}"
    tokens = _tokenize(combined)
    if not tokens:
        return None

    best_bu: Optional[BusinessUnit] = None
    best_score = 0.0

    for bu in BUSINESS_UNITS:
        if not bu.is_active:
            continue
        score = _score_business_unit(tokens, bu)
        if score > best_score:
            best_score = score
            best_bu = bu

    if best_bu is None or best_score < MIN_CONFIDENCE:
        return None

    return BusinessUnitMatch(
        slug=best_bu.slug,
        display_name=best_bu.display_name,
        cluster=best_bu.cluster,
        confidence=round(min(best_score * 3, 1.0), 3),
        matched_by="keyword_scoring",
    )


def resolve_cluster(
    title: str,
    description: str = "",
    business_unit_slug: Optional[str] = None,
) -> ClusterSlug:
    """
    Resolve a ClusterSlug. Prefers BU lookup, falls back to cluster-level
    keyword scoring. Returns UNBEKANNT when nothing matches.
    """
    # Direct BU → cluster
    if business_unit_slug:
        bu = get_business_unit_by_slug(business_unit_slug)
        if bu:
            return bu.cluster

    combined = f"{title} {description}"
    tokens = _tokenize(combined)
    if not tokens:
        return ClusterSlug.UNBEKANNT

    best_cluster = ClusterSlug.UNBEKANNT
    best_score = 0.0

    for cluster in CLUSTERS:
        if cluster.slug == ClusterSlug.UNBEKANNT:
            continue
        score = _score_cluster(tokens, cluster.slug)
        if score > best_score:
            best_score = score
            best_cluster = cluster.slug

    return best_cluster if best_score >= 0.02 else ClusterSlug.UNBEKANNT


def get_cluster_coordinator(cluster_slug: ClusterSlug) -> Optional[str]:
    """Return employee_id of the coordinator for the given cluster."""
    emp = get_coordinator_for_cluster(cluster_slug.value)
    if emp:
        return emp.employee_id
    return get_cluster_coordinator_id(cluster_slug)


def route_ticket(
    title: str,
    description: str = "",
    asana_project_gid: Optional[str] = None,
) -> RoutingResult:
    """
    Full routing pipeline: BU → cluster → coordinator.
    Returns a RoutingResult with full provenance.
    """
    resolution_path: list[str] = []

    bu_match = resolve_business_unit(title, description, asana_project_gid)
    if bu_match:
        resolution_path.append(f"business_unit:{bu_match.slug}")
        cluster = bu_match.cluster
        resolution_path.append(f"cluster:{cluster.value}")
    else:
        cluster = resolve_cluster(title, description)
        resolution_path.append(f"cluster_fallback:{cluster.value}")

    coordinator_id = get_cluster_coordinator(cluster)
    if coordinator_id:
        resolution_path.append(f"coordinator:{coordinator_id}")

    confidence = bu_match.confidence if bu_match else (0.3 if cluster != ClusterSlug.UNBEKANNT else 0.0)

    return RoutingResult(
        business_unit=bu_match,
        cluster=cluster,
        cluster_coordinator_id=coordinator_id,
        confidence=confidence,
        resolution_path=resolution_path,
    )

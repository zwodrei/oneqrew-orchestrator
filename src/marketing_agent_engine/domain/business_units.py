"""
Business unit registry with slugs, display names, aliases, cluster membership,
and key terms used for routing and text-matching.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from .schemas import ClusterSlug


class BusinessUnit(BaseModel):
    slug: str
    display_name: str
    cluster: ClusterSlug
    aliases: list[str] = Field(default_factory=list)
    key_terms: list[str] = Field(default_factory=list)
    asana_project_gid: Optional[str] = None
    is_active: bool = True


# ---------------------------------------------------------------------------
# Business unit registry
# ---------------------------------------------------------------------------

BUSINESS_UNITS: list[BusinessUnit] = [
    # ── SHK+E ────────────────────────────────────────────────────────────────
    BusinessUnit(
        slug="shk_heizung",
        display_name="SHK – Heizung",
        cluster=ClusterSlug.SHK_E,
        aliases=["heizung", "heizungsbau", "wärmepumpe", "heiztechnik"],
        key_terms=[
            "heizung", "heizungsanlage", "wärmepumpe", "heiztechnik",
            "pelletofen", "fernwärme", "gasheizung", "ölheizung",
        ],
    ),
    BusinessUnit(
        slug="shk_sanitaer",
        display_name="SHK – Sanitär",
        cluster=ClusterSlug.SHK_E,
        aliases=["sanitär", "bad", "badezimmer", "sanitärtechnik"],
        key_terms=[
            "sanitär", "bad", "badezimmer", "wasserinstallation",
            "wc", "dusche", "badplanung", "armaturen",
        ],
    ),
    BusinessUnit(
        slug="shk_elektro",
        display_name="SHK – Elektro",
        cluster=ClusterSlug.SHK_E,
        aliases=["elektro", "elektroinstallation", "e-installation"],
        key_terms=[
            "elektro", "elektroinstallation", "photovoltaik", "pv",
            "ladestation", "wallbox", "smart-home", "elektrik",
        ],
    ),
    BusinessUnit(
        slug="shk_klima",
        display_name="SHK – Klima & Lüftung",
        cluster=ClusterSlug.SHK_E,
        aliases=["klima", "klimaanlage", "lüftung", "kältetechnik"],
        key_terms=[
            "klimaanlage", "klimatechnik", "lüftungsanlage", "wohnraumlüftung",
            "kältetechnik", "split-klimaanlage",
        ],
    ),
    # ── Dach_und_Holz ────────────────────────────────────────────────────────
    BusinessUnit(
        slug="dach_ziegel",
        display_name="Dach – Ziegeldeckung",
        cluster=ClusterSlug.DACH_UND_HOLZ,
        aliases=["ziegel", "ziegeldach", "dachdeckung"],
        key_terms=[
            "ziegel", "dachziegel", "dachdeckung", "ziegeldach",
            "tonziegel", "betonziegel",
        ],
    ),
    BusinessUnit(
        slug="dach_flachdach",
        display_name="Dach – Flachdach",
        cluster=ClusterSlug.DACH_UND_HOLZ,
        aliases=["flachdach", "flachdachsanierung"],
        key_terms=[
            "flachdach", "flachdachsanierung", "dachbegrünung",
            "bitumen", "foliendach",
        ],
    ),
    BusinessUnit(
        slug="dach_abdichtung",
        display_name="Dach – Abdichtung & Sanierung",
        cluster=ClusterSlug.DACH_UND_HOLZ,
        aliases=["abdichtung", "dachabdichtung", "sanierung"],
        key_terms=[
            "dachabdichtung", "abdichtung", "sanierung", "kellersanierung",
            "feuchtigkeitsschutz",
        ],
    ),
    BusinessUnit(
        slug="holzbau",
        display_name="Holzbau & Zimmerei",
        cluster=ClusterSlug.DACH_UND_HOLZ,
        aliases=["holzbau", "zimmerei", "holzkonstruktion"],
        key_terms=[
            "holzbau", "zimmerei", "holzkonstruktion", "dachstuhl",
            "carport", "terrasse", "balkon", "holzrahmenbau",
        ],
    ),
    # ── Baugewerbe ───────────────────────────────────────────────────────────
    BusinessUnit(
        slug="bau_rohbau",
        display_name="Bau – Rohbau",
        cluster=ClusterSlug.BAUGEWERBE,
        aliases=["rohbau", "mauerwerk", "betonbau"],
        key_terms=[
            "rohbau", "mauerwerk", "betonbau", "fundament",
            "stahlbeton", "hochbau", "neubau",
        ],
    ),
    BusinessUnit(
        slug="bau_ausbau",
        display_name="Bau – Innenausbau",
        cluster=ClusterSlug.BAUGEWERBE,
        aliases=["innenausbau", "ausbau", "trockenbau"],
        key_terms=[
            "innenausbau", "ausbau", "trockenbau", "estrich",
            "fliesen", "bodenbeläge", "deckenverkleidung",
        ],
    ),
    BusinessUnit(
        slug="bau_tiefbau",
        display_name="Bau – Tiefbau",
        cluster=ClusterSlug.BAUGEWERBE,
        aliases=["tiefbau", "erdarbeiten", "kanalbau"],
        key_terms=[
            "tiefbau", "erdarbeiten", "kanalbau", "pflasterarbeiten",
            "straßenbau", "drainage",
        ],
    ),
    BusinessUnit(
        slug="bau_malerarbeiten",
        display_name="Bau – Maler & Lackierer",
        cluster=ClusterSlug.BAUGEWERBE,
        aliases=["maler", "lackierer", "anstrich"],
        key_terms=[
            "maler", "lackierer", "anstrich", "fassadenfarbe",
            "tapete", "wandgestaltung", "putz",
        ],
    ),
]

# Lookup maps
_BY_SLUG: dict[str, BusinessUnit] = {bu.slug: bu for bu in BUSINESS_UNITS}
_BY_ALIAS: dict[str, BusinessUnit] = {}
for _bu in BUSINESS_UNITS:
    for _alias in _bu.aliases:
        _BY_ALIAS[_alias.lower()] = _bu


def get_business_unit_by_slug(slug: str) -> Optional[BusinessUnit]:
    return _BY_SLUG.get(slug)


def get_business_units_by_cluster(cluster: ClusterSlug) -> list[BusinessUnit]:
    return [bu for bu in BUSINESS_UNITS if bu.cluster == cluster and bu.is_active]


def get_all_active_business_units() -> list[BusinessUnit]:
    return [bu for bu in BUSINESS_UNITS if bu.is_active]


def find_by_alias(term: str) -> Optional[BusinessUnit]:
    return _BY_ALIAS.get(term.lower())

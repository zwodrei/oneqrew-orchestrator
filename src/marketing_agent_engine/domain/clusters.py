"""
Cluster registry with metadata, coordinator resolution, and key-term sets.

Clusters group related business units and define the top-level routing
hierarchy for the Marketing Agent Engine.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from .schemas import ClusterSlug


class Cluster(BaseModel):
    slug: ClusterSlug
    display_name: str
    coordinator_employee_id: Optional[str] = None
    business_unit_slugs: list[str] = Field(default_factory=list)
    key_terms: list[str] = Field(default_factory=list)
    description: str = ""


CLUSTERS: list[Cluster] = [
    Cluster(
        slug=ClusterSlug.SHK_E,
        display_name="SHK + Elektro",
        coordinator_employee_id="emp_002",
        business_unit_slugs=[
            "shk_heizung",
            "shk_sanitaer",
            "shk_elektro",
            "shk_klima",
        ],
        key_terms=[
            "shk", "sanitär", "heizung", "klima", "elektro",
            "wärmepumpe", "photovoltaik", "pv", "wallbox",
            "ladestation", "smart-home", "bad",
        ],
        description=(
            "Sanitär, Heizung, Klima und Elektro –"
            " gebäudetechnische Haustechnik."
        ),
    ),
    Cluster(
        slug=ClusterSlug.DACH_UND_HOLZ,
        display_name="Dach und Holz",
        coordinator_employee_id="emp_004",
        business_unit_slugs=[
            "dach_ziegel",
            "dach_flachdach",
            "dach_abdichtung",
            "holzbau",
        ],
        key_terms=[
            "dach", "dachdeckung", "ziegel", "flachdach",
            "abdichtung", "holzbau", "zimmerei", "dachstuhl",
            "sanierung", "carport",
        ],
        description="Dacharbeiten jeder Art sowie Holzbau und Zimmerei.",
    ),
    Cluster(
        slug=ClusterSlug.BAUGEWERBE,
        display_name="Baugewerbe",
        coordinator_employee_id="emp_005",
        business_unit_slugs=[
            "bau_rohbau",
            "bau_ausbau",
            "bau_tiefbau",
            "bau_malerarbeiten",
        ],
        key_terms=[
            "bau", "rohbau", "ausbau", "innenausbau", "tiefbau",
            "maler", "mauerwerk", "estrich", "trockenbau",
            "erdarbeiten", "neubau",
        ],
        description="Allgemeines Baugewerbe: Rohbau, Ausbau, Tiefbau, Maler.",
    ),
    Cluster(
        slug=ClusterSlug.UNBEKANNT,
        display_name="Unbekannt / Nicht zugeordnet",
        coordinator_employee_id=None,
        business_unit_slugs=[],
        key_terms=[],
        description=(
            "Fallback-Cluster für Tickets, die keinem"
            " bekannten Cluster zugeordnet werden können."
        ),
    ),
]

_BY_SLUG: dict[ClusterSlug, Cluster] = {c.slug: c for c in CLUSTERS}


def get_cluster(slug: ClusterSlug) -> Optional[Cluster]:
    return _BY_SLUG.get(slug)


def get_all_known_clusters() -> list[Cluster]:
    return [c for c in CLUSTERS if c.slug != ClusterSlug.UNBEKANNT]


def get_cluster_key_terms(slug: ClusterSlug) -> list[str]:
    cluster = _BY_SLUG.get(slug)
    return cluster.key_terms if cluster else []


def get_cluster_coordinator_id(slug: ClusterSlug) -> Optional[str]:
    cluster = _BY_SLUG.get(slug)
    return cluster.coordinator_employee_id if cluster else None

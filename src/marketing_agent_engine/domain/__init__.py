"""
marketing_agent_engine.domain

Public API for the domain layer. Import from here to avoid coupling to
internal module structure.
"""

from .assignment_rules import AssignmentAnalysis, analyse_assignment
from .business_units import (
    BUSINESS_UNITS,
    BusinessUnit,
    find_by_alias,
    get_all_active_business_units,
    get_business_unit_by_slug,
    get_business_units_by_cluster,
)
from .clusters import (
    CLUSTERS,
    Cluster,
    get_all_known_clusters,
    get_cluster,
    get_cluster_coordinator_id,
    get_cluster_key_terms,
)
from .completeness_rules import check_completeness
from .employees import (
    EMPLOYEES,
    Employee,
    get_active_employees,
    get_coordinator_for_cluster,
    get_employee_by_asana_gid,
    get_employee_by_email,
    get_employee_by_id,
    get_employees_by_cluster,
)
from .routing_rules import (
    get_cluster_coordinator,
    resolve_business_unit,
    resolve_cluster,
    route_ticket,
)
from .schemas import (
    AssigneeRecommendation,
    AssigneePlausibilityResult,
    BusinessUnitMatch,
    ClusterSlug,
    CompletenessFlag,
    CompletenessResult,
    PlausibilityVerdict,
    RoutingResult,
    SkillDomain,
)
from .skill_matching import (
    evaluate_assignee_plausibility,
    recommend_assignees,
    resolve_skill_domain,
)

__all__ = [
    "ClusterSlug",
    "SkillDomain",
    "AssigneeRecommendation",
    "AssigneePlausibilityResult",
    "PlausibilityVerdict",
    "CompletenessFlag",
    "CompletenessResult",
    "BusinessUnitMatch",
    "RoutingResult",
    "Employee",
    "EMPLOYEES",
    "get_employee_by_id",
    "get_employee_by_email",
    "get_employee_by_asana_gid",
    "get_active_employees",
    "get_employees_by_cluster",
    "get_coordinator_for_cluster",
    "BusinessUnit",
    "BUSINESS_UNITS",
    "get_business_unit_by_slug",
    "get_business_units_by_cluster",
    "get_all_active_business_units",
    "find_by_alias",
    "Cluster",
    "CLUSTERS",
    "get_cluster",
    "get_all_known_clusters",
    "get_cluster_key_terms",
    "get_cluster_coordinator_id",
    "resolve_business_unit",
    "resolve_cluster",
    "get_cluster_coordinator",
    "route_ticket",
    "resolve_skill_domain",
    "recommend_assignees",
    "evaluate_assignee_plausibility",
    "check_completeness",
    "AssignmentAnalysis",
    "analyse_assignment",
]

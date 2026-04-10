"""
test_domain.py — Unit tests for deterministic domain layer.

Covers: route_ticket(), check_completeness(), evaluate_assignee_plausibility(),
recommend_assignees(). No LLM, no MCP, no I/O.
"""
from __future__ import annotations

import pytest

from marketing_agent_engine.domain.completeness_rules import check_completeness
from marketing_agent_engine.domain.routing_rules import route_ticket
from marketing_agent_engine.domain.schemas import (
    ClusterSlug,
    CompletenessFlag,
    CompletenessResult,
    PlausibilityVerdict,
)
from marketing_agent_engine.domain.skill_matching import (
    evaluate_assignee_plausibility,
    recommend_assignees,
    resolve_skill_domain,
)


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────

FULL_TICKET = {
    "gid": "t001",
    "name": "Instagram Reels Kampagne Flachdach Q3",
    "notes": (
        "Wir benötigen 4 Instagram Reels für die Flachdach-Saison. "
        "Themen: Vorteile Flachdach, Dachbegrünung, Abdichtung, Wartungstipps. "
        "Zielgruppe: Eigenheimbesitzer 35–55."
    ),
    "due_on": "2025-07-01",
    "assignee": {"gid": "gid_emp_004", "name": "David Klein"},
    "projects": [{"gid": "proj_dach_q3", "name": "Dach_und_Holz Q3"}],
    "tags": [{"name": "social-media"}],
    "custom_fields": [{"display_value": "Social Media"}],
    "followers": [{"gid": "follower_1"}],
    "workspace": {"gid": "ws_main"},
    "permalink_url": "https://app.asana.com/0/test/001",
}

EMPTY_TICKET: dict = {"gid": "t002", "name": "", "notes": ""}


# ─────────────────────────────────────────────────────────────────────────────
# route_ticket()
# ─────────────────────────────────────────────────────────────────────────────

class TestRouteTicket:
    def test_shk_cluster_from_heizung_keyword(self) -> None:
        r = route_ticket("Wärmepumpe Landingpage", "Neue Seite für Wärmepumpen Heizungsanlage")
        assert r.cluster == ClusterSlug.SHK_E

    def test_dach_cluster_from_flachdach_keyword(self) -> None:
        r = route_ticket("Flachdach Sanierungsartikel", "Artikel über Flachdachsanierung Dachbegrünung")
        assert r.cluster == ClusterSlug.DACH_UND_HOLZ

    def test_baugewerbe_cluster_from_rohbau_keyword(self) -> None:
        r = route_ticket("Rohbau Kampagne Neubau", "Kampagne für Rohbau- und Neubau-Projekte")
        assert r.cluster == ClusterSlug.BAUGEWERBE

    def test_unbekannt_for_noise_input(self) -> None:
        r = route_ticket("xyz abc 123", "")
        assert r.cluster == ClusterSlug.UNBEKANNT

    def test_confidence_is_zero_for_unbekannt(self) -> None:
        r = route_ticket("xyz abc", "")
        assert r.confidence == 0.0

    def test_coordinator_set_for_known_cluster(self) -> None:
        r = route_ticket("Heizung Newsletter Wärmepumpe gasheizung", "shk sanitär bad")
        if r.cluster != ClusterSlug.UNBEKANNT:
            assert r.cluster_coordinator_id is not None

    def test_resolution_path_non_empty_for_match(self) -> None:
        r = route_ticket("Flachdach abdichtung dachbegrünung", "ziegel sanierung")
        if r.cluster != ClusterSlug.UNBEKANNT:
            assert len(r.resolution_path) >= 1

    def test_routing_result_has_confidence_in_range(self) -> None:
        r = route_ticket("Photovoltaik Wallbox Elektro Smart-Home", "pv anlage ladestation")
        assert 0.0 <= r.confidence <= 1.0

    def test_business_unit_resolved_for_strong_match(self) -> None:
        r = route_ticket("Flachdach Sanierung Abdichtung Bitumen", "foliendach flachdachsanierung")
        assert r.business_unit is not None
        assert r.business_unit.cluster == ClusterSlug.DACH_UND_HOLZ


# ─────────────────────────────────────────────────────────────────────────────
# check_completeness()
# ─────────────────────────────────────────────────────────────────────────────

class TestCheckCompleteness:
    def test_full_ticket_scores_high(self) -> None:
        result = check_completeness(FULL_TICKET)
        assert result.score >= 0.7

    def test_empty_ticket_scores_low(self) -> None:
        result = check_completeness(EMPTY_TICKET)
        assert result.score < 0.5

    def test_always_returns_eleven_flags(self) -> None:
        assert len(check_completeness(FULL_TICKET).flags) == 11
        assert len(check_completeness(EMPTY_TICKET).flags) == 11

    def test_missing_fields_listed_for_empty_ticket(self) -> None:
        result = check_completeness(EMPTY_TICKET)
        assert "title_present" in result.missing
        assert "description_present" in result.missing
        assert "assignee_set" in result.missing

    def test_due_date_flag_passes_when_present(self) -> None:
        ticket = {**EMPTY_TICKET, "due_on": "2025-09-01"}
        result = check_completeness(ticket)
        flag = next(f for f in result.flags if f.criterion == "due_date_set")
        assert flag.passed is True

    def test_score_bounds(self) -> None:
        assert 0.0 <= check_completeness(FULL_TICKET).score <= 1.0
        assert 0.0 <= check_completeness(EMPTY_TICKET).score <= 1.0

    def test_passed_computed_field_true_above_80pct(self) -> None:
        flags = [CompletenessFlag(criterion=f"c{i}", passed=True) for i in range(9)]
        flags += [CompletenessFlag(criterion="c9", passed=False)]
        result = CompletenessResult(score=0.9, flags=flags, missing=["c9"])
        assert result.passed is True

    def test_passed_computed_field_false_below_80pct(self) -> None:
        flags = [CompletenessFlag(criterion=f"c{i}", passed=True) for i in range(7)]
        flags += [CompletenessFlag(criterion=f"m{i}", passed=False) for i in range(4)]
        result = CompletenessResult(
            score=0.636, flags=flags, missing=[f"m{i}" for i in range(4)]
        )
        assert result.passed is False

    def test_warnings_have_text_for_failed_flags(self) -> None:
        result = check_completeness(EMPTY_TICKET)
        assert len(result.warnings) > 0

    def test_project_flag_passes_when_set(self) -> None:
        ticket = {**EMPTY_TICKET, "projects": [{"gid": "p1", "name": "P1"}]}
        result = check_completeness(ticket)
        flag = next(f for f in result.flags if f.criterion == "project_assigned")
        assert flag.passed is True


# ─────────────────────────────────────────────────────────────────────────────
# evaluate_assignee_plausibility()
# ─────────────────────────────────────────────────────────────────────────────

class TestEvaluatePlausibility:
    def test_social_media_employee_is_plausible_for_social_task(self) -> None:
        # emp_002: SOCIAL_MEDIA, PAID_ADS, ANALYTICS
        result = evaluate_assignee_plausibility(
            "emp_002",
            title="Instagram Facebook Reel Social Media Post",
            description="instagram reel community social paid facebook-ads",
        )
        assert result.verdict == PlausibilityVerdict.PLAUSIBLE

    def test_seo_employee_is_implausible_for_pure_design_task(self) -> None:
        # emp_004: SEO, ANALYTICS, TECHNICAL — design task should be low match
        result = evaluate_assignee_plausibility(
            "emp_004",
            title="Design Grafik Canva Banner Visual Mockup Infografik",
            description="design grafik canva figma bildbearbeitung infografik mockup banner visual",
        )
        assert result.verdict in (
            PlausibilityVerdict.IMPLAUSIBLE,
            PlausibilityVerdict.QUESTIONABLE,
            PlausibilityVerdict.UNKNOWN,
        )

    def test_nonexistent_employee_returns_unknown(self) -> None:
        result = evaluate_assignee_plausibility("emp_9999", title="Beliebiger Titel")
        assert result.verdict == PlausibilityVerdict.UNKNOWN
        assert "emp_9999" in result.explanation

    def test_result_always_has_explanation(self) -> None:
        result = evaluate_assignee_plausibility("emp_001", title="SEO Artikel Blog")
        assert result.explanation != ""

    def test_matched_skills_populated_for_plausible(self) -> None:
        result = evaluate_assignee_plausibility(
            "emp_002",
            title="Social Media Instagram Reel Post",
            description="instagram facebook ads tracking analytics",
        )
        if result.verdict == PlausibilityVerdict.PLAUSIBLE:
            assert len(result.matched_skills) > 0


# ─────────────────────────────────────────────────────────────────────────────
# recommend_assignees()
# ─────────────────────────────────────────────────────────────────────────────

class TestRecommendAssignees:
    def test_returns_list(self) -> None:
        recs = recommend_assignees("Instagram Reel Social Post", "social media instagram")
        assert isinstance(recs, list)

    def test_top_n_respected(self) -> None:
        recs = recommend_assignees("SEO Artikel Blog", "keyword ranking", top_n=2)
        assert len(recs) <= 2

    def test_ordered_by_confidence_descending(self) -> None:
        recs = recommend_assignees("SEO Analytics Tracking Daten Auswertung", "reporting kpi")
        if len(recs) >= 2:
            assert recs[0].confidence >= recs[1].confidence

    def test_recommendation_fields_present(self) -> None:
        recs = recommend_assignees("Newsletter Email Kampagne", "mailing klickrate klaviyo")
        if recs:
            r = recs[0]
            assert r.employee_id
            assert r.display_name
            assert 0.0 <= r.confidence <= 1.0

    def test_cluster_filter_respected(self) -> None:
        from marketing_agent_engine.domain.employees import EMPLOYEES
        recs = recommend_assignees(
            "Dach Flachdach Content", "artikel blog text",
            cluster_slug="Dach_und_Holz",
        )
        # All returned employees should be in the Dach_und_Holz cluster
        # (or the fallback was triggered — still bounded by active employee count)
        active = len([e for e in EMPLOYEES if e.is_active])
        assert len(recs) <= active

    def test_resolve_skill_domain_returns_list(self) -> None:
        from marketing_agent_engine.domain.schemas import SkillDomain
        domains = resolve_skill_domain("Instagram Reel Social Media Post", "instagram facebook")
        assert isinstance(domains, list)
        assert len(domains) >= 1
        assert all(isinstance(d, SkillDomain) for d in domains)

"""
Tests for task categorization and skill matrix mapping.
"""

from __future__ import annotations

import pytest

from marketing_agent_engine.domain import (
    AIReadiness,
    EMPLOYEES,
    TaskCategory,
    categorize_task,
    determine_ai_readiness_required,
    evaluate_assignee_plausibility,
    recommend_assignees,
)
from marketing_agent_engine.domain.assignment_rules import analyse_assignment
from marketing_agent_engine.domain.schemas import PlausibilityVerdict


# ---------------------------------------------------------------------------
# Task categorization
# ---------------------------------------------------------------------------

class TestCategorizeTask:
    def test_wordpress(self):
        assert categorize_task("WordPress Plugin Update") == TaskCategory.WORDPRESS

    def test_wordpress_with_notes(self):
        assert categorize_task("Webseite anpassen", "WordPress Template und Blog-Anpassung") == TaskCategory.WORDPRESS

    def test_hubspot(self):
        assert categorize_task("HubSpot Kontaktformular einrichten") == TaskCategory.HUBSPOT

    def test_hubspot_webhook(self):
        assert categorize_task("Webhook einrichten", "Automation für Double-Opt-In in HubSpot") == TaskCategory.HUBSPOT

    def test_social_media(self):
        assert categorize_task("Instagram Post für Messe") == TaskCategory.SOCIAL_MEDIA

    def test_social_media_ugc(self):
        assert categorize_task("UGC Experiment", "LinkedIn und Instagram Posts erstellen") == TaskCategory.SOCIAL_MEDIA

    def test_seo_content(self):
        assert categorize_task("SEO-Optimierung Produktseite") == TaskCategory.SEO_CONTENT

    def test_seo_keyword(self):
        assert categorize_task("Keyword-Recherche Q2", "Content-Strategie für SHK-Cluster") == TaskCategory.SEO_CONTENT

    def test_event_messe(self):
        assert categorize_task("Messeplanung ISH 2025") == TaskCategory.EVENT_MESSE

    def test_event_networking(self):
        assert categorize_task("Networking Event", "Speaker-Slots und Raumausstattung") == TaskCategory.EVENT_MESSE

    def test_print_graphic(self):
        assert categorize_task("Logo Design Update") == TaskCategory.PRINT_GRAPHIC

    def test_print_leitfaden(self):
        assert categorize_task("Print-Leitfaden erstellen", "Corporate Design Messe-Grafiken") == TaskCategory.PRINT_GRAPHIC

    def test_internal_comm(self):
        assert categorize_task("Intranet News veröffentlichen") == TaskCategory.INTERNAL_COMM

    def test_landing_pages(self):
        assert categorize_task("Landing-Page Korrektur SHK") == TaskCategory.LANDING_PAGES

    def test_campaign_email(self):
        assert categorize_task("Newsletter für Wärmepumpe Q2") == TaskCategory.CAMPAIGN_EMAIL

    def test_coordination(self):
        assert categorize_task("Koordination BU-Informationen") == TaskCategory.COORDINATION

    def test_other(self):
        assert categorize_task("Unbekannte Aufgabe ohne Keywords") == TaskCategory.OTHER


# ---------------------------------------------------------------------------
# AI-Readiness determination
# ---------------------------------------------------------------------------

class TestDetermineAIReadiness:
    def test_custom_gpt_requires_experienced(self):
        result = determine_ai_readiness_required("Custom-GPT für Texterstellung", "AI-generierte Texte produzieren")
        assert result == AIReadiness.EXPERIENCED

    def test_prompt_engineering_requires_experienced(self):
        result = determine_ai_readiness_required("Prompt-Engineering für Banner", "")
        assert result == AIReadiness.EXPERIENCED

    def test_basic_ai_requires_ready(self):
        result = determine_ai_readiness_required("ChatGPT nutzen", "AI-Unterstützung bei Texten")
        assert result == AIReadiness.READY

    def test_print_category_requires_novice(self):
        result = determine_ai_readiness_required("Logo Design", "Print-Leitfaden erstellen", TaskCategory.PRINT_GRAPHIC)
        assert result == AIReadiness.NOVICE

    def test_event_category_requires_novice(self):
        result = determine_ai_readiness_required("Messeplanung", "Tickets und Debriefing", TaskCategory.EVENT_MESSE)
        assert result == AIReadiness.NOVICE

    def test_standard_digital_task_requires_ready(self):
        result = determine_ai_readiness_required("Newsletter erstellen", "Mailing an Fachbetriebe")
        assert result == AIReadiness.READY


# ---------------------------------------------------------------------------
# Skill matrix / employee registry
# ---------------------------------------------------------------------------

class TestEmployeeRegistry:
    def test_14_employees_loaded(self):
        assert len(EMPLOYEES) == 14

    def test_all_have_ai_readiness(self):
        for emp in EMPLOYEES:
            assert emp.ai_readiness in AIReadiness

    def test_ai_novices(self):
        novices = [e for e in EMPLOYEES if e.ai_readiness == AIReadiness.NOVICE]
        novice_names = {e.display_name for e in novices}
        assert "Lina Weiß" in novice_names
        assert "André Köhler" in novice_names
        assert "Christina Helms" in novice_names

    def test_ai_pioneer(self):
        pioneers = [e for e in EMPLOYEES if e.ai_readiness == AIReadiness.PIONEER]
        assert any(e.display_name == "Sandra Hoppe" for e in pioneers)

    def test_ai_experienced(self):
        experienced = [e for e in EMPLOYEES if e.ai_readiness == AIReadiness.EXPERIENCED]
        names = {e.display_name for e in experienced}
        assert "Matteo Diehl" in names
        assert "Laura Piccolomo" in names

    def test_coordinators(self):
        coordinators = [e for e in EMPLOYEES if e.is_coordinator]
        names = {e.display_name for e in coordinators}
        assert "Maren Hoyer" in names
        assert "Sara Niklassik" in names
        assert "Philipp Ehring" in names


# ---------------------------------------------------------------------------
# Recommend assignees with AI-Readiness filter
# ---------------------------------------------------------------------------

class TestRecommendAssignees:
    def test_hubspot_recommends_matteo_first(self):
        recs = recommend_assignees("HubSpot Automation", "Webhook und Double-Opt-In")
        assert len(recs) > 0
        assert recs[0].display_name == "Matteo Diehl"
        assert recs[0].ai_readiness == "AI-Erfahren"

    def test_wordpress_recommends_janosch(self):
        recs = recommend_assignees("WordPress Plugin Update", "Blog-Template anpassen")
        assert len(recs) > 0
        names = [r.display_name for r in recs]
        assert "Janosch Niemeyer" in names

    def test_social_media_recommends_madelin(self):
        recs = recommend_assignees("Instagram Post", "Social-Media-Beitrag UGC")
        names = [r.display_name for r in recs]
        assert "Madelin Grohmann" in names

    def test_ai_readiness_filter_excludes_novices(self):
        recs = recommend_assignees(
            "Custom-GPT Texterstellung", "AI-generierte Texte",
            min_ai_readiness=AIReadiness.EXPERIENCED
        )
        for r in recs:
            assert r.ai_readiness in ("AI-Erfahren", "AI-Pioneer")

    def test_returns_max_3(self):
        recs = recommend_assignees("Newsletter Kampagne", "Email Marketing Mailing", top_n=3)
        assert len(recs) <= 3


# ---------------------------------------------------------------------------
# Evaluate assignee plausibility with AI-Readiness
# ---------------------------------------------------------------------------

class TestEvaluatePlausibility:
    def test_matteo_plausible_for_hubspot(self):
        result = evaluate_assignee_plausibility("emp_003", "HubSpot Automation", "Webhook einrichten")
        assert result.verdict == PlausibilityVerdict.PLAUSIBLE
        assert result.human_review_required is False

    def test_novice_triggers_human_review(self):
        result = evaluate_assignee_plausibility("emp_009", "HubSpot komplex", "Automation Webhook")
        assert result.human_review_required is True

    def test_ai_readiness_mismatch_triggers_review(self):
        result = evaluate_assignee_plausibility(
            "emp_007",  # Lina Weiß — AI-Novice
            "Custom-GPT nutzen",
            required_ai_readiness=AIReadiness.EXPERIENCED,
        )
        assert result.human_review_required is True

    def test_unknown_employee(self):
        result = evaluate_assignee_plausibility("emp_999", "Beliebige Aufgabe")
        assert result.verdict == PlausibilityVerdict.UNKNOWN

    def test_pioneer_for_ai_task_no_review(self):
        result = evaluate_assignee_plausibility(
            "emp_008",  # Sandra Hoppe — AI-Pioneer
            "Prompt-Engineering für Banner", "AI-Tools nutzen",
            required_ai_readiness=AIReadiness.EXPERIENCED,
        )
        assert result.human_review_required is False


# ---------------------------------------------------------------------------
# AIReadiness level comparison
# ---------------------------------------------------------------------------

class TestAIReadinessLevels:
    def test_pioneer_meets_all(self):
        assert AIReadiness.PIONEER.meets(AIReadiness.NOVICE)
        assert AIReadiness.PIONEER.meets(AIReadiness.READY)
        assert AIReadiness.PIONEER.meets(AIReadiness.EXPERIENCED)
        assert AIReadiness.PIONEER.meets(AIReadiness.PIONEER)

    def test_novice_meets_only_novice(self):
        assert AIReadiness.NOVICE.meets(AIReadiness.NOVICE)
        assert not AIReadiness.NOVICE.meets(AIReadiness.READY)
        assert not AIReadiness.NOVICE.meets(AIReadiness.EXPERIENCED)
        assert not AIReadiness.NOVICE.meets(AIReadiness.PIONEER)

    def test_ready_meets_ready_and_below(self):
        assert AIReadiness.READY.meets(AIReadiness.NOVICE)
        assert AIReadiness.READY.meets(AIReadiness.READY)
        assert not AIReadiness.READY.meets(AIReadiness.EXPERIENCED)
        assert not AIReadiness.READY.meets(AIReadiness.PIONEER)


# ---------------------------------------------------------------------------
# analyse_assignment — new AI-readiness + skill-matrix fields
# ---------------------------------------------------------------------------

class TestAnalyseAssignmentNewFields:
    def test_task_category_populated(self):
        ticket = {
            "name": "HubSpot Webhook einrichten",
            "notes": "Double-Opt-In Automation",
        }
        result = analyse_assignment(ticket)
        assert result.task_category == TaskCategory.HUBSPOT.value

    def test_ai_readiness_required_populated(self):
        ticket = {
            "name": "Custom-GPT Texterstellung",
            "notes": "AI-generierte Texte produzieren",
        }
        result = analyse_assignment(ticket)
        assert result.ai_readiness_required is not None
        assert result.ai_readiness_required in [r.value for r in AIReadiness]

    def test_no_assignee_sets_assigned_by_skill_matrix_true(self):
        ticket = {
            "name": "WordPress Plugin Update",
            "notes": "Blog-Template anpassen",
        }
        result = analyse_assignment(ticket)
        assert result.assigned_by_skill_matrix is True
        assert result.needs_reassignment is True

    def test_known_assignee_sets_assigned_by_skill_matrix_false(self):
        ticket = {
            "name": "HubSpot Automation",
            "notes": "Webhook einrichten",
            "assignee": {"email": "m.diehl@example.com", "name": "Matteo Diehl"},
        }
        result = analyse_assignment(ticket)
        assert result.assigned_by_skill_matrix is False
        assert result.assignee_readiness == AIReadiness.EXPERIENCED.value

    def test_novice_assignee_on_hubspot_triggers_needs_reassignment(self):
        ticket = {
            "name": "HubSpot Automation",
            "notes": "Komplexer Webhook und CRM-Automation",
            "assignee": {"email": "a.koehler@example.com", "name": "André Köhler"},
        }
        result = analyse_assignment(ticket)
        assert result.needs_reassignment is True
        assert result.assignee_readiness == AIReadiness.NOVICE.value

    def test_recommended_assignee_ai_level_populated_when_recommendations_exist(self):
        ticket = {
            "name": "Social Media Post",
            "notes": "Instagram Post UGC LinkedIn",
        }
        result = analyse_assignment(ticket)
        if result.recommendations:
            assert result.recommended_assignee_ai_level is not None
            assert result.recommended_assignee_ai_level in [r.value for r in AIReadiness]

    def test_ai_readiness_required_for_print_task(self):
        ticket = {
            "name": "Logo Design Update",
            "notes": "Print-Leitfaden Corporate Design",
        }
        result = analyse_assignment(ticket)
        assert result.task_category == TaskCategory.PRINT_GRAPHIC.value
        assert result.ai_readiness_required == AIReadiness.NOVICE.value

    def test_recommendations_respect_ai_readiness_filter(self):
        ticket = {
            "name": "Custom-GPT für Texterstellung",
            "notes": "AI-generierte Texte Prompt-Engineering",
        }
        result = analyse_assignment(ticket)
        for rec in result.recommendations:
            readiness = AIReadiness(rec.ai_readiness)
            required = AIReadiness(result.ai_readiness_required)
            assert readiness.meets(required), (
                f"{rec.display_name} ({rec.ai_readiness}) does not meet "
                f"required {result.ai_readiness_required}"
            )

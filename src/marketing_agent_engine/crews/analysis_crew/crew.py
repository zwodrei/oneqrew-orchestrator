from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from crewai import Agent, Crew, Process, Task
from crewai.knowledge.source.json_knowledge_source import JSONKnowledgeSource
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent

from marketing_agent_engine.config.llm import get_default_llm
from marketing_agent_engine.config.settings import settings
from .domain_tools import (
    analyse_assignment_tool,
    check_completeness_tool,
    route_ticket_tool,
)

# ---------------------------------------------------------------------------
# Knowledge sources — employee JSON files loaded relative to project root
# ---------------------------------------------------------------------------

_KNOWLEDGE_DIR = Path(__file__).parents[6] / "knowledge"
_EMPLOYEE_FILES = [
    str(p.relative_to(_KNOWLEDGE_DIR))
    for p in (_KNOWLEDGE_DIR / "employees").glob("*.json")
] + ["team_skill_map.json"]

_BRAND_GUIDE_FILES = sorted(
    str(p.relative_to(_KNOWLEDGE_DIR))
    for p in (_KNOWLEDGE_DIR / "brand_guides").glob("*.pdf")
)


def _build_knowledge_sources() -> list:
    sources: list = []
    try:
        sources.append(JSONKnowledgeSource(file_paths=_EMPLOYEE_FILES))
    except Exception:
        pass
    if _BRAND_GUIDE_FILES:
        try:
            sources.append(PDFKnowledgeSource(file_paths=_BRAND_GUIDE_FILES))
        except Exception:
            pass
    return sources


@CrewBase
class AnalysisCrew:
    """
    Four-agent marketing ticket analysis crew.

    Agents:
      1. routing_analyst       — cluster + business unit resolution
      2. assignment_analyst    — assignee plausibility + recommendations
      3. completeness_analyst  — 11-criteria completeness check
      4. decision_synthesizer  — merges all outputs into final JSON decision
    """

    agents: list[BaseAgent]
    tasks: list[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self, ticket: dict[str, Any] | None = None) -> None:
        self._ticket = ticket or {}

    # ------------------------------------------------------------------
    # Agents
    # ------------------------------------------------------------------

    @agent
    def routing_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["routing_analyst"],  # type: ignore[index]
            llm=get_default_llm(),
            tools=[route_ticket_tool],
            verbose=True,
        )

    @agent
    def assignment_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["assignment_analyst"],  # type: ignore[index]
            llm=get_default_llm(),
            tools=[analyse_assignment_tool],
            verbose=True,
        )

    @agent
    def completeness_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["completeness_analyst"],  # type: ignore[index]
            llm=get_default_llm(),
            tools=[check_completeness_tool],
            verbose=True,
        )

    @agent
    def decision_synthesizer(self) -> Agent:
        return Agent(
            config=self.agents_config["decision_synthesizer"],  # type: ignore[index]
            llm=get_default_llm(),
            verbose=True,
        )

    # ------------------------------------------------------------------
    # Tasks
    # ------------------------------------------------------------------

    @task
    def routing_task(self) -> Task:
        return Task(
            config=self.tasks_config["routing_task"],  # type: ignore[index]
        )

    @task
    def assignment_task(self) -> Task:
        return Task(
            config=self.tasks_config["assignment_task"],  # type: ignore[index]
        )

    @task
    def completeness_task(self) -> Task:
        return Task(
            config=self.tasks_config["completeness_task"],  # type: ignore[index]
        )

    @task
    def synthesis_task(self) -> Task:
        return Task(
            config=self.tasks_config["synthesis_task"],  # type: ignore[index]
        )

    # ------------------------------------------------------------------
    # Crew
    # ------------------------------------------------------------------

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            knowledge_sources=_build_knowledge_sources(),
        )

    # ------------------------------------------------------------------
    # Convenience entry-point
    # ------------------------------------------------------------------

    def analyse(self, ticket: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Run the full analysis pipeline for a ticket.

        Returns the parsed JSON decision dict from the synthesizer.
        Falls back to raw string if JSON parse fails.
        """
        target = ticket or self._ticket
        ticket_json = json.dumps(target)
        routing_json = json.dumps({})  # populated by context chain at runtime

        inputs = {
            "ticket_json": ticket_json,
            "routing_result_json": routing_json,
            "dry_run": str(settings.dry_run).lower(),
            "model": settings.model,
        }

        raw_result = self.crew().kickoff(inputs=inputs)
        raw = str(raw_result)

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # Synthesizer may have wrapped in markdown fences — strip and retry
            cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError:
                return {"raw_output": raw, "parse_error": "Could not parse synthesizer JSON"}

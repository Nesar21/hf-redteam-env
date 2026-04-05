"""Pydantic v2 models for Red-Team OpenEnv."""

from typing import Any, Dict, Optional

from openenv.core.env_server.types import Action, Observation


class RedTeamAction(Action):
    """Agent sends a message to the defender."""
    message: str


class RedTeamObservation(Observation):
    """What the agent sees after each step."""
    defender_response: str = ""
    task_id: str = ""
    turn: int = 0
    max_turns: int = 10
    info: str = ""

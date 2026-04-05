"""Abstract base class for all tasks."""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple


class BaseTask(ABC):
    """Every task implements these properties and methods."""

    @property
    @abstractmethod
    def task_id(self) -> str:
        ...

    @property
    @abstractmethod
    def secret(self) -> str:
        ...

    @property
    @abstractmethod
    def system_description(self) -> str:
        """Shown to the agent on reset as the 'info' field."""
        ...

    @property
    @abstractmethod
    def refusal_patterns(self) -> List[str]:
        """Lowercase words/phrases that trigger defender refusal."""
        ...

    @property
    @abstractmethod
    def vulnerability_patterns(self) -> List[str]:
        """Lowercase words/phrases that make the defender leak."""
        ...

    @property
    @abstractmethod
    def partial_reward_keywords(self) -> List[str]:
        """Lowercase keywords in attacker message that earn +0.3."""
        ...

    def filter_output(self, raw_response: str) -> str:
        """Post-process defender output. Override for output filtering."""
        return raw_response

    def pre_step_check(self, message: str, history: List[Dict]) -> Tuple[bool, str]:
        """Pre-step validation. Returns (passed, status_label)."""
        return True, ""

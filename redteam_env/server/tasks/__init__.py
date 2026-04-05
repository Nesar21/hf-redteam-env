"""Task registry."""

from .task_easy import TaskEasy
from .task_medium import TaskMedium
from .task_hard import TaskHard

TASK_REGISTRY = {
    "task_easy": TaskEasy(),
    "task_medium": TaskMedium(),
    "task_hard": TaskHard(),
}

TASK_IDS = list(TASK_REGISTRY.keys())

"""Red-Team Environment Client."""

from openenv.core.env_client import EnvClient
from .models import RedTeamAction, RedTeamObservation


class RedTeamEnv(EnvClient):
    """Client for connecting to a Red-Team Environment server."""

    ACTION_CLS = RedTeamAction
    OBSERVATION_CLS = RedTeamObservation

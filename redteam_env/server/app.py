"""FastAPI application — stateful singleton for Red-Team Environment."""

from typing import Any, Dict, Optional

from fastapi import FastAPI
from pydantic import BaseModel

from ..models import RedTeamAction
from .environment import RedTeamEnvironment

app = FastAPI(title="Red-Team OpenEnv", version="1.0.0")

# Singleton — one live env instance that persists state across HTTP calls
_env = RedTeamEnvironment()


class ResetBody(BaseModel):
    task_id: str = "task_easy"
    seed: Optional[int] = None
    episode_id: Optional[str] = None


class StepBody(BaseModel):
    action: Dict[str, Any]


@app.get("/")
def read_root():
    return {
        "title": "Red-Team OpenEnv",
        "status": "Online",
        "description": "API is running. See POST /reset and POST /step for interactions."
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/reset")
def reset(body: Optional[ResetBody] = None):
    body = body or ResetBody()
    obs = _env.reset(
        seed=body.seed,
        episode_id=body.episode_id,
        task_id=body.task_id,
    )
    return {
        "observation": obs.model_dump(exclude={"done", "reward", "metadata"}),
        "reward": obs.reward,
        "done": obs.done,
    }


@app.post("/step")
def step(body: StepBody):
    action = RedTeamAction.model_validate(body.action)
    obs = _env.step(action)
    return {
        "observation": obs.model_dump(exclude={"done", "reward", "metadata"}),
        "reward": obs.reward,
        "done": obs.done,
    }


@app.get("/state")
def state():
    return _env.state.model_dump()


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()

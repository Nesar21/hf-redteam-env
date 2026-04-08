"""FastAPI application — stateful singleton for Red-Team Environment."""
import logging
from typing import Any, Dict, Optional

from fastapi import FastAPI, Request
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
async def reset(request: Request):
    try:
        data = await request.json()
    except Exception as e:
        logging.warning(f"Malformed /reset payload received (returning default state). Error: {e}")
        data = {}
        
    body = ResetBody(**data)
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

from fastapi import FastAPI
from env import StudyPlannerEnv, Action

app = FastAPI()

env = StudyPlannerEnv()

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/reset")
def reset():
    obs = env.reset()
    return obs.dict()

@app.post("/step")
def step(action: Action):

    obs, reward, done, _ = env.step(action)

    return {
        "observation": obs.dict(),
        "reward": reward,
        "done": done,
        "info": {}
    }

@app.get("/state")
def state():
    return env.state().dict()

from abc import abstractmethod
from typing import Any, Optional, Dict
from openenv.core import Action, Environment, Observation, State

class SimpleState(State):
    pass

class SimpleEnv(Environment):
    def reset(self, seed=None, episode_id=None, **kwargs) -> Observation:
        return Observation(message="Hello")

    def step(self, action, timeout_s=None, **kwargs) -> Observation:
        return Observation(message="World", done=True)

    @property
    def state(self) -> State:
        return SimpleState()

if __name__ == "__main__":
    try:
        env = SimpleEnv()
        print("Success!")
    except TypeError as e:
        print(f"Failed: {e}")

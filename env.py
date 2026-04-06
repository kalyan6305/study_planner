from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from openenv.core import Action, Environment, Observation, State

# --- Models for RL Agent Training ---

class StudyTask(BaseModel):
    id: int
    title: str
    priority: int = 1
    duration_hours: float
    deadline_hours: float
    status: str = "pending"

class StudyAction(Action):
    action_type: str = Field(..., description="study, break, or sleep")
    task_id: Optional[int] = Field(None, description="ID of task to study")

class StudyObservation(Observation):
    current_hour: float = 0.0
    energy: float = 100.0
    knowledge: float = 0.0
    remaining_tasks: List[StudyTask] = []
    message: str = ""

class StudyState(State):
    current_hour: float = 0.0
    energy: float = 100.0
    knowledge: float = 0.0
    tasks: List[StudyTask] = []

class DeepStudyPlanner(Environment):
    """Hackathon-Grade OpenEnv Environment for Study Planning."""
    
    def __init__(self):
        super().__init__()
        self._energy: float = 100.0
        self._knowledge: float = 0.0
        self._current_hour: float = 0.0
        self._tasks: List[StudyTask] = []
        self._max_hours: float = 24.0

    def reset(self, seed: Optional[int] = None, episode_id: Optional[str] = None, **kwargs: Any) -> StudyObservation:
        self._energy = 100.0
        self._knowledge = 0.0
        self._current_hour = 0.0
        self._tasks = [
            StudyTask(id=1, title="Math Exam", duration_hours=3.0, deadline_hours=8.0, priority=5),
            StudyTask(id=2, title="Physics Lab", duration_hours=4.0, deadline_hours=12.0, priority=4),
            StudyTask(id=3, title="React App", duration_hours=5.0, deadline_hours=20.0, priority=3),
        ]
        return self._get_obs("Environment reset.")

    def step(self, action: Union[StudyAction, Dict[str, Any]], timeout_s: Optional[float] = None, **kwargs: Any) -> StudyObservation:
        if isinstance(action, dict):
            action = StudyAction(**action)

        reward = 0.0
        msg = ""
        done = False

        self._current_hour += 1.0
        if self._current_hour >= self._max_hours:
            done = True

        if action.action_type == "study":
            task = next((t for t in self._tasks if t.id == action.task_id), None)
            if task and task.status == "pending":
                gain = (self._energy / 100.0) * task.priority
                self._knowledge += gain
                self._energy -= 15.0
                reward = gain
                msg = f"Studying {task.title}."
            else:
                reward = -2.0
                msg = "Invalid task."
        elif action.action_type == "break":
            self._energy = min(100.0, self._energy + 10.0)
            reward = 0.5
            msg = "Short break."
        elif action.action_type == "sleep":
            self._energy = min(100.0, self._energy + 40.0)
            self._current_hour += 2.0
            reward = 1.0
            msg = "Sleeping."

        self._energy = max(0.0, self._energy)
        
        for task in self._tasks:
            if self._current_hour > task.deadline_hours and task.status == "pending":
                reward -= 10.0
                task.status = "missed"
                msg += " MISSED DEADLINE!"

        obs = self._get_obs(msg)
        obs.reward = float(reward)
        obs.done = done
        return obs

    def _get_obs(self, message: str) -> StudyObservation:
        return StudyObservation(
            current_hour=self._current_hour,
            energy=self._energy,
            knowledge=self._knowledge,
            remaining_tasks=[t for t in self._tasks if t.status == "pending"],
            message=message,
            done=self._current_hour >= self._max_hours
        )

    @property
    def state(self) -> StudyState:
        return StudyState(
            current_hour=self._current_hour,
            energy=self._energy,
            knowledge=self._knowledge,
            tasks=self._tasks
        )

if __name__ == "__main__":
    env = DeepStudyPlanner()
    print("Instance created!")
    obs = env.reset()
    print("Reset successful!")

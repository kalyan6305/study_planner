import random
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, ConfigDict
from openenv.core import Action, Environment, Observation, State
from openenv.core.rubrics.base import Rubric

# --- MODELS ---

class StudyTask(BaseModel):
    id: int
    title: str
    priority: int = 1
    duration_hours: float
    deadline_hours: float
    status: str = "pending"

class StudyAction(Action):
    action_type: str
    task_id: Optional[int] = None

class StudyObservation(Observation):
    model_config = ConfigDict(extra="allow") # Allow extra fields like energy
    current_hour: float = 0.0
    energy: float = 100.0
    knowledge: float = 0.0
    remaining_tasks: List[StudyTask] = []
    message: str = ""

# --- ENVIRONMENT ---

class StudyEnv(Environment):
    """A professional Study Planning environment for OpenEnv."""
    
    def __init__(self):
        super().__init__()
        self._energy = 100.0
        self._knowledge = 0.0
        self._current_hour = 0.0
        self._tasks = []
        self._max_hours = 24.0

    def reset(self, seed=None, episode_id=None, **kwargs) -> StudyObservation:
        self._energy = 100.0
        self._knowledge = 0.0
        self._current_hour = 0.0
        self._tasks = [
            StudyTask(id=1, title="Math Exam", duration_hours=3.0, deadline_hours=8.0, priority=5),
            StudyTask(id=2, title="Physics Lab", duration_hours=4.0, deadline_hours=12.0, priority=4),
            StudyTask(id=3, title="React App", duration_hours=5.0, deadline_hours=20.0, priority=3),
        ]
        return self._make_obs("Hackathon Challenge Started!")

    def step(self, action: Union[StudyAction, Dict[str, Any]], timeout_s=None, **kwargs) -> StudyObservation:
        if isinstance(action, dict): action = StudyAction(**action)
        
        self._current_hour += 1.0
        msg = f"Action: {action.action_type}"
        
        if action.action_type == "study":
            task = next((t for t in self._tasks if t.id == action.task_id), None)
            if task and task.status == "pending":
                gain = (self._energy / 100.0) * task.priority
                self._knowledge += gain
                self._energy = max(0, self._energy - 15)
                msg = f"Studied {task.title}. Knowledge +{gain:.1f}"
        elif action.action_type == "break":
            self._energy = min(100.0, self._energy + 15)
            msg = "Short rest. Energy +15"
        elif action.action_type == "sleep":
            self._energy = 100.0
            self._current_hour += 4.0
            msg = "Deep sleep. Energy Refilled."

        # Check Deadlines
        for t in self._tasks:
            if self._current_hour > t.deadline_hours and t.status == "pending":
                t.status = "missed"
                msg += f" MISSED: {t.title}"

        obs = self._make_obs(msg)
        return obs

    def _make_obs(self, message: str) -> StudyObservation:
        done = self._current_hour >= self._max_hours
        return StudyObservation(
            current_hour=self._current_hour,
            energy=self._energy,
            knowledge=self._knowledge,
            remaining_tasks=[t for t in self._tasks if t.status == "pending"],
            message=message,
            done=done,
            reward=float(self._knowledge)
        )

    @property
    def state(self) -> State:
        """Required by OpenEnv API."""
        return State(metadata={"energy": self._energy, "knowledge": self._knowledge})

# --- DEMO ---

def run_hackathon():
    print("🎓 DEEP STUDY PLANNER | OPENENV HACKATHON 🎓\n")
    env = StudyEnv()
    obs = env.reset()
    
    while not obs.done:
        # Simple Agent: Work if energy > 50, otherwise rest
        if obs.energy > 50:
            tid = obs.remaining_tasks[0].id if obs.remaining_tasks else 1
            action = StudyAction(action_type="study", task_id=tid)
        else:
            action = StudyAction(action_type="break")
            
        obs = env.step(action)
        print(f"[{obs.current_hour:02.0f}h] {obs.message} | Knowledge: {obs.knowledge:.1f} | Energy: {obs.energy:.0f}%")

    print(f"\n✅ Simulation Finished. Total Knowledge Gained: {obs.knowledge:.1f}")

if __name__ == "__main__":
    run_hackathon()

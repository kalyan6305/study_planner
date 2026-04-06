from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from openenv.core.rubrics.base import Rubric
from env import StudyAction, StudyObservation, StudyTask

class GraderReport(BaseModel):
    efficiency_score: float = 0.0
    deadline_penalty: float = 0.0
    total_knowledge: float = 0.0
    final_grade: str = "F"

class StudyPlannerRubric(Rubric):
    """
    Formal Rubric for the DeepStudyPlanner environment.
    Evaluates the trajectory of an agent's study habits.
    """
    
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self) -> None:
        """Reset the rubric state for a new episode."""
        self.history = []

    def __call__(self, action: Any, observation: Any) -> float:
        """Calculate the instantaneous reward for a step."""
        # Convert to models if necessary
        if isinstance(action, dict): action = StudyAction(**action)
        if isinstance(observation, dict): observation = StudyObservation(**observation)
        
        # 1. Base Knowledge Gain (The primary objective)
        reward = observation.reward # Provided by env based on energy
        
        # 2. Penalty for very low energy (Fatigue check)
        if observation.energy < 20.0:
            reward -= 5.0 # Burnout penalty
            
        # 3. Completion Bonus
        if observation.done:
            if observation.knowledge > 20.0:
                reward += 50.0 # High Achievement Bonus
            elif observation.knowledge > 10.0:
                reward += 20.0 # Passing Grade Bonus
        
        return float(reward)

    def calculate_final_grade(self, state: Dict[str, Any]) -> GraderReport:
        """Final summary of the episode performance."""
        knowledge = state.get("knowledge", 0.0)
        
        if knowledge >= 30: grade = "A+"
        elif knowledge >= 20: grade = "B"
        elif knowledge >= 10: grade = "C"
        else: grade = "F"
        
        return GraderReport(
            total_knowledge=knowledge,
            final_grade=grade
        )

# Example usage for training
def get_grader():
    return StudyPlannerRubric()

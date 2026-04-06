import json
import random
from env import DeepStudyPlanner, StudyAction
from graders import StudyPlannerRubric

def simulate_hackathon_agent():
    """
    Simulation of an RL-style agent training on the DeepStudyPlanner environment.
    """
    print("🎓 --- DeepStudyPlanner: Hackathon ML Simulation --- 🎓\n")
    
    env = DeepStudyPlanner()
    rubric = StudyPlannerRubric()
    
    obs = env.reset()
    total_reward = 0
    step = 0
    
    print(f"Initial State: Energy: {obs.energy}%, Tasks: {len(obs.remaining_tasks)}")

    while not obs.done:
        step += 1
        
        # --- Simple Heuristic Agent Logic ---
        if obs.energy < 30:
            action_type = random.choice(["break", "sleep"])
            task_id = None
        else:
            action_type = "study"
            # Pick first available task
            task_id = obs.remaining_tasks[0].id if obs.remaining_tasks else 1
            
        action = StudyAction(action_type=action_type, task_id=task_id)
        
        # --- Interaction ---
        obs = env.step(action)
        
        # --- Reward Calculation (Rubric) ---
        reward = rubric(action, obs)
        total_reward += reward
        
        print(f"[{obs.current_hour}h] Action: {action_type} -> {obs.message} | Reward: {reward:.1f}")

    # --- Final Grading ---
    report = rubric.calculate_final_grade(env.state.model_dump())
    print("\n--- 🏁 HACKATHON PERFORMANCE REPORT ---")
    print(f"Knowledge Gained: {report.total_knowledge:.1f}")
    print(f"Cumulative Reward: {total_reward:.1f}")
    print(f"FINAL GRADE: {report.final_grade}")
    print("---------------------------------------")

if __name__ == "__main__":
    simulate_hackathon_agent()
    print("\nNext: Upgrade dashboard.html to visualize Energy and Knowledge!")

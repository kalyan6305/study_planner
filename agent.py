import os
import asyncio
from datetime import datetime, timedelta
from env import StudyPlannerEnv

class MockLLMClient:
    """A mock LLM client for when API keys are not available."""
    async def complete(self, prompt: str) -> str:
        # Simple rule-based mock logic
        if "math" in prompt.lower():
            return '{"type": "add_task", "payload": {"title": "Math Revision", "duration": 2.5}}'
        elif "physics" in prompt.lower():
            return '{"type": "add_task", "payload": {"title": "Physics Problem Set", "duration": 3.0}}'
        elif "schedule" in prompt.lower():
            return '{"type": "schedule_tasks", "payload": {}}'
        return '{"type": "add_task", "payload": {"title": "Manual Study Task", "duration": 1.0}}'

class StudyAgent:
    def __init__(self, env: StudyPlannerEnv):
        self.env = env
        self.llm = MockLLMClient()

    async def chat(self, user_input: str):
        print(f"\nUser: {user_input}")
        
        # In a real app, we would send this to the LLM
        # response = await self.llm.complete(user_input)
        
        # For this demo, let's parse manual commands or simulate LLM actions
        if "schedule" in user_input.lower():
            action = {"type": "schedule_tasks", "payload": {}}
        elif "export" in user_input.lower():
             action = {"type": "generate_ics", "payload": {}}
        elif "add" in user_input.lower():
            # Basic parsing: "Add [Title] for [hours]"
            parts = user_input.split()
            title = parts[1] if len(parts) > 1 else "New Task"
            duration = float(parts[-1]) if parts[-1].replace('.', '').isdigit() else 2.0
            action = {"type": "add_task", "payload": {"title": title, "duration": duration}}
        else:
            print("Agent: I'm not sure how to help with that. Try 'Add Math 2', 'Schedule', or 'Export'.")
            return

        result = self.env.step(action)
        print(f"Agent: {result.message}")
        
        if result.ics_content:
            with open("study_plan.ics", "w") as f:
                f.write(result.ics_content)
            print("Agent: Success! Your calendar file 'study_plan.ics' has been generated.")

async def main():
    env = StudyPlannerEnv()
    env.reset()
    agent = StudyAgent(env)
    
    print("--- Welcome to Study Planner AI Agent ---")
    print("You can say things like:")
    print(" - 'Add Math 4'")
    print(" - 'Schedule my week'")
    print(" - 'Export to calendar'")
    print(" - 'exit' to stop")
    
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            await agent.chat(user_input)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())

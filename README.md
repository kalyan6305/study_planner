# Study Planner OpenEnv

An environment for evaluating AI agents on study planning and scheduling tasks, built with the [OpenEnv](https://github.com/meta-pytorch/OpenEnv) framework.

## Project Structure

- `env.py`: Defines the `StudyPlannerEnv` class, supporting actions to manage study tasks and schedules.
- `tasks.py`: Predefined study tasks used during evaluation.
- `graders.py`: Grading logic to evaluate agent performance based on schedule efficiency and task completion.
- `inference.py`: Script to simulate agent interaction with the environment.
- `openenv.yaml`: Metadata and configuration for the OpenEnv SDK.
- `Dockerfile`: Containerization setup for the environment.

## Usage

### Prerequisites
- Python 3.10+
- OpenEnv SDK

### Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Environment
You can run the environment locally for testing:
```bash
python env.py
```

### Running Inference
To simulate an agent interacting with the environment:
```bash
python inference.py
```

## Grading
The `StudyGrader` in `graders.py` evaluates the agent's ability to:
- Include all necessary tasks in the schedule.
- Respect deadlines.
- Optimize study time allocation.

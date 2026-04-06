from datetime import datetime, timedelta

TASKS = [
    {
        "id": 1,
        "title": "Study Linear Algebra",
        "description": "Cover chapters 1-3 of the textbook.",
        "duration": 3.0,
        "deadline": (datetime.now() + timedelta(days=2)).isoformat()
    },
    {
        "id": 2,
        "title": "Finish Physics Assignment",
        "description": "Complete problem set on electromagnetism.",
        "duration": 4.0,
        "deadline": (datetime.now() + timedelta(days=1)).isoformat()
    },
    {
        "id": 3,
        "title": "React Project",
        "description": "Implement the authentication flow.",
        "duration": 5.0,
        "deadline": (datetime.now() + timedelta(days=5)).isoformat()
    }
]

def get_task_by_id(task_id: int):
    for task in TASKS:
        if task["id"] == task_id:
            return task
    return None

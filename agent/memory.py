import json
import os

MEMORY_FILE = "data/memory.json"

def save_memory(task, results):
    """
    Persist task execution results to memory.
    """
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            try:
                memory = json.load(f)
            except json.JSONDecodeError:
                memory = []
    else:
        memory = []

    memory.append({
        "task": task,
        "results": results
    })

    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

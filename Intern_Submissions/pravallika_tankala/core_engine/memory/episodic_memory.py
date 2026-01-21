import json
import os

class EpisodicMemory:
    def __init__(self, vector_store=None):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(base_dir, "episodic_memory.json")
        self.vector_store = vector_store

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump([], f)

    def save(self, step, result):
        with open(self.file_path, "r") as f:
            data = json.load(f)

        entry = {
            "step": step,
            "result": result
        }
        data.append(entry)

        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=2)

       
        if self.vector_store:
            
            combined_text = f"STEP: {step}\nRESULT:\n{result}"
            self.vector_store.add(combined_text)


    def load_all(self):
        with open(self.file_path, "r") as f:
            return json.load(f)

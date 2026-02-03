class CostTracker:
    def __init__(self, max_steps=8):
        self.steps = 0
        self.max_steps = max_steps

    def tick(self):
        self.steps += 1
        if self.steps > self.max_steps:
            raise Exception(
                "Maximum execution steps exceeded — human escalation required"
            )

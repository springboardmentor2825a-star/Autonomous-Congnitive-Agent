class ResearchMemory:
    def __init__(self):
        self.logs = []

    def store(self, entry):
        self.logs.append(entry)

    def retrieve_all(self):
        return self.logs

    def clear(self):
        self.logs = []

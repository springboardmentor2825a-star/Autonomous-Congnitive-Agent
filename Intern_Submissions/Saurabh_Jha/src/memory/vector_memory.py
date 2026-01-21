import faiss
from sentence_transformers import SentenceTransformer


class VectorMemory:
    """
    Vector-based long-term memory for evidence storage and retrieval.
    """

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.IndexFlatL2(384)
        self.texts = []

    def add(self, text: str):
        """
        Store a piece of evidence in memory.
        """
        vector = self.model.encode([text])
        self.index.add(vector)
        self.texts.append(text)

    def retrieve(self, query: str, k: int = 3):
        """
        Retrieve top-k relevant memory items for a query.
        """
        if not self.texts:
            return []

        vector = self.model.encode([query])
        _, indices = self.index.search(vector, k)

        return [self.texts[i] for i in indices[0]]

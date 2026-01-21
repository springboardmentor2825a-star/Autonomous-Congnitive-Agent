def retrieve(vector_store, query, limit=2):
    """
    Semantic RAG using FAISS + Sentence Transformers
    """
    return vector_store.search(query, top_k=limit)

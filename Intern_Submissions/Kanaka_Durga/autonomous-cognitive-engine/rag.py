from llm import GeminiLLM
from typing import List, Dict

class RAGSystem:
    """Retrieval Augmented Generation system for enhanced research"""
    
    def __init__(self, llm: GeminiLLM):
        self.llm = llm
        self.knowledge_base = []
    
    def add_to_knowledge_base(self, document: str, source: str = ""):
        """Add document to knowledge base"""
        self.knowledge_base.append({
            'content': document,
            'source': source
        })
    
    def retrieve_relevant_context(self, query: str, top_k: int = 3) -> str:
        """Retrieve relevant context from knowledge base"""
        if not self.knowledge_base:
            return "No documents in knowledge base."
        
        # Simple relevance scoring based on keyword overlap
        query_words = set(query.lower().split())
        scores = []
        
        for i, doc in enumerate(self.knowledge_base):
            doc_words = set(doc['content'].lower().split())
            overlap = len(query_words & doc_words)
            scores.append((overlap, i))
        
        scores.sort(reverse=True)
        top_docs = scores[:top_k]
        
        context = "\n---\n".join([
            f"Source: {self.knowledge_base[idx]['source']}\n{self.knowledge_base[idx]['content']}"
            for _, idx in top_docs
        ])
        
        return context if context else "No relevant documents found."
    
    def augment_query_with_context(self, query: str) -> str:
        """Augment query with retrieved context"""
        context = self.retrieve_relevant_context(query)
        return f"Query: {query}\n\nRelevant Context:\n{context}"
    
    def generate_with_augmentation(self, query: str, prompt_template: str) -> str:
        """Generate response with RAG augmentation"""
        augmented_query = self.augment_query_with_context(query)
        full_prompt = prompt_template.format(query=augmented_query)
        return self.llm.generate(full_prompt)
    
    def summarize_knowledge_base(self) -> str:
        """Get summary of current knowledge base"""
        if not self.knowledge_base:
            return "Knowledge base is empty."
        
        summary = f"Total documents: {len(self.knowledge_base)}\n"
        summary += "\nDocuments:\n"
        for i, doc in enumerate(self.knowledge_base):
            preview = doc['content'][:100] + "..." if len(doc['content']) > 100 else doc['content']
            summary += f"{i+1}. Source: {doc['source']}\n   Preview: {preview}\n"
        
        return summary

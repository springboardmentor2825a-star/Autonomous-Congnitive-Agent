from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    return ChatGroq(
        model="qwen/qwen3-32b"
    )

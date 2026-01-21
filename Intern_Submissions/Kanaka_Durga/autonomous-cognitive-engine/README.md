# 🧠 Autonomous Cognitive Engine for Deep Research

An advanced AI-powered research engine that conducts comprehensive research on any topic using multiple specialized agents working together in a coordinated pipeline.

## Architecture Overview

```
Input Query
    ↓
[PLANNER] - Creates research plan & breaks down query
    ↓
[RESEARCHER] - Conducts deep research & analyzes findings
    ↓
[WRITER] - Creates comprehensive answer
    ↓
[CRITIC] - Evaluates & suggests improvements (optional)
    ↓
Final Answer
```

## Features

✨ **Multi-Agent System:**
- **Planner Agent**: Creates detailed research plans
- **Researcher Agent**: Conducts deep research and analysis
- **Writer Agent**: Composes comprehensive, well-structured answers
- **Critic Agent**: Evaluates responses and suggests improvements
- **Memory System**: Maintains conversation history and research findings
- **RAG System**: Retrieval-Augmented Generation for enhanced accuracy

🎯 **Capabilities:**
- Deep research on complex topics
- Chain-of-thought reasoning
- Multi-hop reasoning
- Long-form content generation
- Fact verification
- Response evaluation and improvement

## Setup Instructions

### 1. Get Free Gemini API Key
- Visit: https://ai.google.dev
- Click "Get API Key"
- Create a new API key (free tier available)

### 2. Create Project Structure
```bash
mkdir ace
cd ace
```

### 3. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment
```bash
# Create .env file
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_actual_api_key_here
```

### 6. Run the Application
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Project Structure

```
ace/
├── app.py                 # Streamlit UI application
├── engine.py              # Main orchestrator engine
├── llm.py                 # LLM integration (Gemini)
├── rag.py                 # RAG system implementation
├── agents/
│   ├── __init__.py
│   ├── planner.py        # Planning agent
│   ├── researcher.py     # Research agent
│   ├── writer.py         # Writing agent
│   ├── critic.py         # Critic agent
│   └── memory.py         # Memory management
├── requirements.txt      # Dependencies
├── .env.example          # Environment template
└── README.md             # This file
```

## Usage Guide

### Basic Query
1. Open the Streamlit app
2. Enter your research question in the input field
3. Click "🚀 Research"
4. View results in different tabs

### Enable/Disable Critic Agent
- Toggle in the sidebar to enable or disable response evaluation
- Helps improve answer quality through feedback

### Add Knowledge Documents
- Use the sidebar to add documents to the knowledge base
- Documents are used for RAG-enhanced generation

### Memory Management
- View engine status in sidebar
- Clear memory when starting a new research session

## Example Queries

- "What are the latest developments in quantum computing?"
- "How does machine learning impact financial markets?"
- "Explain the economic implications of renewable energy adoption"
- "What are the current challenges in autonomous vehicles?"
- "Analyze the impact of AI on job markets"

## Features Explanation

### Planner Agent
- Breaks down complex queries into sub-questions
- Creates structured research plans
- Identifies key research areas

### Researcher Agent
- Conducts comprehensive research
- Analyzes findings contextually
- Fact-checks claims
- Provides evidence and examples

### Writer Agent
- Composes well-structured answers
- Creates summaries at different lengths
- Formats content for presentation

### Critic Agent
- Evaluates response quality
- Identifies gaps and weaknesses
- Suggests specific improvements
- Ensures comprehensive coverage

### Memory System
- Tracks conversation history
- Stores research findings
- Maintains planning steps
- Provides context for multi-turn conversations

### RAG System
- Stores documents in knowledge base
- Retrieves relevant context for queries
- Enhances generation with external knowledge

## API Usage

The Gemini API free tier includes:
- Unlimited requests for text generation
- 1500 requests per minute limit
- 32k token input limit
- 8k token output limit

## Troubleshooting

**Issue: "GEMINI_API_KEY not found"**
- Ensure .env file exists with your API key
- Restart the Streamlit app

**Issue: API rate limiting**
- Wait a few minutes before making new requests
- Reduce output token limit if needed

**Issue: Slow responses**
- This is normal for complex research queries
- Larger responses take more time to generate

## Tips for Best Results

1. **Be Specific**: More detailed queries produce better results
2. **Enable Critic**: Helps ensure comprehensive answers
3. **Add Context**: Use the knowledge base for domain-specific queries
4. **Review Sections**: Check different tabs for complete information
5. **Download Results**: Save important answers for later reference

## Requirements

- Python 3.8+
- Gemini API Key (free)
- Internet connection

## Project Status

✅ Complete and working
✅ Free API integration
✅ Streamlit UI
✅ Multi-agent system
✅ Memory management
✅ RAG system

## Support

For issues or questions:
1. Check the troubleshooting section
2. Verify your API key is correct
3. Ensure all dependencies are installed
4. Check internet connection

## License

This project is for educational purposes (Infosys Virtual Internship)

---

**Created for:** Infosys Virtual Internship
**Technology:** Python, Streamlit, Google Gemini API
**Purpose:** Deep Research & Autonomous Cognitive Tasks

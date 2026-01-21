from agent.controller import AutonomousAgent
from agent.tools import ask_openai, analyze_sentiment

def main():
    task = "Analyze retail sales data and suggest improvements"

    print("Starting Autonomous Cognitive Agent...\n")
    print("Task:", task)

    # Run agent pipeline
    agent = AutonomousAgent(task)
    results, reflection = agent.run()

    print("\nExecution Results:")
    for r in results:
        print("-", r)

    print("\nAgent Reflection:")
    print(reflection)

    # Demonstrate OpenAI LLM simulation
    llm_response = ask_openai("Suggest top 2 products to promote")
    print("\nOpenAI LLM Simulation:")
    print(llm_response)

    # Demonstrate Hugging Face sentiment analysis
    sample_text = "The sales report shows good growth but some products are underperforming."
    sentiment = analyze_sentiment(sample_text)
    print("\nHugging Face Sentiment Analysis:")
    print(sentiment)

if __name__ == "__main__":
    main()

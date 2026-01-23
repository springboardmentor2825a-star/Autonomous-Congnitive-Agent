from litellm import completion
from dotenv import load_dotenv

load_dotenv()

def ask_llm(prompt):
    for model in ["openai/gpt-4o-mini"]:
        try:
            response = completion(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                max_iter = 1
            )
            print(f"Response from {model}")
            return response
        except Exception as e:
            print(f"{model} failed:", e)

    raise RuntimeError("All LLMs failed")

response = ask_llm("Explain Machine Learning in simple Hinglish")
print(response.choices[0].message.content)

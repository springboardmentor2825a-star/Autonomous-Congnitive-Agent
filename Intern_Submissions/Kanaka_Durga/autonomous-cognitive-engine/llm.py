import google.generativeai as genai
from typing import Generator


class GeminiLLM:
    def __init__(self, api_key: str):
        # Configure API key
        genai.configure(api_key=api_key)

        # ✅ Use a model that ACTUALLY EXISTS in your project
        self.model = genai.GenerativeModel(
            model_name="models/gemini-2.5-flash-lite"
        )

    def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate text using Gemini 2.5 Flash"""
        try:
            response = self.model.generate_content(
                contents=prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=4096,  # safe default
                    top_p=0.95,
                    top_k=64
                )
            )

            # Safety: response.text can be None in rare cases
            return response.text if response.text else ""

        except Exception as e:
            return f"Error generating response: {str(e)}"

    def generate_streaming(
        self,
        prompt: str,
        temperature: float = 0.7
    ) -> Generator[str, None, None]:
        """Generate text with streaming support"""
        try:
            response = self.model.generate_content(
                contents=prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=4096,
                    top_p=0.95,
                    top_k=64
                ),
                stream=True
            )

            for chunk in response:
                if hasattr(chunk, "text") and chunk.text:
                    yield chunk.text

        except Exception as e:
            yield f"Error: {str(e)}"

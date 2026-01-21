from google import genai


class GeminiTool:
    def __init__(self, api_key):
        # Initialize Gemini client
        self.client = genai.Client(
            api_key=api_key
        )

    def generate(self, prompt):
        # Generate response from Gemini
        response = self.client.models.generate_content(
            model="models/gemini-flash-lite-latest",
            contents=prompt
        )
        return response.text

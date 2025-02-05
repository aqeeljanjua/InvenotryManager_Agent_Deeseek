import ollama
from typing import Any

class OllamaAgent:
    def __init__(self, session_id: str):
        self.model = "deepseek-r1:14b"
        # self.model = "llama2:7b"
        self.session_id = session_id

    def chat(self, system_prompt: str, user_query: str) -> str:
        try:
            response = ollama.chat(model=self.model, messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ])
            return response['message']['content'].strip()
        except Exception as e:
            print(f"Ollama error: {e}")
            return f"Error processing request: {str(e)}"

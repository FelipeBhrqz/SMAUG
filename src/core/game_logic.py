import os
from openai import OpenAI

class SmaugGuardian:
    def __init__(self, use_local=True):
        if use_local:
            print("Conectando con OLLAMA (Local)...")
            self.client = OpenAI(
                base_url="http://localhost:11434/v1",
                api_key="ollama" 
            )
            self.model = "llama3.1" 

    def get_response(self, user_input, system_prompt):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7,
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error de conexión con SMAUG: {e}"
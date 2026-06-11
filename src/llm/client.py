import os

from dotenv import load_dotenv
from openai import OpenAI


class LLMClient:

    def __init__(self):

        load_dotenv()

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY no encontrada en el archivo .env"
            )

        self.model = "llama-3.3-70b-versatile"

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )

    def generate(
        self,
        prompt: str,
        temperature: float = 0.0
    ) -> str:

        try:

            response = self.client.chat.completions.create(
                model=self.model,
                temperature=temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            content = response.choices[0].message.content
            if not content:
                raise ValueError("No se obtuvo una respuesta válida del modelo.")

            return content

        except Exception as e:

            raise RuntimeError(
                f"Error comunicándose con Groq: {e}"
            )

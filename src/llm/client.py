from ollama import chat


class LLMClient:

    def __init__(self):

        self.model = "gemma4:e4b"

    def generate(
        self,
        prompt: str,
        temperature: float = 0.0
    ) -> str:

        response = chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": temperature
            }
        )

        return response["message"]["content"]

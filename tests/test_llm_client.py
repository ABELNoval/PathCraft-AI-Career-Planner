from src.llm.client import LLMClient

client = LLMClient()

response = client.generate(
    "Respond only with SUCCESS"
)

print(response)

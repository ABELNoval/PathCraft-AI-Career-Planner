from src.llm.client import LLMClient

client = LLMClient()

response = client.generate(
    "Say hello in one sentence."
)

print(response)

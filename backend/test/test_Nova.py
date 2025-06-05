from huggingface_hub import InferenceClient
import os

client = InferenceClient(
    provider="nebius",
    api_key=os.getenv("HUGGINGFACE_API_KEY"),
)

completion = client.chat.completions.create(
    model="Qwen/Qwen2.5-32B-Instruct",
    messages=[{"role": "user", "content": "人生に愛は必要ですか？"}],
)

print(completion.choices[0].message)

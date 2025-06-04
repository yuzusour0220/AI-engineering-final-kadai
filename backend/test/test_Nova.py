from huggingface_hub import InferenceClient
import os

client = InferenceClient(
    provider="together",
    api_key=os.getenv("HUGGINGFACE_API_KEY"),
)

completion = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-R1-0528",
    messages=[{"role": "user", "content": "人生に愛は必要ですか？"}],
)

print(completion.choices[0].message)

from openai import OpenAI


client = OpenAI(
    api_key="sk-pH90E6pXcQ39nqjYVIBKAMYuHGObfM4dX1QrKuMuktC8GUco",
    base_url="https://api.n1n.ai/v1"
)

def call_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
    )
    return response.choices[0].message.content
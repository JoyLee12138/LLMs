from openai import OpenAI
client = OpenAI(
    api_key="sk",
    base_url=""
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
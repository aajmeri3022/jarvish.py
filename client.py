
from openai import OpenAI

client = OpenAI(
    api_key="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")

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general task like Alexa and Google cloud."},
        {"role": "user", "content": "What is coding?"}
    ]
)

print(response.choices[0].message.content)

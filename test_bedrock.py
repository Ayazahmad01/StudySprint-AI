
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://bedrock-mantle.eu-north-1.api.aws/v1",
)

try:
    response = client.chat.completions.create(
        model="openai.gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": "Explain machine learning in two simple sentences."
            }
        ],
        max_tokens=150,
    )

    print("SUCCESS!")
    print(response.choices[0].message.content)

except Exception as e:
    print("Error type:", type(e).__name__)
    print("Error details:", e)
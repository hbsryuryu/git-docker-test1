import openai
from .env_setting import *
import json

client = openai.AzureOpenAI(
    api_version=AZURE_OPENAI_DEPLOYMENT_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY,
)

async def generate_response(prompt: str):
    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000,
        stream=True
    )

    for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            text = chunk.choices[0].delta.content
            res_json = {
                "type": "chunk",
                "data": text,
            }
            str_json = json.dumps(res_json)
            yield f"data: {str_json}\n\n"
    
    res_json = {
        "type": "end",
        "data": "",
    }
    str_json = json.dumps(res_json)
    yield f"data: {str_json}\n\n"
import openai
import os
from fastapi import FastAPI

app = FastAPI()

def get_openai_response(prompt: str) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")  # Get API key from environment variable
    
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or "gpt-3.5-turbo" based on your access
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"]

@app.post("/generate")
async def generate_response(prompt: str):
    reply = get_openai_response(prompt)
    return {"response": reply}

import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def call_model(model_name, prompt):
    start = time.time()

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={os.getenv('GEMINI_API_KEY')}"

        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json={
                "contents": [
                    {
                        "parts": [{"text": prompt}]
                    }
                ]
            }
        )

        end = time.time()
        data = response.json()

        if response.status_code != 200:
            raise Exception(f"API Error: {data}")

        text = data["candidates"][0]["content"]["parts"][0]["text"]

        # Gemini does not return tokens → estimate
        input_tokens = len(prompt.split())
        output_tokens = len(text.split())

        return {
            "response": text,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "latency": end - start
        }

    except Exception as e:
        return {
            "response": f"ERROR: {str(e)}",
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
            "latency": 0
        }
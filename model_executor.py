import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def call_model(model_name, prompt):
    start = time.time()

    try:
        # ================= GEMINI =================
        if "gemini" in model_name:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={os.getenv('GEMINI_API_KEY')}"

            response = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{"parts": [{"text": prompt}]}]
                }
            )

            data = response.json()

            if response.status_code != 200:
                raise Exception(data)

            text = data["candidates"][0]["content"]["parts"][0]["text"]

            # Gemini → estimated tokens
            input_tokens = len(prompt.split())
            output_tokens = len(text.split())

        # ================= GROQ =================
        elif "groq" in model_name:
            url = "https://api.groq.com/openai/v1/chat/completions"

            response = requests.post(
                url,
                headers={
                    "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama3-70b-8192",
                    "messages": [{"role": "user", "content": prompt}]
                }
            )

            data = response.json()

            if response.status_code != 200:
                raise Exception(data)

            text = data["choices"][0]["message"]["content"]

            usage = data.get("usage", {})
            input_tokens = usage.get("prompt_tokens", len(prompt.split()))
            output_tokens = usage.get("completion_tokens", len(text.split()))

        else:
            raise Exception("Unknown model type")

        end = time.time()

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
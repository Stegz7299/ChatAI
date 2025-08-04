# src/model/gptj.py
import os
import json
import requests


class GPTChat:
    def __init__(self):
        self.api_url = "https://router.huggingface.co/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {os.environ.get('HF_TOKEN')}",
            "Content-Type": "application/json"
        }

    def query(self, messages: list) -> str:
        payload = {
            "model": os.environ.get("HF_MODEL"),
            "messages": messages
        }

        response = requests.post(self.api_url, headers=self.headers, json=payload)

        if response.status_code == 200:
            try:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            except (KeyError, json.JSONDecodeError) as e:
                print("Error parsing response:", e)
                return "Error: Could not parse response."
        else:
            print("Request failed:", response.status_code, response.text)
            return f"Error: {response.text}"

import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

class GPT:
    def __init__(self):
        self.url = os.environ.get('MODEL_URL')
        self.headers = {
            "Authorization": f"Bearer {os.environ.get('HUGGINGFACE_INFERENCE_TOKEN')}",
            "Content-Type": "application/json"
        }
        self.payload = {
            "inputs": "",
            "parameters": {"max_new_tokens": 50}  # Tambahkan parameter yang valid untuk text-generation
        }

    def query(self, input: str) -> str:
        self.payload["inputs"] = f"Human: {input}\nBot:"
        data = json.dumps(self.payload)

        response = requests.post(self.url, headers=self.headers, data=data)

        if response.status_code == 200:
            try:
                result = response.json()
                generated_text = result[0].get('generated_text', '').strip()
            
                # Only return the bot's response, not the whole conversation
                bot_response = generated_text.split("Bot:")[-1].strip()
                return bot_response
            except json.JSONDecodeError as e:
                print("Failed to decode JSON:", e)
                return "Error decoding JSON."
        else:
            print("Error Response:", response.text)
            return f"Error: {response.text}"


if __name__ == "__main__":
    print(GPT().query("Will artificial intelligence help humanity conquer the universe?"))

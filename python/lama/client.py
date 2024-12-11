from ollama import Client
from config import HOST, MODEL, PORT


class OllamaClient:

    def __init__(self):
        self._client = Client(host=f"{HOST}:{PORT}")

    def get_response(self, content: str) -> str:
        response = self._client.chat(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": content,
                },
            ],
        )
        return response["message"]["content"]

import asyncio
from ollama import AsyncClient, Message

from config import HOST, PORT, MODEL, VerbForm
from common import Storage


async def chat(request: Message) -> str:
  answer = ""
  async for part in await AsyncClient(f"{HOST}:{PORT}").chat(model=MODEL, messages=[request], stream=True):
    content = part["message"]["content"]
    print(content, end='', flush=True)
    answer += content
  return answer


sentence_number = "12"
request_msg = "Найди ошибки в предложении и исправь ошибки если найдешь ошибки -Oleg tells me about Petrov's being sent on a business-trip."
request: Message  = {'role': 'user', 'content': request_msg}
answer = asyncio.run(chat(request))

verb_form = VerbForm.GERUND
storage = Storage(verb_form)
storage.insert(sentence_number, request_msg, answer)
storage.save()

print()


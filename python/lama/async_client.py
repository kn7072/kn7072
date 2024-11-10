import asyncio

from common import Storage

from config import HOST, MODEL, PORT, VerbForm

from ollama import AsyncClient, Message


async def chat(request: Message) -> str:
    answer = ""
    async for part in await AsyncClient(f"{HOST}:{PORT}").chat(
        model=MODEL,
        messages=[request],
        stream=True,
    ):
        content = part["message"]["content"]
        print(content, end="", flush=True)
        answer += content
    return answer


sentence_number = "296"
request_msg = "Чем отличаются during и while, приведи примеры"
# request_msg = (
#     "Найди ошибки в предложении и исправь"
#     "ошибки если найдешь ошибки - Despite myself I couldn't help but lie to her."
# )
request: Message = {"role": "user", "content": request_msg}
answer = asyncio.run(chat(request))

verb_form = VerbForm.GERUND
storage = Storage(verb_form)
storage.insert(sentence_number, request_msg, answer)
storage.save()

print()

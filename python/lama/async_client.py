from ollama import AsyncClient

from config import HOST, MODEL

async def chat():
  message = {'role': 'user', 'content': 'переведи на русский язык - One afternoon, when I was counting on working for an hour or two more, the telephone rang.'}
  async for part in await AsyncClient(HOST).chat(model=MODEL, messages=[message], stream=True):
    # print(part['message']['content'], end='', flush=True)
    return part['message']['content']

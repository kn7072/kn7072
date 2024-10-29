# -*- coding:utf-8 -*-
import asyncio
from config import VerbForm, request_time_out
from async_client import chat
from client import OllamaClient
from common import InitRequests

init_requests = InitRequests(VerbForm.GERUND, count_request=10, time_out_between_requests=request_time_out)
lama_client = OllamaClient()
# res = asyncio.run(chat())
# res = lama_client.get_response(content="переведи на русский язык - One afternoon, when I was counting on working for an hour or two more, the telephone rang.")
# print(res)
init_requests.send_request()
print()

# -*- coding:utf-8 -*-
from config import VerbForm, request_time_out
from client import OllamaClient
from common import InitRequests

init_requests = InitRequests(VerbForm.GERUND, count_request=20, time_out_between_requests=request_time_out)
lama_client = OllamaClient()

init_requests.send_request()
print()

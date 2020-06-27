# -*- coding: utf-8 -*-
import http.client
import requests
# proxies = {"https": "10.76.182.43:8888"}
# headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'}
# url = r'http://www.google.ru/'
auth = requests.auth.HTTPProxyAuth('sg.chernov', 'QWEqwe123')
# x = requests.get(url=url, auth=auth, proxies=proxies)  # ,  headers=headers , data=data,  proxies=proxies,


headers_auh = {'Content-type': 'application/json,charset=UTF-8'}
url_auh = r'https://test-online.sbis.ru/auth/service/sbis-rpc-service300.dll'
data = '{"protocol": 3, "id": 1, "params": {"login": "\\u0432\\u0438\\u0442\\u0435\\u0441\\u04421", "password": "09876qwE"}, "jsonrpc": "2.0", "method": "\\u0421\\u0410\\u041f.\\u0410\\u0443\\u0442\\u0435\\u043d\\u0442\\u0438\\u0444\\u0438\\u0446\\u0438\\u0440\\u043e\\u0432\\u0430\\u0442\\u044c"}'
aut_res = requests.post(url=url_auh, auth=auth, data=data, headers=headers_auh)  # , proxies=proxies




# conn = http.client.HTTPSConnection("localhost", 8888)
# conn.set_tunnel("https://docs.python.org")
# res = conn.request("GET", "https://docs.python.org/3.3/library/http.client.html")
# response = conn.getresponse()
print()









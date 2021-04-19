# -*- coding=utf-8 -*-
import requests
import re
import os

all_contant = r"id=\"cleardefslist\">(?P<Cont>.+?)<div style=\"clear:both"
pattert_all_contant = re.compile(all_contant, re.DOTALL)

word_contant = r"<li>(?P<word>.+?)</li>"
pattert_word_contant = re.compile(word_contant, re.DOTALL)

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                      ' Chrome/70.0.3538.102 Safari/537.36 OPR/57.0.3098.116',
                        "Refere": "https://www.google.com/"})

url = "https://www.macmillandictionary.com/learn/clear-definitions.html"
response = session.request(method="POST", url=url)
contant = response.content

search = pattert_all_contant.search(contant.decode())

with open("Macmillan.txt", mode="w", encoding="utf-8") as f:
    if search:
        word_info = search.group("Cont")
        words = pattert_word_contant.findall(word_info)
        if words:
            for i in words:
                f.write(i + "\n")  # print(i)
    else:
        print("Релярное выражение ничего не обнаружело")



print()


# -*- coding: utf-8 -*-
from  urllib.request  import  urlopen,  Request
from  urllib.parse  import  urlencode, urlparse
from http.client import HTTPConnection, HTTPSConnection, OK
import chardet
print(chardet.detect(bytes("Cтpoкa", "cp1251")))  # "ср1251" "koi8-r"
print(chardet.detect(bytes("Cтpoкa", "utf-8")))
data = urlencode({'s':"m", 'ty':'c', 'p':'d', 't':'A'}, encoding="utf-8")
data3 = urlencode({'v':"340", 's':'ta_topgainers'}, encoding="utf-8")
print(data)
headers  =  {  "User-Agent":  "Mozilla/5.0 (Windows NT 6.1; rv:30.0) Gecko/20100101 Firefox/20.0",
               "Accept":  "image/png,image/*;q=0.8,*/*;q=0.5",
               "Accept-Language":  "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
               "Accept-Encoding":  "gzip, deflate",
               #"Referer":  "http://finviz.com/screener.ashx?v=111&f=exch_nyse,idx_sp500",
               "Connection": "keep-alive"
               }
headers2 = {"User-Agent":  "Mozilla/5.0 (Windows NT 6.1; rv:30.0) Gecko/20100101 Firefox/30.0",
           "Accept": "*/*",
           "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
           "Accept-Encoding": "gzip, deflate",
           #"Referer": "http://finviz.com/quote.ashx?t=ABT&ty=c&ta=1&p=d&b=1",
           "Connection": "keep-alive"
          }
headers3 = {'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:20.0) Gecko/20100101 Firefox/20.0', 'Cookie': '__utma=189210428.833898174.1403449111.1403449111.1403449111.1; __utmz=189210428.1403449111.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __qca=P0-1863874454-1403449111286; __csmv=a5677a7fa5145513; __csv=ce189cdcc3f16018|0; __csnv=89543c38fc1ebe0d; screenerUrl=screener.ashx?v=340&s=ta_topgainers', 'Accept-Encoding': 'gzip, deflate', 'Host': 'www.finviz.com', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5'}
con = HTTPConnection("www.finviz.com")  # http://finviz.com www.
#con.request("GET", "/chart.ashx?%s" % data,  headers=headers)
con.request("GET", "/screener.ashx?%s" % data3,  headers=headers3)
result = con.getresponse()
print(result.msg.get_content_charset())
ggg = result.read()
print(result.read().decode("utf-8"))
con.close()

headers2 = {"User-Agent":  "Mozilla/5.0 (Windows NT 6.1; rv:30.0) Gecko/20100101 Firefox/30.0",
           "Accept": "*/*",
           "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
           "Accept-Encoding": "gzip, deflate",
           #"Referer": "http://finviz.com/quote.ashx?t=ABT&ty=c&ta=1&p=d&b=1",
           "Connection": "keep-alive"
          }
data2 = urlencode({'rev':"4"}, encoding="utf-8")
con2 = HTTPConnection("finviz.com")
con2.request("GET", "/script/quote.js?%s" % data2,  headers=headers2)

result = con2.getresponse()
cod = result.msg.get_content_charset()
print(result.status)
print(result.getheader("Content-Type"))
# javascript:alert("Cookies: "+document.cookie)
print(result.read().decode("utf-8"))
dict_heders = dict(result.getheaders())
# версия протокола
print(result.version)
# писок ключей в заголовках ответа сервера
result.msg.keys()
result.msg.get_content_charset()  # позволяет  получить кодировку  из  заголовка Content-Type
#con.close()
print()
"""headers  =  {  "User-Agent":  "MySpider/1.0",
"Accept":  "text/htm1,  text/p1ain,  app1ication/xm1",
"Accept-Language":  "ru,  ru-RU",
"Accept-Charset":  "windows-1251",
"Referer":  "/index.php"  }
data  =  urlencode({  "co1or":  "Красный",  "var":  15},  encoding="cp1251")
#  Отправка даннь~ методом POST
ur1  =  "http://test1.ru/testrobots.php"
request  =  Request(ur1,  data.encode("cp1251"),  headers=headers)
res  =  urlopen(request)
print(res.read() .decode("cpl251"))
res. close ()
"""
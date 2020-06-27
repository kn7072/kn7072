# -*- coding:utf-8 -*-
import requests
import lxml.html as html
import sys

url = r'http://www.barchart.com/commodityfutures/Natural_Gas_Futures/options/NG?mode=d&view='
auth = requests.auth.HTTPProxyAuth('sg.chernov', 'QWEqwe123')
headers0 = {'Content-Type': 'application/json; charset=UTF-8'}
r = requests.get(url, headers=headers0, verify=False, auth=auth)
text = r.text  # код страницы
table = html.fromstring(text)  # объект html
obj = table.find_class('datatable_simple')
# убираем 1 и последний элеменыт - пусты
list_price_puts = obj[0].find_class('qb_shad')[15].text_content().split('\r\n\t\t')[1:-1]
put_quote = []
for i in obj[0].find_class('qb_shad'):
    quote_list = i.text_content().split('\r\n\t\t')[1:-1]
    # Strike 	Open 	High 	Low 	Close 	Change 	Volume 	Open Int 	Delta 	Prem ($)
    # начинае разгребать
    try:
        strike = float(quote_list[0].replace('P', ''))
        # на месте open может находиться '\xa0'
        open_price = float(quote_list[1].replace('\xa0', '0'))
        high = float(quote_list[2])
        low = float(quote_list[3])
        close = float(quote_list[4].replace('s', ''))
        change = float(quote_list[5].replace('unch', '0'))
        volume = float(quote_list[6].replace(',', ''))

        open_int = float(quote_list[7].replace('\t', '').replace(',', ''))
    except :
        sys.exc_info()
        print()
    delta = float(quote_list[8])
    prem = float(quote_list[9].replace(',', ''))
    if open_price == 0:
        open_price = close
    put_quote.append([strike, open_price, high, low, close, change, open_int, delta, prem])
dict_data_puts = dict()
list_price_calls = obj[0].find_class('qb_line')
text_element = obj.text_content()
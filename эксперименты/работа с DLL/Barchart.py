# -*- coding:utf-8 -*-
import requests
import lxml.html as html
from lxml.cssselect import CSSSelector
import sys

sel = CSSSelector('div#divContent tbody')

url = r'http://www.barchart.com/commodityfutures/Natural_Gas_Futures/options/NGM15?mode=d&view='
auth = requests.auth.HTTPProxyAuth('sg.chernov', 'QWEqwe123')
headers0 = {'Content-Type': 'application/json; charset=UTF-8'}
r = requests.get(url, headers=headers0, verify=False)  # , auth=auth
text = r.text  # код страницы
table = html.fromstring(text)  # объект html
elm = table.xpath("(//div[@id='divContent']//table//table)[1]")[0].cssselect("tr")#//tbody
current_price = float(elm[2].text_content().split(":")[1])
set(table)

obj = table.find_class('datatable_simple')
# убираем 1 и последний элеменыт - пусты
list_price_puts = obj[0].find_class('qb_shad')[15].text_content().split('\r\n\t\t')[1:-1]
price_1 = obj[0].find_class('qb_shad')
price_2 = obj[0].find_class('qb_line')
all_price = price_1 + price_2
put_quote = []
call_quote = []

def ratio_spread(list_quote, min_step=4, max_step=7, ratio=2):
    # Type   Strike 	Open 	High 	Low 	Close 	Change 	Volume 	Open Int 	Delta 	Prem ($)
    count = len(list_quote)
    for i in range(count):
        min_spread = i + min_step
        if min_spread < count - 1:
            max_spread = i + max_step
            if max_spread < count:
                pass
            else:
                max_spread = count
            for j in range(min_spread, max_spread):
                price = list_quote[j][9]*ratio - list_quote[i][9]
                if price > 0:
                    try:
                        print(str(list_quote[i][1])+"   "+str(list_quote[j][1])+" = "+str(price))
                    except:
                        x = sys.exc_info()
                        print(x)


    pass
for i in all_price:
    quote_list = i.text_content().split('\r\n\t\t')[1:-1]
    # Type   Strike 	Open 	High 	Low 	Close 	Change 	Volume 	Open Int 	Delta 	Prem ($)
    # начинае разгребать
    try:
        type_option = ''
        if 'P' in quote_list[0]:
            type_option = 'P'
            strike = float(quote_list[0].replace('P', ''))
        elif 'C' in quote_list[0]:
            type_option = 'C'
            strike = float(quote_list[0].replace('C', ''))
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
    if type_option == 'P':
        put_quote.append([type_option, strike, open_price, high, low, close, change, open_int, delta, prem])
    if type_option == 'C':
        call_quote.append([type_option, strike, open_price, high, low, close, change, open_int, delta, prem])

def sortByLength(inputStr):
        return inputStr[1]
sort_call = sorted(call_quote, key=sortByLength)

ratio_spread(sort_call)

dict_data_puts = dict()

list_price_calls = obj[0].find_class('qb_line')
text_element = obj.text_content()
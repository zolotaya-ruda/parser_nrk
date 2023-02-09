import datetime
import json
import time
from html.parser import HTMLParser
import requests
from sql_module.models import Day, Week, Month, session
import pandas as pd

import config

MAIN_URL = 'https://plati.market'

cooks = {}

with open('cookies.json', 'r') as f:
    for cook in json.loads(f.read()):
        cooks[cook['name']] = cook['value']

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Host': 'plati.market',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36', }


class Parser(HTMLParser):
    def __init__(self, is_parse_product_page):
        self.is_parse_product_page = is_parse_product_page

        self.title = None
        self.sales_count = None

        self.is_found_title = False
        self.is_found_sales_count = False

        super(Parser, self).__init__()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if not self.is_parse_product_page:
            if tag == 'a':
                if 'href' in attrs:
                    if attrs['href'].startswith('/itm/last-sale'):
                        product_parser = Parser(True)

                        d = requests.get(MAIN_URL + attrs['href'], headers=headers, cookies=cooks)
                        product_parser.feed(requests.get(MAIN_URL + attrs['href'], headers=headers).text)

                        price = int(requests.get(
                            f'https://plati.market/asp/price_options.asp?p={attrs["href"].split("/")[-1]}&n=0&c=RUB&e=&d=true&x=<response></response>&rnd=0.5937313590599644').json()[
                                        'amount'])

                        if Day.is_exists(product_parser.title):
                            try:

                                Day.get_by_title(product_parser.title).change(price, int(product_parser.sales_count))
                                Week.get_by_title(product_parser.title).change(price, int(product_parser.sales_count))
                                Month.get_by_title(product_parser.title).change(price, int(product_parser.sales_count))

                            except:
                                print('passed')

                        else:
                            Day(title=product_parser.title, price=price, sales_count=0,
                                last_sales_count=int(product_parser.sales_count)).create()

                            Week(title=product_parser.title, price=price, sales_count=0,
                                 last_sales_count=int(product_parser.sales_count)).create()

                            Month(title=product_parser.title, price=price, sales_count=0,
                                  last_sales_count=int(product_parser.sales_count)).create()

        if self.is_parse_product_page:
            if tag == 'h1':
                if 'itemprop' in attrs:
                    if attrs['itemprop'] == 'name':
                        self.is_found_title = True

            elif tag == 'div':
                if 'class' in attrs:
                    if attrs['class'] == 'goods-sell-count':
                        self.is_found_sales_count = True

    def handle_data(self, _data):
        if self.is_found_title:
            self.title = _data
            self.is_found_title = False

        if 'Продаж' in _data.strip():
            self.sales_count = _data.strip().split(':')[-1]


start_time = datetime.datetime.now()


def make_excel():
    excel_data = {'Название': ['за час'],
                  'Цена': [''],
                  'Количество продаж': ['']
                  }

    for product in Day.get_by_date():
        excel_data['Название'].append(product[0])
        excel_data['Цена'].append(product[1])
        excel_data['Количество продаж'].append(product[2])

    excel_data['Название'].append('за 2 часа')
    excel_data['Цена'].append('')
    excel_data['Количество продаж'].append('')

    for product in Week.get_by_date():
        excel_data['Название'].append(product[0])
        excel_data['Цена'].append(product[1])
        excel_data['Количество продаж'].append(product[2])
    excel_data['Название'].append('за 3 часа')
    excel_data['Цена'].append('')
    excel_data['Количество продаж'].append('')

    for product in Month.get_by_date():
        excel_data['Название'].append(product[0])
        excel_data['Цена'].append(product[1])
        excel_data['Количество продаж'].append(product[2])

    df = pd.DataFrame(excel_data)
    df.to_excel('table.xlsx')

    with open("table.xlsx", "rb") as filexlsx:
        files = {"document": filexlsx}
        chat_id = "1460245641"
        r = requests.post('https://api.telegram.org/bot5473936156:AAElTjeR8ydJrPK57_eOF1dDEs1I9aqiBbg/sendDocument',
                          data={"chat_id": chat_id}, files=files)


while True:
    print('[START]')
    for ref in config.hrefs:
        data = requests.get(ref, headers=headers, allow_redirects=True)
        print(f'[SUCCESS PARSED] {ref}')
        parser = Parser(False)
        parser.feed(data.text)
    print('[END]')

    if datetime.datetime.now() - start_time >= datetime.timedelta(hours=3):
        make_excel()
        session.query(Month).delete()
        session.commit()

    elif datetime.datetime.now() - start_time >= datetime.timedelta(hours=2):
        make_excel()
        session.query(Month).delete()
        session.commit()

    elif datetime.datetime.now() - start_time >= datetime.timedelta(hours=1):
        make_excel()
        session.query(Month).delete()
        session.commit()

    time.sleep(60)

import datetime
import json
import time
from html.parser import HTMLParser
import requests
from sql_module.models import Day, Week, Month, session
import pandas as pd
import xmltodict
import config
from fake_useragent import UserAgent

ua = UserAgent()

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
    def __init__(self, is_parse_product_page, session=None):
        self.is_parse_product_page = is_parse_product_page
        self.session = session

        self.title = None
        self.sales_count = None

        self.is_found_title = False
        self.is_found_sales_count = False
        self.flag = False
        self.is_find_ref = False

        super(Parser, self).__init__()

    def handle_starttag(self, tag, attrs) -> None:
        attrs = dict(attrs)
        if tag == 'a':
            if 'href' in attrs:
                if attrs['href'].startswith('/itm/last-sale'):
                    self.flag = True
                    product_id = attrs['href'].split('/')[-1]

                    r = requests.post('https://plati.io/xml/goods_info.asp',
                                      data=f'''
                    <?xml version='1.0' encoding='utf-8'?>
                    <digiseller.request>
                      <id_good>{product_id}</id_good>
                      <guid_agent>10C2691408D14B458E348F2A52F2BF45</guid_agent>
                      <lang>ru-RU</lang>

                    </digiseller.request>     
                    ''', headers={'Content-Type': 'application/xml'}).text

                    xml_data = xmltodict.parse(r)

                    sales_count = int(xml_data['digiseller.response']['statistics']['cnt_sell'])
                    title = xml_data['digiseller.response']['name_goods']

                    price_data = requests.get(
                        f'https://api.digiseller.ru/api/products/{product_id}/data',
                        headers={'Accept': 'application/json'}).json()

                    try:
                        price = int(price_data['product']['prices']['initial']['RUB'])
                    except:
                        return

                    time_now = datetime.datetime.now()

                    if Day.is_exists(title):
                        table = Day.get_by_title(title)

                        if table.last_sales_count != sales_count:
                            try:

                                Day.get_by_title(title).change(price, int(sales_count), time_now)
                            except Exception as e:
                                print(e)

                    else:
                        Day(title=title, price=price, sales_count=0,
                            last_sales_count=int(sales_count), time=datetime.datetime.now()).create()


start_time = datetime.datetime.now()

start_time_day = start_time


def make_excel():
    print('send')
    excel_data = {'Название': ['за 10'],
                  'Цена': [''],
                  'Количество продаж': ['']
                  }

    for product in Day.get_by_day():
        excel_data['Название'].append(product[0])
        excel_data['Цена'].append(product[1])
        excel_data['Количество продаж'].append(product[2])

    excel_data['Название'].append('')
    excel_data['Цена'].append('')
    excel_data['Количество продаж'].append('')

    excel_data['Название'].append('за 20')
    excel_data['Цена'].append('')
    excel_data['Количество продаж'].append('')

    for product in Day.get_by_week():
        excel_data['Название'].append(product[0])
        excel_data['Цена'].append(product[1])
        excel_data['Количество продаж'].append(product[2])

    excel_data['Название'].append('')
    excel_data['Цена'].append('')
    excel_data['Количество продаж'].append('')

    excel_data['Название'].append('за 30')
    excel_data['Цена'].append('')
    excel_data['Количество продаж'].append('')

    for product in Day.get_by_month():
        excel_data['Название'].append(product[0])
        excel_data['Цена'].append(product[1])
        excel_data['Количество продаж'].append(product[2])

    df = pd.DataFrame(excel_data)
    df.to_excel('table.xlsx')

    with open("table.xlsx", "rb") as filexlsx:
        files = {"document": filexlsx}
        chat_id = "1460245641"
        requests.post('https://api.telegram.org/bot5473936156:AAElTjeR8ydJrPK57_eOF1dDEs1I9aqiBbg/sendDocument',
                      data={"chat_id": -1001880738236}, files=files)


while True:
    print('[START]')

    for ref in config.hrefs:
        headers['User-Agent'] = ua.random

        _session = requests.session()
        _session.headers = headers
        _session.get('https://plati.market')
        data = _session.get(ref, cookies=cooks)
        parser = Parser(False, _session)
        parser.feed(data.text)
        if not parser.flag:
            requests.post('https://api.telegram.org/bot5473936156:AAElTjeR8ydJrPK57_eOF1dDEs1I9aqiBbg/sendMessage',
                          data={"chat_id": -1001880738236, 'text': 'error: nothing parsed'})

    print('[END]')

    if datetime.datetime.now() - start_time_day >= datetime.timedelta(hours=1):
        make_excel()
        start_time_day = datetime.datetime.now()

    time.sleep(300)

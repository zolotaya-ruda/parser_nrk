import requests
from html.parser import HTMLParser
import json

class Parser(HTMLParser):
    def handle_starttag(self, tag, attrs) -> None:
        attrs = dict(attrs)
        if tag == 'a':
            if 'href' in attrs:
                if attrs['href'].startswith('/itm/last-sale'):
                    print(attrs)


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

session = requests.session()
session.headers = headers
session.get('https://plati.market')

data = session.get('https://plati.market/seller/mmopix/987024/', cookies=cooks)

with open('test.html', 'wb') as f:
    f.write(data.content)

Parser().feed(data.text)

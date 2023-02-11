import requests

_pass = '30FFB8F0F9'
r = requests.post('https://plati.io/xml/goods_info.asp',
                  data='''
<?xml version='1.0' encoding='utf-8'?>
<digiseller.request>
  <id_good>3587291</id_good>
  <guid_agent>10C2691408D14B458E348F2A52F2BF45</guid_agent>
  <lang>ru-RU</lang>

</digiseller.request>     
''', headers={'Content-Type': 'application/xml'}).text

print(r)

r1 = requests.get(f'https://plati.market/asp/price_options.asp?p=3409971&n=0&c=RUB&e=&d=true&x=<response></response>&rnd=0.5937313590599644')

import xmltodict, json
o = xmltodict.parse(r)
res = json.dumps(o)
print(res)


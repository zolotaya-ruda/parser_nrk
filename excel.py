import pandas as pd

data = {
    '✅FINAL FANTASY XIV Online Starter🎁Steam Gift RU🚛 Авто': {'price': 1143, 'sales_count': 0, 'last_sales_count': 77},
    'Wolfpack - STEAM GIFT РОССИЯ': {'price': 854, 'sales_count': 0, 'last_sales_count': 6},
    'РФ/СНГ/Турция ☑️⭐Hogwarts Legacy DELUXE EDITION Steam': {'price': 4599, 'sales_count': 4,
                                                              'last_sales_count': 2225},
    '🎁+PS PLUS ESSENTIAL EXTRA DELUXE 1-12 МЕСЯЦЕВ 🚀БЫСТРО': {'price': 104, 'sales_count': 3,
                                                              'last_sales_count': 28538},
    'Epic Games ☑️⭐Смена региона на КАЗАХСТАН': {'price': 199, 'sales_count': 0, 'last_sales_count': 11},
    '✅Xbox Game Pass ULTIMATE 2 МЕСЯЦА+EA PLAY': {'price': 99, 'sales_count': 0, 'last_sales_count': 11013},
    '❤️✅XBOX GAME PASS ULTIMATE 12 МЕСЯЦЕВ 🚀 ЛЮБОЙ АККАУНТ': {'price': 1999, 'sales_count': 1,
                                                              'last_sales_count': 92134}}


def make_excel():
    excel_data = {'Название': [],
                  'Цена': [],
                  'Количество продаж': []
                  }

    for product in data:
        excel_data['Название'].append(product)
        excel_data['Цена'].append(data[product]['price'])
        excel_data['Количество продаж'].append(data[product]['sales_count'])

    df = pd.DataFrame(excel_data)
    print(df)
    df.to_excel('table1.xlsx')

import requests

with open("table1.xlsx", "rb") as filexlsx:
    files = {"document":filexlsx}
    title = "table1.xlsx"
    chat_id = "1460245641"
    r = requests.post('https://api.telegram.org/bot5473936156:AAElTjeR8ydJrPK57_eOF1dDEs1I9aqiBbg/sendDocument', data={"chat_id": chat_id}, files=files)
    print(r.text)
from sql_module.models import Day, Week, Month, session
import pandas as pd
import xmltodict
import requests
import datetime


def make_excel():
    excel_data = {'Название': ['за 10'],
                  'Цена': [''],
                  'Количество продаж': ['']
                  }

    for product in Day.get_by_date():
        excel_data['Название'].append(product[0])
        excel_data['Цена'].append(product[1])
        excel_data['Количество продаж'].append(product[2])

    excel_data['Название'].append('за 20')
    excel_data['Цена'].append('')
    excel_data['Количество продаж'].append('')

    for product in Week.get_by_date():
        excel_data['Название'].append(product[0])
        excel_data['Цена'].append(product[1])
        excel_data['Количество продаж'].append(product[2])

    excel_data['Название'].append('за 30')
    excel_data['Цена'].append('')
    excel_data['Количество продаж'].append('')

    for product in Month.get_by_date():
        excel_data['Название'].append(product[0])
        excel_data['Цена'].append(product[1])
        excel_data['Количество продаж'].append(product[2])

    print(excel_data)

    df = pd.DataFrame(excel_data)
    df.to_excel('table.xlsx')

    with open("table.xlsx", "rb") as filexlsx:
        files = {"document": filexlsx}
        chat_id = "1460245641"
        requests.post('https://api.telegram.org/bot5473936156:AAElTjeR8ydJrPK57_eOF1dDEs1I9aqiBbg/sendDocument',
                      data={"chat_id": chat_id}, files=files)


s = [[product.title, product.price, product.sales_count] for product in session.query(Week).all() if
     datetime.datetime.now() - product.time > datetime.timedelta(
         minutes=20)]
print(Day.get_by_date())

make_excel()

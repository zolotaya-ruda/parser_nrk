import datetime

from sql_module.models import Day, Sale

# day = Day(title='CSGO AVTOBUY', last_sales_count=231, price=600).create()
# print(day)

print(Sale.get_by_day(), Sale.get_by_week(), Sale.get_by_month())

# sale = Sale(title='CSGO AVTOBUY', product_id=1).create()
#Sale(title='CSGO AVTOBUY1', last_sales_count=231, price=600).create()

print(Sale.get_by_month().items())

res = dict(sorted(Sale.get_by_day().items(), key=lambda item: len(item[1]), reverse=True))
print(res)

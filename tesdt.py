import datetime
from sql_module.models import Day

d = datetime.datetime.now() - datetime.datetime(2023, 2, 9, 22, 0)
print(d >= datetime.timedelta(minutes=20))

print(Day.get_by_date())

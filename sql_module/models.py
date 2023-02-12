import datetime

from .connector import base, session, engine
from sqlalchemy.types import Integer, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Column


class Day(base):
    __tablename__ = 'day'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    price = Column(Integer, nullable=False)
    last_sales_count = Column(Integer, nullable=False)
    time = Column(DateTime, default=datetime.datetime.now())

    def create(self):
        session.add(self)
        session.commit()
        return self

    @staticmethod
    def get_by_title(title):
        return session.query(Day).filter(Day.title == title).one()

    def change(self, price, sales_count, time):
        self.sales_count += sales_count - self.last_sales_count
        self.last_sales_count = sales_count
        self.price = price
        self.time = time
        session.commit()

    @staticmethod
    def is_exists(title):
        return True if len(session.query(Day).filter(Day.title == title).all()) != 0 else False

    @staticmethod
    def get_by_day():
        data = session.query(Day)

    @staticmethod
    def get_by_week():
        data = [[product.title, product.price, product.sales_count] for product in
                session.query(Day).order_by(Day.sales_count.desc()).all() \
                if datetime.datetime.now() - product.time <= datetime.timedelta(hours=2)]
        if len(data) < 21:
            return data

        return data[:20]

    @staticmethod
    def get_by_month():
        data = [[product.title, product.price, product.sales_count] for product in
                session.query(Day).order_by(Day.sales_count.desc()).all() \
                if datetime.datetime.now() - product.time <= datetime.timedelta(hours=3)]
        if len(data) < 21:
            return data

        return data[:20]

    @staticmethod
    def all():
        return [[product.title, product.price, product.sales_count] for product in session.query(Day).all()]


class Sale(base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    price = Column(Integer, nullable=False)
    time = Column(DateTime, default=datetime.datetime.now())
    last_sales_count = Column(Integer, nullable=False)

    def create(self):
        session.add(self)
        session.commit()
        return self

    def change(self, sales_count, title, price):
        difference = sales_count - self.last_sales_count
        for _ in range(difference):
            Sale(title=title, price=price, last_sales_count=sales_count, time=datetime.datetime.now()).create()

    @staticmethod
    def get_by_day():
        data = {}
        for sale in session.query(Sale).all():
            if datetime.datetime.now() - sale.time < datetime.timedelta(minutes=5):
                if sale.title not in data:
                    data[sale.title] = [sale]
                else:
                    data[sale.title].append(sale)

        return data

    @staticmethod
    def get_by_week():
        data = {}
        for sale in session.query(Sale).all():
            if datetime.datetime.now() - sale.time < datetime.timedelta(minutes=10):
                if sale.title not in data:
                    data[sale.title] = [sale]
                else:
                    data[sale.title].append(sale)

        return data

    @staticmethod
    def get_by_month():
        data = {}
        for sale in session.query(Sale).all():
            if datetime.datetime.now() - sale.time < datetime.timedelta(minutes=15):
                if sale.title not in data:
                    data[sale.title] = [sale]
                else:
                    data[sale.title].append(sale)

        return data

    @staticmethod
    def get_last(title):
        return session.query(Sale).filter(Sale.title == title).all()[-1]

    @staticmethod
    def is_exists(title):
        return True if len(session.query(Sale).filter(Sale.title == title).all()) > 0 else False

# base.metadata.create_all(engine)

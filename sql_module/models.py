import datetime

from .connector import base, session, engine
from sqlalchemy.types import Integer, String, DateTime
from sqlalchemy import Column


class Day(base):
    __tablename__ = 'day'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    price = Column(Integer, nullable=False)
    sales_count = Column(Integer, nullable=False)
    last_sales_count = Column(Integer, nullable=False)
    time = Column(DateTime, default=datetime.datetime.now())

    def create(self):
        session.add(self)
        session.commit()
        return self

    @staticmethod
    def get_by_title(title):
        return session.query(Day).filter(Day.title == title).one()

    def change(self, price, sales_count):
        self.sales_count += sales_count - self.last_sales_count
        self.last_sales_count = sales_count
        self.price = price
        self.create()

    @staticmethod
    def is_exists(title):
        return True if len(session.query(Day).filter(Day.title == title).all()) != 0 else False

    @staticmethod
    def get_by_date():
        return [[product.title, product.price, product.sales_count] for product in session.query(Day).filter((datetime.datetime.now() - Day.time) > datetime.timedelta(hours=1)).all()]


class Week(base):
    __tablename__ = 'week'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    price = Column(Integer, nullable=False)
    sales_count = Column(Integer, nullable=False)
    last_sales_count = Column(Integer, nullable=False)
    time = Column(DateTime, default=datetime.datetime.now())

    def create(self):
        session.add(self)
        session.commit()
        return self

    @staticmethod
    def get_by_title(title):
        return session.query(Week).filter(Week.title == title).one()

    def change(self, price, sales_count):
        self.sales_count += sales_count - self.last_sales_count
        self.last_sales_count = sales_count
        self.price = price
        self.create()

    @staticmethod
    def get_by_date():
        return [[product.title, product.price, product.sales_count] for product in session.query(Week).filter((datetime.datetime.now() - Day.time) > datetime.timedelta(hours=2)).all()]

class Month(base):
    __tablename__ = 'month'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    price = Column(Integer, nullable=False)
    sales_count = Column(Integer, nullable=False)
    last_sales_count = Column(Integer, nullable=False)
    time = Column(DateTime, default=datetime.datetime.now())

    def create(self):
        session.add(self)
        session.commit()
        return self

    @staticmethod
    def get_by_title(title):
        return session.query(Month).filter(Month.title == title).one()

    def change(self, price, sales_count):
        self.sales_count += sales_count - self.last_sales_count
        self.last_sales_count = sales_count
        self.price = price
        self.create()

    @staticmethod
    def get_by_date():
        return [[product.title, product.price, product.sales_count] for product in session.query(Month).filter((datetime.datetime.now() - Day.time) > datetime.timedelta(hours=1)).all()]

# base.metadata.create_all(engine)

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

    def change(self, price, sales_count, time):
        self.sales_count += sales_count - self.last_sales_count
        self.last_sales_count = sales_count
        self.price = price
        self.create()
        self.time = time
        session.commit()

    @staticmethod
    def is_exists(title):
        return True if len(session.query(Day).filter(Day.title == title).all()) != 0 else False

    @staticmethod
    def get_by_day():
        data = [[product.title, product.price, product.sales_count] for product in
                session.query(Day).order_by(Day.sales_count.desc()).all() \
                if datetime.datetime.now() - product.time <= datetime.timedelta(hours=1)]
        if len(data) < 21:
            return data

        return data[:20]

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

    @staticmethod
    def is_exists(title):
        return True if len(session.query(Week).filter(Week.title == title).all()) != 0 else False

    def change(self, price, sales_count, time):
        self.sales_count += sales_count - self.last_sales_count
        self.last_sales_count = sales_count
        self.price = price
        self.time = time
        session.commit()

    @staticmethod
    def get_by_date():
        data = [[product.title, product.price, product.sales_count] for product in session.query(Week).all() \
                if datetime.datetime.now() - product.time <= datetime.timedelta(minutes=10)]
        if len(data) < 21:
            return data

        return data[:20]

    @staticmethod
    def all():
        return [[product.title, product.price, product.sales_count] for product in session.query(Week).all()]


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

    def change(self, price, sales_count, time):
        self.sales_count += sales_count - self.last_sales_count
        self.last_sales_count = sales_count
        self.price = price
        self.create()
        self.time = time
        session.commit()

    @staticmethod
    def is_exists(title):
        return True if len(session.query(Month).filter(Month.title == title).all()) != 0 else False

    @staticmethod
    def get_by_date():
        data = [[product.title, product.price, product.sales_count] for product in session.query(Month).all() \
                if datetime.datetime.now() - product.time <= datetime.timedelta(minutes=15)]

        if len(data) < 21:
            return data

        return data[:20]

    @staticmethod
    def all():
        return [[product.title, product.price, product.sales_count] for product in session.query(Month).all()]

# base.metadata.create_all(engine)

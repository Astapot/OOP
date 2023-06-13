import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Book, Shop, Sale, Stock

DSN = 'postgresql://postgres:99113322vfrcbv@localhost:5432/ORM'
engine = sqlalchemy.create_engine(DSN)

# Задание 2. Функция для поиска продаж по автору. Лень было дальше вникать как делать выборку по разным данным, поэтому
# просто сделал через трай ексепт, но этого если что и в обучении не было..


def find_sales(session):
    aim = input('Введите идентификатор или имя: ')
    try:
        int(aim)
        sales = session.query(Sale, Stock, Shop, Book, Publisher). \
            select_from(Sale).outerjoin(Stock).outerjoin(Shop).outerjoin(Book, Stock.id_book == Book.id).outerjoin(
            Publisher).filter(Publisher.id == aim).all()
        for sale, stock, shop, book, publisher in sales:
            print(f'{book.title} | {shop.name} | {sale.price} | {sale.date_sale}')
    except ValueError:
        sales = session.query(Sale, Stock, Shop, Book, Publisher). \
            select_from(Sale).outerjoin(Stock).outerjoin(Shop).outerjoin(Book, Stock.id_book == Book.id).outerjoin(
            Publisher).filter(Publisher.name == aim).all()
        for sale, stock, shop, book, publisher in sales:
            print(f'{book.title} | {shop.name} | {sale.price} | {sale.date_sale}')
    return '.'


create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

p1 = Publisher(name='Terry Goodkind')
p2 = Publisher(name='Steven King')

session.add_all([p1, p2])
session.commit()

b1 = Book(title='First rule of witcher', id_publisher='1')
b2 = Book(title='Second rule of witcher', id_publisher='1')
b3 = Book(title='IT', id_publisher='2')

session.add_all([b1, b2, b3])
session.commit()

shop1 = Shop(name='Книжный')
shop2 = Shop(name='Суперкнижный')

session.add_all([shop1, shop2])
session.commit()

stock1 = Stock(id_book=1, id_shop=1, count=30)
stock2 = Stock(id_book=2, id_shop=1, count=10)
stock3 = Stock(id_book=3, id_shop=2, count=1)

session.add_all([stock1, stock2, stock3])
session.commit()

s1 = Sale(price=100, date_sale='2023-01-01 20:20:20', id_stock='1', count=10)
s2 = Sale(price=80, date_sale='2023-01-01 20:20:21', id_stock='2', count=5)
s3 = Sale(price=50, date_sale='2023-01-01 20:20:22', id_stock='1', count=6)
s4 = Sale(price=1000, date_sale='2001-01-01 00:01:02', id_stock='3', count=10)

session.add_all([s1, s2, s3, s4])
session.commit()

find_sales(session)

session.close()

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Consignor(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Уникальный идентификатор комитента
    first_name = db.Column(db.varchar(50), nullable=False) # Имя комитента
    last_name = db.Column(db.varchar(50), nullable=False) # Фамилия комитента
    middle_name = db.Column(db.varchar(50), nullable=True) # Отчество комитента
    email = db.Column(db.varchar(100), nullable=False) # Email комитента
    phone_number = db.Column(db.varchar(20), nullable=False)  # Номер телефона комитента
    passport_data = db.Column(db.varchar(50), nullable=False) # Паспортные данные комитента
    INN = db.Column(db.varchar(50), nullable=False) # ИНН комитента
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id')) # Идентификатор продажи
    report_id = db.Column(db.Integer, db.ForeignKey('report.id')) # Идентификатор отчёта


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Уникальный идентификатор товара
    product_name = db.Column(db.varchar(100), nullable=False) # Наименование товара
    description = db.Column(db.varchar(500), nullable=False) # Описание товара
    delivery_date = db.Column(db.date, nullable=False) # Дата доставки товара
    expiry_date = db.Column(db.date, nullable=False) # Срок реализации товара
    price = db.Column(db.float, nullable=False) # Цена товара
    status = db.Column(db.varchar(50), nullable=False) # Статус товара
    consignor_id = db.Column(db.Integer, db.ForeignKey('consignor.id')) # Идентификатор комитента
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id')) # Идентификатор продажи
    report_id = db.Column(db.Integer, db.ForeignKey('report.id')) # Идентификатор отчёта


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Уникальный идентификатор продажи
    sale_date = db.Column(db.date, nullable=False) # Дата продажи
    sale_price = db.Column(db.float, nullable=False) # Цена продажи
    commission = db.Column(db.float, nullable=False) # Комиссия
    status = db.Column(db.varchar(50), nullable=False) # Статус
    consignor_id = db.Column(db.Integer, db.ForeignKey('consignor.id')) # Идентификатор комитента


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор отчета
    number = db.Column(db.varchar(50), nullable=False)  # Номер отчета
    date = db.Column(db.Date, nullable=False)  # Дата отчета
    report_type = db.Column(db.varchar(50), nullable=False)  # Тип отчета
    description = db.Column(db.varchar(200), nullable=False)  # Описание отчета

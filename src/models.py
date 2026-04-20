from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Consignor(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Уникальный идентификатор комитента
    last_name = db.Column(db.String(50), nullable=False)  # Фамилия комитента
    first_name = db.Column(db.String(50), nullable=False) # Имя комитента
    middle_name = db.Column(db.String(50), nullable=True) # Отчество комитента
    email = db.Column(db.String(100), nullable=False) # Email комитента
    phone_number = db.Column(db.String(20), nullable=False)  # Номер телефона комитента
    passport_data = db.Column(db.String(50), nullable=False) # Паспортные данные комитента
    INN = db.Column(db.String(50), nullable=False) # ИНН комитента


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор отчета
    number = db.Column(db.String(50), nullable=False)  # Номер отчета
    date = db.Column(db.Date, nullable=False)  # Дата отчета
    report_type = db.Column(db.String(50), nullable=False)  # Тип отчета
    description = db.Column(db.String(200), nullable=False)  # Описание отчета
    consignor_id = db.Column(db.Integer, db.ForeignKey('consignor.id'), nullable=False) # Идентификатор комитента


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Уникальный идентификатор продажи
    sale_date = db.Column(db.Date, nullable=False) # Дата продажи
    sale_price = db.Column(db.Float, nullable=False) # Цена продажи
    commission = db.Column(db.Float, nullable=False) # Комиссия
    status = db.Column(db.String(50), nullable=False) # Статус


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Уникальный идентификатор товара
    product_name = db.Column(db.String(100), nullable=False) # Наименование товара
    description = db.Column(db.String(500), nullable=False) # Описание товара
    delivery_date = db.Column(db.Date, nullable=False) # Дата доставки товара
    expiry_date = db.Column(db.Date, nullable=False) # Срок реализации товара
    price = db.Column(db.Float, nullable=False) # Цена товара
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False) # Идентификатор отчёта
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'), nullable=True)  # Идентификатор продажи

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, redirect, url_for, request, flash
from models import db, Consignor, Report, Sale, Product
from config import Config

from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


# Для тестирования
def insert_test_data():
    consignors = [
        {'id': 1, 'last_name': 'Соколов', 'first_name': 'Иван', 'middle_name': 'Алексеевич',
         'email': 'ivan.sokolov@example.com',
         'phone_number': '79001234567', 'passport_data': '4510 123456', 'INN': '123456789012'},
        {'id': 2, 'last_name': 'Морозова', 'first_name': 'Екатерина', 'middle_name': 'Дмитриевна',
         'email': 'ekaterina.morozova@example.com',
         'phone_number': '79111234568', 'passport_data': '4511 234567', 'INN': '234567890123'},
        {'id': 3, 'last_name': 'Волков', 'first_name': 'Дмитрий', 'middle_name': '',
         'email': 'dmitry.volkov@example.com',
         'phone_number': '79221234569', 'passport_data': '4512 345678', 'INN': '345678901234'},
        {'id': 4, 'last_name': 'Зайцева', 'first_name': 'Анна', 'middle_name': 'Сергеевна',
         'email': 'anna.zaytseva@example.com',
         'phone_number': '79331234570', 'passport_data': '4513 456789', 'INN': '456789012345'},
        {'id': 5, 'last_name': 'Кузнецов', 'first_name': 'Михаил', 'middle_name': 'Петрович',
         'email': 'mikhail.kuznetsov@example.com',
         'phone_number': '79441234571', 'passport_data': '4514 567890', 'INN': '567890123456'},
    ]

    products = [
        {'id': 1, 'product_name': 'Пальто зимнее', 'description': 'Женское, размер 48, цвет чёрный',
         'delivery_date': '2023-09-15', 'expiry_date': '2024-03-15', 'price': 4500.00, 'report_id': 1,
         'sale_id': None},
        {'id': 2, 'product_name': 'Ботинки кожаные', 'description': 'Мужские, размер 42, коричневые',
         'delivery_date': '2023-09-20', 'expiry_date': '2024-02-20', 'price': 3200.00, 'report_id': 2,
         'sale_id': 1},
        {'id': 3, 'product_name': 'Сумка женская', 'description': 'Кожаная, среднего размера, бежевая',
         'delivery_date': '2023-10-01', 'expiry_date': '2024-04-01', 'price': 2800.50, 'report_id': 3,
         'sale_id': None},
        {'id': 4, 'product_name': 'Часы наручные', 'description': 'Механические, мужские, сталь',
         'delivery_date': '2023-09-25', 'expiry_date': '2024-01-25', 'price': 12500.00, 'report_id': 4,
         'sale_id': 3},
        {'id': 5, 'product_name': 'Сервиз чайный', 'description': 'Фарфор, 12 персон, позолота',
         'delivery_date': '2023-10-05', 'expiry_date': '2024-05-05','price': 8900.00, 'report_id': 5,
         'sale_id': 4},
        {'id': 6, 'product_name': 'Шарф пуховый', 'description': 'Оренбургский, белый, ажурный',
         'delivery_date': '2023-10-10', 'expiry_date': '2024-01-10', 'price': 1500.00, 'report_id': 1,
         'sale_id': 5},
    ]

    sales = [
        {'id': 1, 'sale_date': '2023-10-01', 'sale_price': 1500.00,
         'commission': 150.00, 'status': 'Оплачено'},
        {'id': 2, 'sale_date': '2023-10-02', 'sale_price': 3200.50,
         'commission': 320.05, 'status': 'Ожидает'},
        {'id': 3, 'sale_date': '2023-10-03', 'sale_price': 780.00,
         'commission': 78.00, 'status': 'Оплачено'},
        {'id': 4, 'sale_date': '2023-10-04', 'sale_price': 2100.00,
         'commission': 210.00, 'status': 'Возврат'},
        {'id': 5, 'sale_date': '2023-10-05', 'sale_price': 540.75,
         'commission': 54.08, 'status': 'Оплачено'},
    ]

    reports = [
        {'id': 1, 'number': 'REP-001', 'date': '2023-10-01', 'report_type': 'Ежедневный отчет',
         'description': 'Отчет о продажах за день', 'consignor_id': 2},
        {'id': 2, 'number': 'REP-002', 'date': '2023-10-02', 'report_type': 'Еженедельный отчет',
         'description': 'Отчет о продажах за неделю', 'consignor_id': 3},
        {'id': 3, 'number': 'REP-003', 'date': '2023-10-03', 'report_type': 'Ежемесячный отчет',
         'description': 'Отчет о продажах за месяц', 'consignor_id': 4},
        {'id': 4, 'number': 'REP-004', 'date': '2023-10-04', 'report_type': 'Квартальный отчет',
         'description': 'Отчет о продажах за квартал', 'consignor_id': 5},
        {'id': 5, 'number': 'REP-005', 'date': '2023-10-05', 'report_type': 'Годовой отчет',
         'description': 'Отчет о продажах за год', 'consignor_id': 1},
    ]

    # Добавление комитентов
    for consignor_data in consignors:
        consignor = Consignor(
            first_name=consignor_data['first_name'],
            last_name=consignor_data['last_name'],
            middle_name=consignor_data['middle_name'], # может быть None
            email=consignor_data['email'],
            phone_number=consignor_data['phone_number'],
            passport_data=consignor_data['passport_data'],
            INN=consignor_data['INN'],
        )
        db.session.add(consignor)
    db.session.flush()

    # Добавление отчетов
    for report_data in reports:
        report = Report(
            number=report_data['number'],
            date=datetime.strptime(report_data['date'], '%Y-%m-%d').date(),
            report_type=report_data['report_type'],
            description=report_data['description'],
            consignor_id=report_data['consignor_id'],
        )
        db.session.add(report)
    db.session.flush()

    # Добавление продаж
    for sale_data in sales:
        sale = Sale(
            sale_date=datetime.strptime(sale_data['sale_date'], '%Y-%m-%d').date(),
            sale_price=sale_data['sale_price'],
            commission=sale_data['commission'],
            status=sale_data['status'],
        )
        db.session.add(sale)
    db.session.flush()

    # Добавление товаров
    for product_data in products:
        product = Product(
            product_name=product_data['product_name'],
            description=product_data['description'],
            delivery_date=datetime.strptime(product_data['delivery_date'], '%Y-%m-%d').date(),
            expiry_date=datetime.strptime(product_data['expiry_date'], '%Y-%m-%d').date(),
            price=product_data['price'],
            report_id=product_data['report_id'],
            sale_id=product_data['sale_id'],
        )
        db.session.add(product)

    # Сохранение изменений в базе данных
    db.session.commit()


def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        insert_test_data()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/consignors')
def consignors_list():
    consignors = Consignor.query.all()

    return render_template('consignors_list.html', consignors=consignors)


@app.route('/consignors/<consignor_id>')
def consignor_detail(consignor_id):
    consignor = Consignor.query.get_or_404(consignor_id)

    return render_template('consignor_detail.html', consignor=consignor)


@app.route('/add_consignor', methods=['GET', 'POST'])
def add_consignor():
    consignors = Consignor.query.all()
    if request.method == 'POST':
        last_name = request.form['last_name']
        first_name = request.form['first_name']
        middle_name = request.form['middle_name'] or 'Отсутствует'
        email = request.form['email']
        phone_number = request.form['phone_number']
        passport_data = request.form['passport_data']
        INN = request.form['INN']

        new_consignor = Consignor(
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
            email=email,
            phone_number=phone_number,
            passport_data=passport_data,
            INN=INN
        )
        db.session.add(new_consignor)
        db.session.commit()
        flash('Комитент успешно добавлен!', 'success')

        return redirect(url_for('consignors_list'))

    return render_template('add_consignor.html', consignors=consignors)


@app.route('/delete_consignor/<int:consignor_id>', methods=['POST'])
def delete_consignor(consignor_id):
    consignor = Consignor.query.get_or_404(consignor_id)

    # # Check for related employee
    # related_consignors = Sale.query.filter_by(sale_id=consignor_id).all()
    # if related_consignors:
    #     flash('Комитента нельзя удалить, так как есть связанные с ним продажи.', 'error')
    #     return redirect(url_for('employees_list'))
    #
    # # Check for related contracts
    # related_contracts = Report.query.filter_by(report_id=consignor_id).all()
    # if related_contracts:
    #     flash('Сотрудника нельзя удалить, так как есть связанные с ним отчёты.', 'error')
    #     return redirect(url_for('employees_list'))

    db.session.delete(consignor)
    db.session.commit()
    flash('Комитент успешно удалён!', 'success')

    return redirect(url_for('consignors_list'))


@app.route('/reports')
def reports_list():
    reports = Report.query.all()
    consignors = Consignor.query.all()
    # Создание словаря для быстрого доступа к именам комитентов по их идентификаторам
    consignors_dict = {consignor.id: f"{consignor.first_name} {consignor.last_name} {consignor.middle_name or ''}".strip() for consignor in consignors}

    return render_template('reports_list.html', reports=reports, consignors=consignors_dict)


@app.route('/report/<int:report_id>')
def report_detail(report_id):
    report = Report.query.get_or_404(report_id)
    consignor = Consignor.query.get(report.consignor_id)

    return render_template('report_detail.html', report=report, consignor=consignor)


@app.route('/add_report', methods=['GET', 'POST'])
def add_report():
    consignors = Consignor.query.all()
    if request.method == 'POST':
        number = request.form['number']
        date = request.form['date']
        report_type = request.form['report_type']
        description = request.form['description']
        consignor_id = request.form['consignor_id']

        date = datetime.strptime(date, '%Y-%m-%d')

        new_report = Report(
            number=number,
            date=date,
            report_type=report_type,
            description=description,
            consignor_id=consignor_id
        )
        db.session.add(new_report)
        db.session.commit()

        flash('Отчёт успешно добавлен!', 'success')

        return redirect(url_for('reports_list'))

    return render_template('add_report.html', consignors=consignors)


@app.route('/delete_report/<int:report_id>', methods=['POST'])
def delete_report(report_id):
    report = Report.query.get_or_404(report_id)
    db.session.delete(report)
    db.session.commit()
    flash('Отчёт успешно удалён!', 'success')

    return redirect(url_for('reports_list'))


@app.route('/sales')
def sales_list():
    sales = Sale.query.all()

    return render_template('sales_list.html', sales=sales)


@app.route('/sale/<int:sale_id>')
def sale_detail(sale_id):
    sale = Sale.query.get_or_404(sale_id)

    return render_template('sale_detail.html', sale=sale)


@app.route('/add_sale', methods=['GET', 'POST'])
def add_sale():
    if request.method == 'POST':
        sale_date = request.form['sale_date']
        sale_price = request.form['sale_price']
        commission = request.form['commission']
        status = request.form['status']

        # Convert date to a Python date object
        sale_date = datetime.strptime(sale_date, '%Y-%m-%d')

        new_sale = Sale(
            sale_date=sale_date,
            sale_price=sale_price,
            commission=commission,
            status=status
        )
        db.session.add(new_sale)
        db.session.commit()
        flash('Продажа успешно добавлена!', 'success')
        return redirect(url_for('sales_list'))
    return render_template('add_sale.html')


@app.route('/delete_sale/<int:sale_id>', methods=['POST'])
def delete_sale(sale_id):
    sale = Sale.query.get_or_404(sale_id)
    db.session.delete(sale)
    db.session.commit()
    flash('Продажа успешно удалена!', 'success')
    return redirect(url_for('sales_list'))


@app.route('/products')
def products_list():
    products = Product.query.all()
    reports = Report.query.all()
    sales = Sale.query.all()
    # Создание словаря для быстрого доступа к продажам и отчётам по их идентификаторам
    reports_dict = { report.id: report.number for report in reports }
    sales_dict = { sale.id: sale.status for sale in sales }

    return render_template('products_list.html', products=products, reports=reports_dict, sales=sales_dict)


@app.route('/products/<product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    report = Report.query.get(product.report_id)
    sale = Sale.query.get(product.sale_id)

    return render_template('product_detail.html', product=product, report=report, sale=sale)


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    reports = Report.query.all()
    sales = Sale.query.all()
    if request.method == 'POST':
        product_name = request.form['product_name']
        description = request.form['description']
        delivery_date = request.form['delivery_date']
        expiry_date = request.form['expiry_date']
        price = request.form['price']
        report_id = request.form['report_id']
        sale_id = request.form['sale_id'] or None

        # Convert date to a Python date object
        delivery_date = datetime.strptime(delivery_date, '%Y-%m-%d')
        expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d')

        new_product = Product(
            product_name=product_name,
            description=description,
            delivery_date=delivery_date,
            expiry_date=expiry_date,
            price=price,
            report_id=report_id,
            sale_id=sale_id
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Товар успешно добавлен!', 'success')

        return redirect(url_for('products_list'))

    return render_template('add_product.html', reports=reports, sales=sales)


@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Товар успешно удалён!', 'success')

    return redirect(url_for('products_list'))


if __name__ == "__main__":
    init_db() # создаст таблицы перед запуском сервера
    app.run() #debug=True

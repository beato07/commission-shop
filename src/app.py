from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, redirect, url_for, request, flash
from models import db, Consignor
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


# Для тестирования
def insert_test_data():
    consignors = [
        {'id': 1, 'first_name': 'Иван', 'last_name': 'Соколов', 'middle_name': 'Алексеевич', 'email': 'ivan.sokolov@example.com', 'phone_number': '79001234567', 'passport_data': '4510 123456', 'INN': '123456789012', 'sale_id': None, 'report_id': None},
        {'id': 2, 'first_name': 'Екатерина', 'last_name': 'Морозова', 'middle_name': 'Дмитриевна', 'email': 'ekaterina.morozova@example.com', 'phone_number': '79111234568', 'passport_data': '4511 234567', 'INN': '234567890123', 'sale_id': None, 'report_id': None},
        {'id': 3, 'first_name': 'Дмитрий', 'last_name': 'Волков', 'middle_name': None, 'email': 'dmitry.volkov@example.com', 'phone_number': '79221234569', 'passport_data': '4512 345678', 'INN': '345678901234', 'sale_id': None, 'report_id': None},
        {'id': 4, 'first_name': 'Анна', 'last_name': 'Зайцева', 'middle_name': 'Сергеевна', 'email': 'anna.zaytseva@example.com', 'phone_number': '79331234570', 'passport_data': '4513 456789', 'INN': '456789012345', 'sale_id': None, 'report_id': None},
        {'id': 5, 'first_name': 'Михаил', 'last_name': 'Кузнецов', 'middle_name': 'Петрович', 'email': 'mikhail.kuznetsov@example.com', 'phone_number': '79441234571', 'passport_data': '4514 567890', 'INN': '567890123456', 'sale_id': None, 'report_id': None}
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
            sale_id=consignor_data['sale_id'], # None или ID продажи
            report_id=consignor_data['report_id'] # None или ID отчёта
        )
        db.session.add(consignor)

    # Сохранение изменений в базе данных
    db.session.commit()


def init_db():
    with app.app_context():
        db.create_all()
        # insert_test_data()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/consignors')
def consignors_list():
    consignors = Consignor.query.all()
    return render_template('consignors_list.html', consignors=consignors)


@app.route('/consignors/<consignor_id>')
def consignor_detail(consignor_id):
    consignor = Consignor.query.get(consignor_id)
    sale, report = None, None
    if consignor.sale_id:
        sale = Consignor.query.get(consignor.sale_id)
    if consignor.report_id:
        report = Consignor.query.get(consignor.report_id)
    return render_template('consignor_detail.html', consignor=consignor, sale=sale, report=report)


@app.route('/add_consignor', methods=['GET', 'POST'])
def add_consignor():
    consignors = Consignor.query.all()
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        middle_name = request.form['middle_name'] or 'Отсутствует'
        email = request.form['email']
        phone_number = request.form['phone_number']
        passport_data = request.form['passport_data']
        INN = request.form['INN']
        sale_id = request.form.get('sale_id') or None
        report_id = request.form.get('report_id') or None
        new_consignor = Consignor(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            email=email,
            phone_number=phone_number,
            passport_data=passport_data,
            INN=INN,
            sale_id=sale_id,
            report_id=report_id
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


if __name__ == "__main__":
    init_db() # создаст таблицы перед запуском сервера
    app.run() #debug=True

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, redirect, url_for, request, flash
from models import db, Consignor, Report
from config import Config

from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


# Для тестирования
def insert_test_data():
    consignors = [
        {'id': 1, 'first_name': 'Иван', 'last_name': 'Соколов', 'middle_name': 'Алексеевич', 'email': 'ivan.sokolov@example.com', 'phone_number': '79001234567', 'passport_data': '4510 123456', 'INN': '123456789012'},
        {'id': 2, 'first_name': 'Екатерина', 'last_name': 'Морозова', 'middle_name': 'Дмитриевна', 'email': 'ekaterina.morozova@example.com', 'phone_number': '79111234568', 'passport_data': '4511 234567', 'INN': '234567890123'},
        {'id': 3, 'first_name': 'Дмитрий', 'last_name': 'Волков', 'middle_name': None, 'email': 'dmitry.volkov@example.com', 'phone_number': '79221234569', 'passport_data': '4512 345678', 'INN': '345678901234'},
        {'id': 4, 'first_name': 'Анна', 'last_name': 'Зайцева', 'middle_name': 'Сергеевна', 'email': 'anna.zaytseva@example.com', 'phone_number': '79331234570', 'passport_data': '4513 456789', 'INN': '456789012345'},
        {'id': 5, 'first_name': 'Михаил', 'last_name': 'Кузнецов', 'middle_name': 'Петрович', 'email': 'mikhail.kuznetsov@example.com', 'phone_number': '79441234571', 'passport_data': '4514 567890', 'INN': '567890123456'}
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
            # sale_id=consignor_data['sale_id'], # None или ID продажи
            # report_id=consignor_data['report_id'] # None или ID отчёта
        )
        db.session.add(consignor)

    # Сохранение изменений в базе данных
    db.session.commit()

    # Добавление отчетов
    for report_data in reports:
        report = Report(
            number=report_data['number'],
            date=datetime.strptime(report_data['date'], '%Y-%m-%d').date(),
            report_type=report_data['report_type'],
            description=report_data['description'],
            consignor_id=report_data['consignor_id']
        )
        db.session.add(report)

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
    consignor = Consignor.query.get(consignor_id)
    return render_template('consignor_detail.html', consignor=consignor)


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
        new_consignor = Consignor(
            first_name=first_name,
            last_name=last_name,
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

        # Convert date to a Python date object
        date = datetime.strptime(date, '%Y-%m-%d')

        # Create and save the report
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


if __name__ == "__main__":
    init_db() # создаст таблицы перед запуском сервера
    app.run() #debug=True

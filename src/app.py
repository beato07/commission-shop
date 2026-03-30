import psycopg2
from flask import Flask, render_template
from models import db
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


def init_db():
    with app.app_context():
        db.create_all()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/consignors")
def consignors_list():
    return render_template('consignors_list.html')


if __name__ == "__main__":
    init_db() # создаст таблицы перед запуском сервера
    app.run(debug=True)

from flask import Flask, url_for, request, redirect, abort, render_template, session
import datetime
from flask_sqlalchemy import SQLAlchemy
from lab8_db import db
from os import path
from flask_login import LoginManager
from lab8_db.models import users

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from lab9 import lab9
from rgz import rgz
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретный_ключ123')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

if app.config['DB_TYPE'] == 'postgres':
  db_name = 'stas_konev_orm'
  db_user = 'stas_konev_orm'
  db_password = '123'
  host_ip = '127.0.0.1'
  host_port = 5432
  app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
  dir_path = path.dirname(path.realpath(__file__))
  db_path = path.join(dir_path, "stas_konev_orm.db")
  app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'lab8.login'

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(lab9)

app.register_blueprint(rgz)

@app.route('/')
@app.route('/index')
def index():
    return '''<!doctype html>
<html>
    <head>
    <meta charset="utf-8">
    <title>НГТУ, ФБ — Лабораторные работы</title>
    <style>
        body {
            font-family: Arial;
            background: #f7f7f7;
            margin: 0;
            padding: 0;
            color: #333;
        }
        header {
            background: #9bc5e8;
            padding: 15px;
            text-align: center;
        }
        header h1 {
            font-size: 22px;
            margin: 5px 0;
            font-weight: normal;
            color: #1a3c5a;
        }
        nav {
            background: white;
            padding: 15px 25px;
            border-top: 1px solid #ddd;
        }
        nav ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        nav ul li {
            margin: 8px 0;
        }
        nav a {
            text-decoration: none;
            font-size: 17px;
            color: #1a3c5a;
        }
        nav a:hover {
            text-decoration: underline;
        }
        footer {
            margin-top: 40px;
            background: #9bc5e8;
            color: #1a3c5a;
            text-align: center;
            padding: 10px;
            font-size: 14px;
        }
    </style>
</head>
<body>
<header>
    <h1>WEB-программирование, часть 2 — Лабораторные</h1>
</header>

<nav>
    <ul>
        <li><a href="/lab1">Лабораторная работа №1</a></li>
        <li><a href="/lab2">Лабораторная работа №2</a></li>
        <li><a href="/lab3">Лабораторная работа №3</a></li>
        <li><a href="/lab4">Лабораторная работа №4</a></li>
        <li><a href="/lab5">Лабораторная работа №5</a></li>
        <li><a href="/lab6">Лабораторная работа №6</a></li>
        <li><a href="/lab7">Лабораторная работа №7</a></li>
        <li><a href="/lab8">Лабораторная работа №8</a></li>
        <li><a href="/lab9">Лабораторная работа №9</a></li>
        <li><a href="/rgz/">РГЗ — Камера хранения</a></li>
    </ul>
</nav>

<footer>
    Конев Станислав Сергеевич, ФБИ-34, 3 курс, 2025
</footer>
</body>
</html>
'''


journal = []

 
@app.errorhandler(404)
def not_found(err):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip = request.remote_addr
    url = request.url

    entry = f"{time} — {ip} — {url}"
    journal.append(entry)

    log_html = "<h3>Журнал:</h3><ul>"
    for record in journal[-10:]:
        log_html += f"<li>{record}</li>"
    log_html += "</ul>"

    img = url_for('static', filename='404.png')

    return f'''<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>Ошибка 404</title>
    <style>
      body {{
        background: white;
        color: black;
        font-family: Arial;
        text-align: center;
        padding: 40px;
      }}
      h1 {{
        color: black;
      }}
      img {{
        width: 250px;
        margin: 20px;
      }}
      .journal {{
        text-align: left;
        margin-top: 30px;
      }}
    </style>
</head>
<body>
  <h1>Страница не найдена</h1>
  <p><b>Ваш IP:</b> {ip}</p>
  <p><b>Дата и время:</b> {time}</p>
  <p><a href="/">Вернуться на главную</a></p>
  <img src="{img}" alt="404">
  <div class="journal">
    {log_html}
  </div>
</body>
</html>''', 404


@app.errorhandler(500)
def handle_500(err):
    return '''<!doctype html>
<html>
<head><meta charset="utf-8"><title>Ошибка 500</title></head>
<body>
  <h1>Внутренняя ошибка сервера (500)</h1>
  <p>Произошла ошибка. Попробуйте позже.</p>
  <a href="/">На главную</a>
</body>
</html>''', 500
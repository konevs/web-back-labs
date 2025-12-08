from flask import Flask, url_for, request, redirect, abort, render_template, session
import datetime
import os

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from rgz import rgz

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретный_ключ123')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)

app.register_blueprint(rgz, url_prefix='/rgz')

@app.route('/')
@app.route('/index')
def index():
    return '''
<!doctype html>
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
        <li><a href="/lab8">Восьмая лабораторная</a></li>
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

    log_html = "<h3 style='font-size:18px;'>Журнал последних ошибок:</h3><ul>"
    for record in journal[-10:]:
        log_html += f"<li>{record}</li>"
    log_html += "</ul>"

    try:
        img = url_for('static', filename='404.png')
    except:
        img = ""

    return f'''
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>Ошибка 404</title>
    <style>
        body {{
            font-family: Arial;
            background: #f7f7f7;
            color: #333;
            text-align: center;
            padding: 40px;
        }}
        h1 {{
            font-size: 24px;
            margin-bottom: 10px;
            color: #b53333;
            font-weight: normal;
        }}
        img {{
            width: 230px;
            margin: 20px;
            opacity: 0.9;
        }}
        a {{
            font-size: 16px;
            color: #1a3c5a;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .journal {{
            margin-top: 20px;
            text-align: left;
            display: inline-block;
            font-size: 14px;
        }}
    </style>
</head>
<body>
<h1>Страница не найдена</h1>
<p><b>IP:</b> {ip}</p>
<p><b>Время:</b> {time}</p>
<p><a href="/">Перейти на главную</a></p>
<!-- Если картинки нет, браузер покажет иконку "битого изображения", но сервер не упадет -->
<img src="{img}" alt="">
<div class="journal">
    {log_html}
</div>
</body>
</html>
''', 404

@app.errorhandler(500)
def handle_500(err):
    return '''
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>Ошибка 500</title>
    <style>
        body {
            background: #f7f7f7;
            font-family: Arial;
            text-align: center;
            padding: 40px;
            color: #333;
        }
        h1 {
            font-size: 24px;
            color: #b53333;
            font-weight: normal;
        }
        a {
            font-size: 16px;
            color: #1a3c5a;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
<h1>Внутренняя ошибка сервера</h1>
<p>Попробуйте обновить страницу позже.</p>
<p><a href="/">Вернуться на главную</a></p>
</body>
</html>
''', 500
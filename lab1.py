from flask import Blueprint, url_for, redirect, request
import datetime

lab1 = Blueprint('lab1', __name__)

STYLE = """
<style>
body {
    font-family: Arial, sans-serif;
    background: #f5f5f5;
    padding: 40px;
    color: #222;
}
.container {
    background: white;
    max-width: 800px;
    margin: auto;
    padding: 30px;
    border-radius: 14px;
    box-shadow: 0 0 12px rgba(0,0,0,0.1);
}
h1 {
    text-align: center;
    margin-bottom: 25px;
}
a {
    color: #0066cc;
    text-decoration: none;
    font-weight: bold;
}
a:hover {
    text-decoration: underline;
}
.nav {
    margin: 20px 0;
    text-align: center;
}
ul {
    margin-top: 15px;
}
img {
    max-width: 100%;
    border-radius: 10px;
}
.counter-box {
    background: #e8f5ff;
    padding: 15px;
    border-radius: 10px;
}
</style>
"""

@lab1.route('/lab1')
def lab():
    return f'''<!doctype html>
<html>
<head><meta charset="utf-8"><title>Лабораторная 1</title>{STYLE}</head>
<body>
<div class="container">
    <h1>Лабораторная работа 1</h1>

    <p>
        Flask — фреймворк для создания веб-приложений на Python.  
        Он использует Werkzeug и Jinja2, относится к микрофреймворкам — то есть содержит только базовую структуру, 
        предоставляя программисту максимальную гибкость.
    </p>

    <div class="nav"><a href="/">Вернуться на главную</a></div>

    <h2>Список роутов</h2>
    <ul>
        <li><a href="/">Главная страница</a></li>
        <li><a href="/index">Index</a></li>
        <li><a href="/lab1/web">web</a></li>
        <li><a href="/lab1/author">author</a></li>
        <li><a href="/lab1/image">image</a></li>
        <li><a href="/lab1/counter">counter</a></li>
        <li><a href="/lab1/counter/clear">counter_clear</a></li>
        <li><a href="/lab1/info">info</a></li>
        <li><a href="/lab1/created">created</a></li>
        <li><a href="400">400 Bad Request</a></li>
        <li><a href="401">401 Unauthorized</a></li>
        <li><a href="402">402 Payment Required</a></li>
        <li><a href="403">403 Forbidden</a></li>
        <li><a href="404">404 Not Found</a></li>
        <li><a href="405">405 Method Not Allowed</a></li>
        <li><a href="418">418 I'm a teapot</a></li>
        <li><a href="/cause_500">500 internal error</a></li>
    </ul>
</div>
</body>
</html>'''


@lab1.route("/lab1/web")
def web():
    return """<!doctype html>
<html>
<body>
<h1>web-сервер на flask</h1>
<a href="/lab1/author">author</a>
</body>
</html>""", 200, {
        "X-Server": "sample",
        'Content-Type': 'text/plain; charset=utf-8'
    }


@lab1.route("/lab1/author")
def author():
    name = "Конев Станислав Сергеевич"
    group = "ФБИ-34"
    faculty = "ФБ"

    return f'''<!doctype html>
<html>
<head><meta charset="utf-8"><title>Автор</title>{STYLE}</head>
<body>
<div class="container">
    <h1>Автор работы</h1>

    <p><b>Студент:</b> {name}</p>
    <p><b>Группа:</b> {group}</p>
    <p><b>Факультет:</b> {faculty}</p>

    <div class="nav">
        <a href="/lab1/web">Назад</a>
    </div>
</div>
</body>
</html>'''


@lab1.route('/lab1/image')
def image():
    css = url_for('static', filename='lab1/lab1.css')
    img = url_for('static', filename='lab1/oak.jpg')

    return f'''<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Дуб</title>
<link rel="stylesheet" href="{css}">
{STYLE}
</head>
<body>
<div class="container">
    <h1>Дуб</h1>
    <img src="{img}" alt="Дуб">
</div>
</body>
</html>''', 200, {
        'Content-Language': 'ru',
        'X-Project': 'lab1',
        'X-Author': 'Konev'
    }


count = 0

@lab1.route('/lab1/counter')
def counter():
    global count
    count += 1

    time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    url = request.url
    client_ip = request.remote_addr
    clear_url = url_for('lab1.clear_counter')

    return f'''<!doctype html>
<html>
<head><meta charset="utf-8"><title>Счётчик</title>{STYLE}</head>
<body>
<div class="container">
    <h1>Счётчик посещений</h1>

    <div class="counter-box">
        Вы заходили на эту страницу: <b>{count}</b> раз(а)
    </div>

    <p><b>Дата и время:</b> {time}</p>
    <p><b>Адрес запроса:</b> {url}</p>
    <p><b>IP-адрес:</b> {client_ip}</p>

    <a href="{clear_url}">Очистить счётчик</a>
</div>
</body>
</html>'''


@lab1.route('/lab1/counter/clear')
def clear_counter():
    global count
    count = 0
    return redirect(url_for('lab1.counter'))


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@lab1.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
<body>
<h1>Создано успешно</h1>
<i>что-то создано...</i>
</body>
</html>
''', 201


@lab1.route("/400")
def bad_request():
    return "<h1>400 Bad Request</h1>", 400

@lab1.route("/401")
def unauthorized():
    return "<h1>401 Unauthorized</h1>", 401

@lab1.route("/402")
def payment_required():
    return "<h1>402 Payment Required</h1>", 402

@lab1.route("/403")
def forbidden():
    return "<h1>403 Forbidden</h1>", 403

@lab1.route("/405")
def method_not_allowed():
    return "<h1>405 Method Not Allowed</h1>", 405

@lab1.route("/418")
def teapot():
    return "<h1>418 I'm a teapot</h1>", 418


@lab1.route('/cause_500')
def cause_500():
    raise RuntimeError("Ошибка для проверки 500")

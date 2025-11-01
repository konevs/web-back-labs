from flask import Blueprint, url_for, redirect, request, abort, render_template

lab2 = Blueprint('lab2', __name__)


@lab2.route('/lab2/a')
def a1():
    return 'без слэша'


@lab2.route('/lab2/a/')
def a2():
    return 'со слэшем'


flower_list = [
    {"name": "роза", "price": 100},
    {"name": "тюльпан", "price": 70},
    {"name": "незабудка", "price": 50},
    {"name": "ромашка", "price": 40},
]


@lab2.route('/lab2/add_flower/')
def add_flower_post():
    name = request.form.get("name")
    price = request.form.get("price")
    if not name or not price:
        return "Ошибка: не заданы имя или цена", 400
    flower_list.append({"name": name, "price": int(price)})
    return redirect("/lab2/flowers/")


@lab2.route('/lab2/add_flower/')
def add_flower_no_name():
    return "вы не задали имя цветка", 400


@lab2.route('/lab2/flowers/')
def all_flowers():
    return render_template("lab2/flowers.html", flowers=flower_list)


@lab2.route('/lab2/flowers/delete/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    flower_list.pop(flower_id)
    return redirect('/lab2/flowers/')


@lab2.route('/lab2/flowers/clear')
def clear_flowers():
    flower_list.clear()
    return redirect('/lab2/flowers/')


@lab2.route('/lab2/example')
def example():
    name, number, group, course = 'Станислав Конев',  '2', 'ФБИ-34',  '3 курс'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('lab2/example.html', name=name, number=number, group=group, 
                           course=course, fruits=fruits)


@lab2.route('/lab2/')
def lab(): 
    return render_template('lab2/lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('lab2/filter.html', phrase=phrase)


@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return f'''
    <!doctype html>
    <html>
    <head><meta charset="utf-8"><title>Калькулятор</title></head>
    <body>
        <h1>Калькулятор</h1>
        <ul>
            <li>{a} + {b} = {a + b}</li>
            <li>{a} - {b} = {a - b}</li>
            <li>{a} * {b} = {a * b}</li>
            <li>{a} / {b if b != 0 else 1} = {a / b if b != 0 else 'Нельзя делить на 0'}</li>
            <li>{a} ** {b} = {a ** b}</li>
        </ul>
        <p><a href="/lab2/">Назад</a></p>
    </body>
    </html>
    '''


@lab2.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')


@lab2.route('/lab2/calc/<int:a>')
def calc_a(a):
    return redirect(f'/lab2/calc/{a}/1')

books = [
    {'author': 'Дж. Роулинг', 'title': 'Гарри Поттер', 'genre': 'Фэнтези', 'pages': 400},
    {'author': 'Дж. Толкин', 'title': 'Властелин колец', 'genre': 'Фэнтези', 'pages': 800},
    {'author': 'А. Кристи', 'title': 'Убийство в Восточном экспрессе', 'genre': 'Детектив', 'pages': 250},
    {'author': 'С. Кинг', 'title': 'Оно', 'genre': 'Ужасы', 'pages': 700},
    {'author': 'Э. Ремарк', 'title': 'Три товарища', 'genre': 'Роман', 'pages': 350},
    {'author': 'Г. Уэллс', 'title': 'Война миров', 'genre': 'Фантастика', 'pages': 280},
    {'author': 'А. Дюма', 'title': 'Три мушкетера', 'genre': 'Приключения', 'pages': 600},
    {'author': 'Д. Оруэлл', 'title': '1984', 'genre': 'Антиутопия', 'pages': 320},
    {'author': 'Р. Брэдбери', 'title': '451 по Фаренгейту', 'genre': 'Фантастика', 'pages': 200},
    {'author': 'Х. Мураками', 'title': 'Норвежский лес', 'genre': 'Роман', 'pages': 380}
]

@lab2.route('/lab2/books')
def books_list():
    return render_template('books.html', books=books)

fruits = [
    {"name": "Яблоко", "desc": "Сочное красное яблоко", "img": "lab2/apple.jpg"},
    {"name": "Банан", "desc": "Спелый желтый банан", "img": "lab2/banana.jpg"},
    {"name": "Апельсин", "desc": "Сладкий сочный апельсин", "img": "lab2/orange.jpg"},
    {"name": "Клубника", "desc": "Свежая ароматная клубника", "img": "lab2/strawberry.jpg"},
    {"name": "Виноград", "desc": "Сладкий зеленый виноград", "img": "lab2/grape.jpg"},
    {"name": "Персик", "desc": "Мягкий спелый персик", "img": "lab2/peach.jpg"},
    {"name": "Груша", "desc": "Сочная сладкая груша", "img": "lab2/pear.jpg"},
    {"name": "Ананас", "desc": "Спелый тропический ананас", "img": "lab2/pineapple.jpg"},
    {"name": "Манго", "desc": "Ароматное спелое манго", "img": "lab2/mango.jpg"},
    {"name": "Киви", "desc": "Свежий зеленый киви", "img": "lab2/kiwi.jpg"},
    {"name": "Лимон", "desc": "Ароматный желтый лимон", "img": "lab2/lemon.jpg"},
    {"name": "Гранат", "desc": "Спелый рубиновый гранат", "img": "lab2/pomegranate.jpg"},
    {"name": "Арбуз", "desc": "Сладкий сочный арбуз", "img": "lab2/watermelon.jpg"},
    {"name": "Дыня", "desc": "Ароматная спелая дыня", "img": "lab2/melon.jpg"},
    {"name": "Мандарин", "desc": "Сладкий цитрусовый мандарин", "img": "lab2/mandarin.jpg"},
    {"name": "Слива", "desc": "Сочная фиолетовая слива", "img": "lab2/plum.jpg"},
    {"name": "Вишня", "desc": "Кисло-сладкая красная вишня", "img": "lab2/cherry.jpg"},
    {"name": "Черешня", "desc": "Сладкая темная черешня", "img": "lab2/sweet_cherry.jpg"},
    {"name": "Абрикос", "desc": "Нежный спелый абрикос", "img": "lab2/apricot.jpg"},
    {"name": "Инжир", "desc": "Спелый сладкий инжир", "img": "lab2/fig.jpg"}
]

@lab2.route('/lab2/fruits')
def fruits_gallery():
    return render_template('lab2/fruits.html', fruits=fruits)
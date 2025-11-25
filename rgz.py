from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3
import hashlib
from werkzeug.security import check_password_hash, generate_password_hash

rgz = Blueprint('rgz', __name__, url_prefix='/rgz', template_folder='templates', static_folder='static')

def get_db():
    conn = sqlite3.connect('rgz.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    login TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    is_admin BOOLEAN DEFAULT 0
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS locker (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner_id INTEGER DEFAULT NULL
                )''')
    c.execute('SELECT count(*) FROM locker')
    if c.fetchone()[0] == 0:
        for _ in range(100):
            c.execute('INSERT INTO locker (owner_id) VALUES (NULL)')
    conn.commit()
    conn.close()

init_db()

def get_current_user():
    if 'user_id' in session:
        conn = get_db()
        user = conn.execute('SELECT * FROM user WHERE id = ?', (session['user_id'],)).fetchone()
        conn.close()
        return user
    return None

def generate_pastel_color(username):
    if not username:
        return "#ccc"
        
    hash_object = hashlib.md5(username.encode())
    hex_hash = hash_object.hexdigest()
    
    hue = int(hex_hash[:2], 16) * 360 // 255
    
    return f"hsl({hue}, 70%, 80%)"

@rgz.route('/')
def index():
    user = get_current_user()
    conn = get_db()
    
    lockers_db = conn.execute('''
        SELECT locker.id, locker.owner_id, user.login as owner_name 
        FROM locker 
        LEFT JOIN user ON locker.owner_id = user.id
    ''').fetchall()
    conn.close()

    lockers = []
    occupied_count = 0
    my_count = 0

    for l in lockers_db:
        is_free = (l['owner_id'] is None)
        is_mine = (user and l['owner_id'] == user['id'])
        owner_name = l['owner_name'] if l['owner_name'] else 'Неизвестно'
        
        
        cell_color = ""
        if not is_free and not is_mine:
             cell_color = generate_pastel_color(owner_name)
        
        if not is_free:
            occupied_count += 1
        if is_mine:
            my_count += 1

        lockers.append({
            'id': l['id'],
            'free': is_free,
            'mine': is_mine,
            'owner': owner_name,
            'color': cell_color
        })

    total = len(lockers)
    free_count = total - occupied_count

    return render_template('rgz/rgz.html', 
                           lockers=lockers, 
                           user=user, 
                           total=total, 
                           occupied=occupied_count, 
                           free=free_count, 
                           my_count=my_count)

@rgz.route('/booking', methods=['POST'])
def booking():
    user = get_current_user()
    if not user:
        flash('Необходимо войти в систему', 'error')
        return redirect(url_for('rgz.login'))
    if user['is_admin']:
        flash('Администраторы не могут бронировать ячейки', 'error')
        return redirect(url_for('rgz.index'))

    locker_id = request.form.get('locker_id')
    conn = get_db()
    count = conn.execute('SELECT count(*) FROM locker WHERE owner_id = ?', (user['id'],)).fetchone()[0]
    if count >= 5:
        flash('Вы не можете занять больше 5 ячеек', 'error')
        conn.close()
        return redirect(url_for('rgz.index'))

    locker = conn.execute('SELECT owner_id FROM locker WHERE id = ?', (locker_id,)).fetchone()
    if locker and locker['owner_id'] is None:
        conn.execute('UPDATE locker SET owner_id = ? WHERE id = ?', (user['id'], locker_id))
        conn.commit()
    else:
        flash('Ячейка уже занята', 'error')

    conn.close()
    return redirect(url_for('rgz.index'))

@rgz.route('/cancellation', methods=['POST'])
def cancellation():
    user = get_current_user()
    if not user:
        return redirect(url_for('rgz.login'))

    locker_id = request.form.get('locker_id')
    conn = get_db()
    locker = conn.execute('SELECT owner_id FROM locker WHERE id = ?', (locker_id,)).fetchone()

    if locker and (locker['owner_id'] == user['id'] or user['is_admin']):
        conn.execute('UPDATE locker SET owner_id = NULL WHERE id = ?', (locker_id,))
        conn.commit()
    
    conn.close()
    return redirect(url_for('rgz.index'))

@rgz.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        conn = get_db()
        user = conn.execute('SELECT * FROM user WHERE login = ?', (login,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('rgz.index'))
        else:
            flash('Неверный логин или пароль', 'error')
    return render_template('rgz/login.html')

@rgz.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        hashed_pw = generate_password_hash(password)
        conn = get_db()
        try:
            is_admin = (conn.execute('SELECT count(*) FROM user').fetchone()[0] == 0)
            conn.execute('INSERT INTO user (login, password, is_admin) VALUES (?, ?, ?)', (login, hashed_pw, is_admin))
            conn.commit()
            flash('Регистрация успешна!', 'success')
            return redirect(url_for('rgz.login'))
        except sqlite3.IntegrityError:
            flash('Логин занят', 'error')
        finally:
            conn.close()
    return render_template('rgz/register.html')

@rgz.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('rgz.login', logout=True))

@rgz.route('/delete-account', methods=['POST'])
def delete_account():
    if 'user_id' in session:
        uid = session['user_id']
        conn = get_db()
        conn.execute('UPDATE locker SET owner_id = NULL WHERE owner_id = ?', (uid,))
        conn.execute('DELETE FROM user WHERE id = ?', (uid,))
        conn.commit()
        conn.close()
        session.pop('user_id', None)
    return redirect(url_for('rgz.login', deleted=True))
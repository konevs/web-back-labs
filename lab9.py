from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for
import random

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/', methods=['GET', 'POST'])
def main():
    if 'gift_list' not in session:
        init_gifts()
    elif len(session['gift_list']) > 0 and 'position_css' not in session['gift_list'][0]:
        init_gifts()
        
    opened_count = sum(1 for gift in session['gift_list'] if gift['open'])
    
    return render_template('lab9/index.html', 
                           gifts=session['gift_list'], 
                           count=opened_count)

@lab9.route('/lab9/open', methods=['POST'])
def open_gift():
    gift_id = int(request.form.get('gift_id'))
    gift_list = session.get('gift_list', [])
    
    gift = next((g for g in gift_list if g['id'] == gift_id), None)
    
    if not gift:
        return jsonify({'error': 'Подарок не найден'}), 404

    if gift['open']:
        return jsonify({'message': 'Уже открыто', 'gift': gift}), 200

    opened_count = sum(1 for g in gift_list if g['open'])
    if opened_count >= 3:
        return jsonify({'error': 'Можно открыть не более 3-х подарков!'}), 400

    gift['open'] = True
    session['gift_list'] = gift_list 
    
    return jsonify({'result': 'success', 'gift': gift}), 200

@lab9.route('/lab9/reset', methods=['POST'])
def reset_gifts():
    init_gifts()
    return redirect('/lab9/')

def init_gifts():
    greetings = [
        "Счастья!", "Здоровья!", "Богатства!", "Любви!", 
        "Удачи!", "Вдохновения!", "Побед!", "Путешествий!", 
        "Радости!", "Тепла!"
    ]
    
    gifts = []
    for i in range(10):
        file_num = i + 1 
        x = random.randint(5, 90)
        y = random.randint(5, 70)
        
        gifts.append({
            'id': i,
            'x': x,
            'y': y,
            'open': False,
            'message': greetings[i],
            'image_closed': f"box{file_num}.jpg",
            'image_open': f"gift{file_num}.jpg",
            'position_css': f"left: {x}%; top: {y}%;"
        })
    
    session['gift_list'] = gifts
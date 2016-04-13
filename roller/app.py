from flask import Flask, render_template, session, request, abort, redirect, url_for
from flask_socketio import SocketIO, emit
from datetime import datetime
from random import randint

import eventlet
eventlet.monkey_patch()


app = Flask(__name__)
app.config.from_pyfile('config.cfg')
socketio = SocketIO(app)
users = []
dice_history = []


def name():
    return session.get('name', '')


@app.route('/')
def index():
    if not name():
        return render_template('login.html')
    return render_template('index.html')


@app.route('/setname', methods=['GET', 'POST'])
def set_name():
    name = request.form.get('name')
    if name:
        session['name'] = name
        return redirect(url_for('index'))
    else:
        abort(400)


@app.route('/history')
def history():
    return render_template('history.html', history=reversed(dice_history))


@app.route('/history/clear')
def clear_history():
    global dice_history
    dice_history = []
    emit('roll_event', {}, broadcast=True, namespace='/roll')
    return redirect(url_for('index'))


@app.route('/logout')
def logout_page():
    session.clear()
    return redirect(url_for('index'))


@socketio.on('connect', namespace='/roll')
def handle_connect():
    if not name() in users:
        users.append(name())
    emit('users', '<br>'.join(sorted(users)), broadcast=True)


@socketio.on('disconnect', namespace='/roll')
def handle_disconnect():
    if name() in users:
        users.remove(name())
    emit('users', '<br>'.join(sorted(users)), broadcast=True)


@socketio.on('roll_request',  namespace='/roll')
def handle_roll_request(message):
    try:
        ability = int(message.get('ability') or 2)
        bonus = int(message.get('bonus') or 0)
        total = 0
        rolls = []
        keep_rolls = []
        all_rolls = []
        for _ in range(ability + bonus):
            rolls.append(randint(1, 6))
        all_rolls = map(str, rolls)
        for _ in range(ability):
            keep_rolls.append(rolls.pop(rolls.index(max(rolls))))
        total = sum(keep_rolls)
        keep_rolls = map(str, keep_rolls)
        dice_history.append(History(name(), '{}, {}'.format(ability, bonus),
            '{} -> {} -> {}'.format(','.join(all_rolls), ','.join(keep_rolls), total)))
        emit('roll_event', {}, broadcast=True)
    except Exception as e:
        print(e)


class History:

    def __init__(self, name, dice, result):
        self.name = name
        self.dice = dice
        self.result = result
        self.date = datetime.now().strftime('%I:%M:%S %p')

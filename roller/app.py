from flask import Flask, render_template, session, request, abort, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_redis import Redis
from datetime import datetime
from random import randint
import json

import eventlet
eventlet.monkey_patch()


app = Flask(__name__)
app.config.from_pyfile('config.cfg')
socketio = SocketIO(app)
redis = Redis(app)
users = []


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
    history = [History.from_json(js) for js in redis.lrange('history', 0, redis.llen('history'))]
    return render_template('history.html', history=history)


@app.route('/history/clear')
def clear_history():
    redis.delete('history')
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
        h = History(name(), '{}, {}'.format(ability, bonus), '{} -> {} -> {}'.format(','.join(all_rolls), ','.join(keep_rolls), total))
        redis.lpush('history', h.to_json())
        emit('roll_event', {}, broadcast=True)
    except Exception as e:
        print(e)


class History:

    def __init__(self, name, dice, result, date=None):
        self.name = name
        self.dice = dice
        self.result = result
        self.date = date or datetime.now().strftime('%I:%M:%S %p')

    def to_json(self):
        return json.dumps({
            'name': self.name,
            'dice': self.dice,
            'result': self.result,
            'date': self.date
        })

    @staticmethod
    def from_json(s):
        j = json.loads(s.decode('utf-8'))
        return History(j['name'], j['dice'], j['result'], j['date'])

from flask import Flask, jsonify, request
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
users = {}
__all__ = ['app', 'socketio']


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@app.route('/history')
def history():
    history = []
    for item in redis.lrange('history', 0, redis.llen('history')):
        history.append(json.loads(item.decode('utf-8')))
    return jsonify({'history': history})


@app.route('/history/clear')
def clear_history():
    redis.delete('history')
    emit('roll_event', {}, broadcast=True)
    return jsonify({})


@app.route('/users')
def get_users():
    return jsonify(online_users())


def name():
    for sid, name in users.items():
        if sid == request.sid:
            return name


def online_users():
    ret = []
    for u in users.values():
        if u:
            ret.append(u)
    print(ret)
    return {'users': ret}


@socketio.on('connect')
def handle_connect():
    users[request.sid] = ''
    emit('users', online_users(), broadcast=True)


@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in users:
        del users[request.sid]
        emit('users', online_users(), broadcast=True)


@socketio.on('setname')
def handle_set_name(message):
    users[request.sid] = message.get('name')
    emit('users', online_users(), broadcast=True)


@socketio.on('leave')
def handle_leave():
    if request.sid in users:
        print('{} is leaving'.format(name()))
        del users[request.sid]
    emit('users', online_users(), broadcast=True)


@socketio.on('roll_request')
def handle_roll_request(message):
    try:
        print('handle_roll_request')
        ability = int(message.get('ability') or 2)
        bonus = int(message.get('bonus') or 0)
        static = int(message.get('static') or 0)
        total = 0
        rolls = []
        keep_rolls = []
        all_rolls = []
        for _ in range(ability + bonus):
            rolls.append(randint(1, 6))
        all_rolls = list(map(str, rolls))
        for _ in range(ability):
            keep_rolls.append(rolls.pop(rolls.index(max(rolls))))
        total = sum(keep_rolls)
        keep_rolls = map(str, keep_rolls)
        h = None
        if static:
            h = History(name(), '{}, {}'.format(ability, bonus), '{} -> {} -> {} -> {}'.format(
                ','.join(all_rolls) + '+' + str(static),
                ','.join(keep_rolls) + '+' + str(static),
                str(total) + '+' + str(static),
                str(total + static)))
        else:
            h = History(name(), '{}, {}'.format(ability, bonus), '{} -> {} -> {}'.format(','.join(all_rolls), ','.join(keep_rolls), total + static))
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

from flask import Flask, render_template, session, request, abort, redirect, url_for
from flask_socketio import SocketIO, emit
from datetime import datetime

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
    return render_template('history.html', history=dice_history)


@app.route('/logout')
def logout_page():
    session.clear()
    return redirect(url_for('index'))


@socketio.on('connect', namespace='/roll')
def handle_connect():
    if not name() in users:
        users.append(name())
    emit('users', '<br>'.join(users), broadcast=True)


@socketio.on('disconnect', namespace='/roll')
def handle_disconnect():
    if name() in users:
        users.remove(name())
    emit('users', '<br>'.join(users), broadcast=True)


@socketio.on('roll_request',  namespace='/roll')
def handle_roll_request(message):
    ability = message.get('ability') or 2
    specialty = message.get('specialty') or 0
    # TODO: how does rolling in this system work?
    dice_history.append(History(name(), '{}, {}'.format(ability, specialty), '?'))
    emit('roll_event',
        {'message': 'foobar', 'date': datetime.now().strftime('%I:%M:%S %p')},
        broadcast=True)


class History:

    def __init__(self, name, dice, result):
        self.name = name
        self.dice = dice
        self.result = result

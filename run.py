#!/usr/bin/env python
from roller import app, socketio


socketio.run(app, debug=True)

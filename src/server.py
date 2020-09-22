from flask_socketio import Namespace, emit
from flask import Flask, render_template
from flask_socketio import SocketIO
# https://flask-socketio.readthedocs.io/en/latest/

from single_log.log import Logger

import version


class EchoNamespace(Namespace):
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_my_event(self, data):
        emit('my_response', data)


if __name__ == '__main__':
    logger = Logger('main', Logger.INFO)
    logger.show(Logger.INFO, 'uPtt server', version.v)

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    socketio = SocketIO(app)

    socketio.on_namespace(EchoNamespace('/echo'))

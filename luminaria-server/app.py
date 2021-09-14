from flask import Flask, request, send_file
from flask_cors import CORS
from flask_socketio import SocketIO

from apps.app_manager import AppManager
from apps.gateway import Gateway
from common.logger import log
from common.messenger import Messenger
from database.config.global_config_model import GlobalConfigModel

app = Flask(__name__)
app.config['SECRET_KEY'] = GlobalConfigModel.retrieve('FLASK_SECRET_KEY')
socketio = SocketIO(app, cors_allowed_origins='*', cookie=False)
CORS(app)
gateway = Gateway(AppManager(), Messenger(socketio))
log('Flask', 'Deployed')


@app.route('/')
def main():
    return 'Luminarias Server'


@app.route('/<string:command>', methods=['POST'])
def raw(command):
    data = request.get_json()
    return gateway.raw(command, data)


@app.route('/<action>/<string:app_id>/<string:command>', methods=['POST'])
def enact(action, app_id, command):
    data = request.get_json()
    if action == 'blob':
        filename = gateway.blob(app_id, command, data)
        return send_file(filename, as_attachment=True)
    if action == 'query':
        return gateway.query(app_id, command, data)
    if action == 'status':
        return gateway.status(app_id, data)
    return gateway.execute(app_id, command, data)


if __name__ == '__main__':
    socketio.run(app)

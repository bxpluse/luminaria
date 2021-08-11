from flask import Flask, request, send_file
from flask_cors import CORS
from flask_socketio import SocketIO

from apps.app_manager import AppManager
from common.logger import log
from common.messenger import Messenger
from database.config.global_config_model import GlobalConfigModel

app = Flask(__name__)
app.config['SECRET_KEY'] = GlobalConfigModel.retrieve('FLASK_SECRET_KEY')
socketio = SocketIO(app, cors_allowed_origins="*", cookie=False)
CORS(app)
messenger = Messenger(socketio)
manager = AppManager()
log('Flask', 'Deployed')


@app.route('/')
def main():
    return 'Luminarias Server'


@app.route('/get-all-apps', methods=['POST'])
def get_all_apps():
    return manager.get_all_apps()


@app.route('/status/<string:app_id>', methods=['POST'])
def get_app_status(app_id):
    return manager.get_app_status(app_id)


@app.route('/blob/<string:app_id>/<string:command>', methods=['POST'])
def blob(app_id, command):
    data = request.get_json()
    return send_file(manager.blob(app_id, command, data), as_attachment=True)


@app.route('/get/<string:app_id>/<string:command>', methods=['GET'])
def get(app_id, command):
    return execute(app_id, command)


@app.route('/exec/<string:app_id>/<string:command>', methods=['POST'])
def post(app_id, command):
    data = request.get_json()
    return execute(app_id, command, data)


def execute(app_id, command, data=None):
    res = manager.execute(app_id, command, data)
    if not res:
        return {}
    if '<TOAST>' in res:
        messenger.toast(res['<TOAST>'])
        del res['<TOAST>']
    return res


if __name__ == '__main__':
    socketio.run(app)

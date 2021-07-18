from flask import Flask, request, send_file
from flask_cors import CORS
from flask_socketio import SocketIO

from apps.app_manager import AppManager
from common.logger import log
from common.messenger import Messenger

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
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


@app.route('/get/<string:app_id>/<string:command>', methods=['GET'])
def get(app_id, command):
    res = manager.get(app_id, command)
    if '<MESSAGE>' in res:
        messenger.toast(res['<MESSAGE>'])
    return res


@app.route('/blob/<string:app_id>/<string:command>', methods=['POST'])
def download_db(app_id, command):
    return send_file(manager.blob(app_id, command), as_attachment=True)


@app.route('/exec/<string:app_id>/<string:command>', methods=['POST'])
def execute(app_id, command):
    data = request.get_json()
    res = manager.execute(app_id, command, data)
    if not res:
        return {}
    if '<MESSAGE>' in res:
        messenger.toast(res['<MESSAGE>'])
    return res


if __name__ == '__main__':
    socketio.run(app)

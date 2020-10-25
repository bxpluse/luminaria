from flask import Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS
from apps.app_manager import AppManager
from common.logger import log
from common.messenger import Messenger

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", cookie=False)
CORS(app)
messenger = Messenger(socketio)
manager = AppManager(messenger=messenger)
log('Flask', 'Deployed')


@app.route('/')
def main():
    return 'Luminarias Server'


@app.route('/test', methods=['POST'])
def test():
    if request.method == 'POST':
        data = request.get_json()
        if data['order'] == 'fire':
            res = {'message': 'activating lasers ...'}
            return res


@app.route('/get-all-apps', methods=['POST'])
def get_all_apps():
    return manager.get_all_apps()


@app.route('/status/<string:app_id>', methods=['POST'])
def get_app_status(app_id):
    return {'status': manager.get_app_status(app_id)}


@app.route('/updater/exchanges/<string:exchange>', methods=['POST'])
@app.route('/updater/exchanges', methods=['POST'])
def get_all_exchanges(exchange=None):
    if exchange is None:
        return {'exchanges': manager.exchange_updater.EXCHANGES}
    else:
        manager.exchange_updater.run(exchange)
        messenger.toast(str(exchange) + " exchange has finished updating")
        return {}


@app.route('/log-viewer/<string:command>', methods=['POST'])
def exec_logviewer(command):
    data = request.get_json()
    num_lines = data['numLines']
    res = manager.log_viewer.run(lines=num_lines)
    return {'lines': res}


@app.route('/exec/<string:app_id>/<string:command>', methods=['POST'])
def execute(app_id, command):
    data = request.get_json()
    res = manager.execute(app_id, command, data)
    return res


if __name__ == '__main__':
    # app.run()
    socketio.run(app)

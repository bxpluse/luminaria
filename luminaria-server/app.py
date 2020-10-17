from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def main():
    return 'Luminaria Server'


@app.route('/test', methods=['POST'])
def test():
    if request.method == 'POST':
        data = request.get_json()
        if data['order'] == 'fire':
            res = {'message': 'activating lasers ...'}
            return res
    return {}


if __name__ == '__main__':
    app.run()

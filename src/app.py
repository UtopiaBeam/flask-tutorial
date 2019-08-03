import os
import pika
import json
from flask import Flask, request, jsonify
from rmq_client import RmqClient

app = Flask(__name__)
client = RmqClient()


@app.route('/ping', methods=['GET', 'POST'])
def ping():
    if request.method == 'GET':
        return jsonify({'message': 'pong'})
    return jsonify(request.get_json())


@app.route('/message/<id>', methods=['POST'])
def message(id):
    body = json.dumps({
        'pattern': {
            'cmd': 'get_sheet',
            'target': 'fhb'
        },
        'data': {
            'id': id
        }
    })
    try:
        return client.call(message=body)
    except:
        return '',500


if __name__ == "__main__":
    app.run(host=os.getenv('HOST'), port=80, debug=True)

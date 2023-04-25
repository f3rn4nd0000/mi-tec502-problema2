from flask import Flask, request, jsonify
import json

gas_station_ids = []
gas_station_queue_sizes = []
app  = Flask(__name__)

@app.route('/data', methods=['POST'])
def data() -> str:

    if request.method == 'POST':
        print(request)
        message = request.data.decode('utf-8')
        payload = {}
        payload['gas_station_id'] = json.loads(message)['gas_station_id']
        payload['queue_size'] = json.loads(message)['queue_size']

        print('payload')
        print(payload)
        print(payload['gas_station_id'])

        if len(gas_station_ids) == 0:
            gas_station_ids.append(payload['gas_station_id'])
            gas_station_queue_sizes.append(payload['queue_size'])
            
        try:
            correct_station_id = gas_station_ids.index(payload['gas_station_id'])
            gas_station_queue_sizes[correct_station_id] = payload['queue_size']
        except ValueError:
            gas_station_ids.append(payload['gas_station_id'])
            gas_station_queue_sizes.append(payload['queue_size'])

        return (gas_station_ids, gas_station_queue_sizes)
        
@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return jsonify({"postos": gas_station_ids, "tamanho_filas": gas_station_queue_sizes})

if __name__ == '__main__':
    app.run()
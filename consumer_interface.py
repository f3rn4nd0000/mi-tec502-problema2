from flask import Flask, request, jsonify, redirect, session, url_for
import json

gas_station_ids = []
gas_station_queue_sizes = []
app  = Flask(__name__)

@app.route('/data', methods=['POST'])
def data() -> str:

    if request.method == 'POST':
        print(request)
        # print(request.data)
        # print(type(request.data))
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
            # gas_station_queue_sizes[gas_station_queue_sizes.index(payload['queue_size'])] = payload['queue_size']
        except ValueError:
            gas_station_ids.append(payload['gas_station_id'])
            gas_station_queue_sizes.append(payload['queue_size'])

        # if payload['gas_station_id'] in gas_stations:
        # for station in gas_stations_ids:
        #     if station['gas_station_id'] == payload['gas_station_id']:
        #         station['queue_size'] = json.loads(message)['queue_size']    
            
        # if gas_stations.index(payload['gas_station_id']) is not None:
        #     gas_stations[gas_stations.index(payload['gas_station_id'])]['queue_size'] = json.loads(message)['queue_size']

        # return redirect(url_for('.index', messages = request.data.decode('utf-8')))
        return (gas_station_ids, gas_station_queue_sizes)
        
    # return jsonify(request.get_data())
    # data = json.dumps({"resposta": request.data.decode("utf-8")})
    # return f'Dados retornados do broker: {data.decode("utf-8")}'


@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        # data = session['messages']
        return jsonify({"postos": gas_station_ids, "tamanho_filas": gas_station_queue_sizes})

if __name__ == '__main__':
    app.run()
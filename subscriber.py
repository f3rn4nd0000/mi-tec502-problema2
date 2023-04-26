from paho.mqtt import client as mqtt_client
import random
import json
import requests

broker    = 'localhost'
port      = 1883
topic     = "fila/posto"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# cache armazenando todas as filas de todos os postos
gas_station_queues = []

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Conectado ao broker MQTT!")
        else:
            print("Erro na conexão, código %d\n", rc)
    # Configura o ID do cliente(subscriber)
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
    
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(str(msg))
        data = str(msg.payload.decode("utf-8"))
        print(f"`{data}` recebida do topico `{msg.topic}`")
        requests.post('http://localhost:5000/data', data = msg.payload)
        # print(f"`{msg.payload.decode()}` Recebida do tópico `{msg.topic}`")
        manage_subscriptions(msg=msg)
    client.subscribe(topic)
    client.on_message = on_message

def manage_subscriptions(msg):
    received_msg = json.loads(msg.payload.decode('utf-8'))
    print('received_msg')
    print(received_msg)
    gas_station_info = {}
    gas_station_info['gas_station_id'] = received_msg['gas_station_id']
    gas_station_info['queue_size']     = received_msg['queue_size']

    for station in gas_station_queues:
        if gas_station_info['gas_station_id'] in station['gas_station_id']:
            print('A')
            station['queue_size'] = gas_station_info['queue_size']
        else:
            print('B')
            gas_station_queues.append(gas_station_info)
            
def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == "__main__":
    run()
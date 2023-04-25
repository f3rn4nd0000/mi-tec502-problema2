from paho.mqtt import client as mqtt_client
import random
import time
from gas_station import GasStation

broker = 'localhost'
port = 1883
topic = "fila/posto"
client_id = f'{random.randint(0, 1000)}' # Equivalente ao número do posto

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Conectado ao Broker MQTT!")
        else:
            print("Falha ao conectar, código de erro: %d\n", rc)
    # Configura o ID do publisher
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
    gas_station = GasStation()
    
    while True:
        time.sleep(5)
        # msg = f" Tamanho da fila do posto {client_id}: {gas_station.queue_size}"
        msg = gas_station.to_json()
        print('msg')
        print(msg)
        print(type(msg))
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Enviando `{msg}` ao tópico `{topic}`")
        else:
            print(f"Falha ao enviar mensagem ao tópico {topic}")
        gas_station.increase_queue()

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

if __name__ == '__main__':
    run()

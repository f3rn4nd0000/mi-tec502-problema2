from paho.mqtt import client as mqtt_client
import random
import time
import threading
import json
import uuid

broker = 'localhost'
port = 1883
topic = "fila/posto"
client_id = f'{random.randint(0, 1000)}' # Equivalente ao número do posto
MAX_THREADS = 15

threads = []
result = []

DISCHARGE_TENDENCY = {
    "0": "rapida",
    "1": "media",
    "2": "lenta"
}

class Vehicle():

    def __init__(self) -> None:
        self.discharge_tendency = random.randint(0,3)
        self.fuel_level = 100
    
    def reduce_fuel_level(self):
        self.fuel_level -= 1*self.discharge_tendency

    def increase_fuel_level(self):
        self.fuel_level += 1*self.discharge_tendency

    def move_around(self):
        self.reduce_fuel_level()

    def refuel(self):
        self.increase_fuel_level()

    def to_json(self):
        return json.dumps({
            "discharge_tendency": DISCHARGE_TENDENCY.get[self.discharge_tendency],
            "fuel_level": self.move_around()
        })

class GasStation():
    
    def __init__(self) -> None:
        self.id = str(uuid.uuid1())
        self.queue_size = 0

    def reduce_queue(self):
        self.queue_size -= 1

    def increase_queue(self):
        self.queue_size += 1
    
    def to_json(self):
        return json.dumps({
            "gas_station_id": self.id,
            "queue_size": self.queue_size
        })

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

def main():
    for _ in range(MAX_THREADS):
        thr = threading.Thread(target=run)
        threads.append(thr)
        thr.setDaemon(True)
        thr.start()
    
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    run()

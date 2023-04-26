from paho.mqtt import client as mqtt_client
import random
import time
# from gas_station import GasStation

"""
Exemplos de topico: 
    "fila/posto" fila de cada posto de gasolina
    "carros/fila" numero de carros se dirigindo ao posto para reabastecer
"""

class Publisher():

    def __init__(self, topic) -> None:
       self.broker = "localhost"
       self.port = 1883
       self.topic = topic
       self.client_id = f'{random.randint(0, 1000)}' # Equivalente ao número do posto

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Conectado ao Broker MQTT!")
            else:
                print("Falha ao conectar, código de erro: %d\n", rc)
        # Configura o ID do publisher
        client = mqtt_client.Client(self.client_id)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def publish(self, client, message):
        # new_gas_station = GasStation()
        while True:
            time.sleep(2)
            # msg = f" Tamanho da fila do posto {client_id}: {gas_station.queue_size}"
            print('message')
            print(message)
            print(type(message))
            result = client.publish(self.topic, message)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Enviando `{message}` ao tópico `{self.topic}`")
            else:
                print(f"Falha ao enviar mensagem ao tópico {self.topic}")
            # gas_station.increase_queue()

    def run(self, message):
        client = self.connect_mqtt()
        client.loop_start()
        self.publish(client, message)

# if __name__ == '__main__':
#     publisher = Publisher()
#     publisher.run()

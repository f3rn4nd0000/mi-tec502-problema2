from paho.mqtt import client as mqtt_client
from multiprocessing import Process
from threading import Thread, Lock
import random
import requests

class Subscriber():
   
    def __init__(self, topic) -> None:
        self.broker    = 'localhost'
        self.port      = 1883
        self.topic     = topic
        self.client_id = f'python-mqtt-{random.randint(0, 1000)}'
        self.gas_station_queues = [] # cache armazenando todas as filas de todos os postos

    def connect_mqtt(self) -> mqtt_client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Conectado ao broker MQTT!")
            else:
                print("Erro na conexão, código %d\n", rc)
        # Configura o ID do cliente(subscriber)
        client = mqtt_client.Client(self.client_id)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client
        
    def subscribe(self, client: mqtt_client):
        def on_message(client, userdata, msg):
            # print(str(msg))
            data = str(msg.payload.decode("utf-8"))
            print(f"`{data}` recebida do topico `{msg.topic}`")
            return data
            # print(f"`{msg.payload.decode()}` Recebida do tópico `{msg.topic}`")
            # self.manage_subscriptions(msg=msg)
        client.subscribe(self.topic)
        client.on_message = on_message
        
    # def manage_subscriptions(self, msg):
    #     received_msg = json.loads(msg.payload.decode('utf-8'))
    #     print('received_msg')
    #     print(received_msg)
    #     gas_station_info = {}
    #     gas_station_info['gas_station_id'] = received_msg['gas_station_id']
    #     gas_station_info['queue_size']     = received_msg['queue_size']

    #     new_gas_station = GasStation()
    #     new_gas_station.set_id(gas_station_info['gas_station_id'])
    #     new_gas_station.set_queue_size(gas_station_info['queue_size'])

    #     for station in self.gas_station_queues:
    #         if gas_station_info['gas_station_id'] in station['gas_station_id']:
    #             print('A')
    #             station['queue_size'] = gas_station_info['queue_size']
    #         else:
    #             print('B')
    #             self.gas_station_queues.append(gas_station_info)
                
    def run(self):
        client_subscriber = self.connect_mqtt()
        self.subscribe(client_subscriber)
        client_subscriber.loop_forever()
            

if __name__ == "__main__":
    thread_gas_station = Thread(target = Subscriber("fila/posto").run).start()
    thread_vehicle     = Thread(target = Subscriber("carros/fila").run).start()

    # thread_gas_station.start()
    # thread_vehicle.start()
    
    # thread_gas_station.join()
    # thread_vehicle.join()

    # while True:
    #     thread_gas_station.run()
    #     thread_vehicle.run()

    #     thread_gas_station.join()
    #     thread_vehicle.join()
    

    # vehicle_subscriber     = Subscriber("carros/fila").run()
    # gas_station_subscriber = Subscriber("fila/posto").run()

    # thread_vehicle.start()
    # thread_gas_station.start()

    # thread_vehicle.join()
    # thread_gas_station.join()

    #     thread_vehicle.join()
    #     thread_gas_station.join()



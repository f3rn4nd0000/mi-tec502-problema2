from paho.mqtt import client as mqtt_client
import random
import time

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
    gas_sation_number = 0
    while True:
        time.sleep(5)
        msg = f"mensagem: {client_id}, Tamanho da fila do posto {client_id} = {gas_sation_number}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Enviando `{msg}` ao tópico `{topic}`")
        else:
            print(f"Falha ao enviar mensagem ao tópico {topic}")
        gas_sation_number += 1

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()

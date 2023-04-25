import random
import time
import threading
import json
import uuid
import sys
import requests

DISCHARGE_TENDENCY = {
    "0": "lenta",
    "1": "media",
    "2": "rapida"
}

class Vehicle():

    def __init__(self) -> None:
        self.vehicle_id = uuid.uuid1()
        self.discharge_tendency = random.randint(0,3)
        self.fuel_level = 100
        print(f'tendencia de descarregamento: {self.discharge_tendency}')

    def reduce_fuel_level(self):
        self.fuel_level -= 1*(self.discharge_tendency + 1)
        print(f'nivel de combustivel: {self.fuel_level}')
    
    def increase_fuel_level(self):
        self.fuel_level += 1*(self.discharge_tendency + 1)

    def move_around(self):
        self.reduce_fuel_level()
        if self.fuel_level <= 80 and self.fuel_level > 0:
            print('Atenção, nivel de combustivel muito baixo, por favor se dirija a um posto')
            lista_postos = json.loads(requests.get('http://127.0.0.1:5000/').content.decode('utf-8'))
            print('lista_postos')
            print(lista_postos)
            print('Veja abaixo uma lista de 5 postos com a menor fila:\n')
            print(45*'_')
            for i in range(0,len(lista_postos['postos'])):
                print(f"|{lista_postos['postos'][i]}: {lista_postos['tamanho_filas'][i]}   |")
            print(45*'-')
        elif self.fuel_level <= 0:
            print('Veiculo sem combustivel, por favor chame um guincho!')
            sys.exit()


    def refuel(self):
        self.increase_fuel_level()

    def to_json(self):
        return json.dumps({
            "discharge_tendency": DISCHARGE_TENDENCY.get[self.discharge_tendency],
            "fuel_level": self.move_around()
        })


if __name__ == '__main__':
    new_car = Vehicle()
    while True:
        time.sleep(.1)
        new_car.move_around()
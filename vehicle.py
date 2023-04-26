import random
import time
import threading
import json
import uuid
import sys
import requests
from gas_station import GasStation
from publisher import Publisher

REFUEL_TIME = 60
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
                better_gas_station_id    = lista_postos['postos'][0]
                better_gas_station_queue = lista_postos['tamanho_filas'][0]
            self.refuel(better_gas_station_id, better_gas_station_queue)
            print(45*'-')
        elif self.fuel_level <= 0:
            print('Veiculo sem combustivel, por favor chame um guincho!')
            sys.exit()

    def refuel(self, gas_station_id, gas_station_queue):
        # better_station_id = gas
        # better_station_id = GasStation.get_station_by_id(id = gas_station_id)
        gas_station_object = GasStation()
        gas_station_object.set_id(gas_station_id)
        gas_station_object.set_queue_size(gas_station_queue)
        
        print('gas_station_id')
        print(gas_station_id)

        if gas_station_object.get_station_id() == gas_station_id:
            gas_station_object.increase_queue()

            while self.fuel_level < 100:
                print('reabastecendo veiculo')
                print(self.fuel_level)
                self.increase_fuel_level()
            time.sleep(REFUEL_TIME)
            gas_station_object.reduce_queue()

    def to_json(self):
        return json.dumps({
            "vehicle_id": self.vehicle_id,
            "discharge_tendency": DISCHARGE_TENDENCY.get[self.discharge_tendency],
            "fuel_level": self.move_around()
        })


if __name__ == '__main__':
    new_car = Vehicle()
    while True:
        time.sleep(.1)
        new_car.move_around()
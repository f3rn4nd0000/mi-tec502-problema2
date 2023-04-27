import random
import time
import json
import uuid
import sys
import requests
from gas_station import GasStation
from publisher import Publisher
from threading import Thread

REFUEL_TIME = 60
DISCHARGE_TENDENCY = {
    "1": "lenta",
    "2": "media",
    "3": "rapida"
}

class Vehicle():

    def __init__(self) -> None:
        self.vehicle_id = uuid.uuid1()
        self.discharge_tendency = random.randint(1,3)
        self.fuel_level = 100
        self.publisher = Publisher("carros/fila")
        print(f'tendencia de descarregamento: {self.discharge_tendency}')
    
    def reduce_fuel_level(self):
        self.fuel_level -= 1*(self.discharge_tendency)
        print(f'nivel de combustivel: {self.fuel_level}')
    
    def increase_fuel_level(self):
        self.fuel_level += 1*(self.discharge_tendency)

    def to_json(self):
        return json.dumps({
            "vehicle_id": str(self.vehicle_id),
            "discharge_tendency": DISCHARGE_TENDENCY[str(self.discharge_tendency)],
            "fuel_level": self.fuel_level
        })

    def move_around(self):
        self.reduce_fuel_level()
        if self.fuel_level <= 80 and self.fuel_level > 0:
            print('Atenção, nivel de combustivel muito baixo, por favor se dirija a um posto')
            lista_postos = json.loads(requests.get('http://127.0.0.1:5000/').content.decode('utf-8'))
            
            print('lista_postos')
            print(lista_postos)

            self.moving_to_station = True
            self.station_id.join(str(lista_postos['postos'][0]))

            self.go_to_station()

        elif self.fuel_level <= 0:
            print('Veiculo sem combustivel, por favor chame um guincho!')
            sys.exit()

    def refuel(self, gas_station_id, gas_station_queue):
        # better_station_id = gas
        # better_station_id = GasStation.get_station_by_id(id = gas_station_id)
        gas_station_object = GasStation().get_station_by_id(gas_station_id)
        # gas_station_object.set_id(gas_station_id)
        # gas_station_object.set_queue_size(gas_station_queue)

        """ EH GERADO UM OBJETO None """  
        print('gas_station_id')
        print(gas_station_object)
        print(gas_station_object.id)

        if gas_station_object.get_station_id() == gas_station_id:
            gas_station_object.increase_queue()

            while self.fuel_level < 100:
                print('reabastecendo veiculo')
                print(self.fuel_level)
                self.increase_fuel_level()
            time.sleep(REFUEL_TIME)
            gas_station_object.reduce_queue()

    def go_to_station(self):
        vehicle_publisher = self.publisher.connect_mqtt()
        # vehicle_publisher.loop_start()
        message = self.to_json()
        # if self.queue_size != self.to_json()["queue_size"]:
        self.publisher.publish(vehicle_publisher, message)

if __name__ == '__main__':
    new_car = Vehicle()
    while True:
        thread_move_around = Thread(target = new_car.move_around).run()
    # thread_go_to_station = Thread(target = new_car.go_to_station).run()    
        # new_car.go_to_station()
        # new_car.move_around()

from subscriber import Subscriber
from publisher import Publisher
from gas_station import GasStation
from vehicle import Vehicle
from threading import Thread
import json


class Fog():

    def __init__(self) -> None:
        self.gas_stations   = []
        self.vehicles       = [] 

    # def manage_gas_stations_and_vehicles(self):

    # def manage_gas_stations(self):
    # def manage_gas_stations(self, gas_stations:list):
    #     for station in gas_stations:
    #         if 

if __name__ == "__main__":
    thread_gas_station = Thread(target = Subscriber("fila/posto").run).start()
    thread_vehicle     = Thread(target = Subscriber("carros/fila").run).start()

    

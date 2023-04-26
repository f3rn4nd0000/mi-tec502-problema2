from subscriber import Subscriber
from publisher import Publisher
from gas_station import GasStation
from vehicle import Vehicle
import json


class Fog():

    def __init__(self) -> None:
        self.subscriber   = Subscriber()
        self.publisher    = Publisher()
        self.gas_stations = []
        self.vehicles     = [] 

from publisher import Publisher
from subscriber import Subscriber
import json
import uuid

class GasStation():
    
    def __init__(self) -> None:
        self.id              = uuid.uuid1()        
        self.queue_size      = 0
        self.vehicle_fueling = None
        self.publisher       = Publisher("fila/posto")
        self.subscriber      = Subscriber("carros/fila")

    def reduce_queue(self):
        self.queue_size -= 1
    
    def increase_queue(self):
        self.queue_size += 1
    
    # A IDEIA EH PODER ACESSAR OS DADOS DE CADA INSTANCIA
    def get_station_by_id(self, id):
        if self.id == id:
            return self

    def set_queue_size(self, new_queue_size):
        self.queue_size = new_queue_size

    def set_id(self, station_id):
        self.id = station_id

    def get_queue_size(self):
        return self.queue_size
    
    def get_station_id(self):
        return self.id
    
    def to_json(self):
        return json.dumps({
            "gas_station_id": str(self.id),
            "queue_size": self.queue_size
        })
    
    def main(self):
        client_publisher = self.publisher.connect_mqtt()
        client_publisher.loop_start()
        message = self.to_json()
        # if self.queue_size != self.to_json()["queue_size"]:
        self.publisher.publish(client_publisher, message)
            

if __name__ == "__main__":
    new_gas_station = GasStation()
    new_gas_station.main()
    
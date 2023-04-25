import json
import uuid


class GasStation():
    
    def __init__(self) -> None:
        self.id = str(uuid.uuid1())
        self.queue_size = 0

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
            "gas_station_id": self.id,
            "queue_size": self.queue_size
        })
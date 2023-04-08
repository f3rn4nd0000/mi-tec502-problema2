import publisher

class Publisher():

    def __init__(self) -> None:
        self.publisher = publisher.connect_mqtt()

class Posto():

    def __init__(self) -> None:
        self.fila = 0
        self.publisher = publisher

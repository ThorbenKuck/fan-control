import yaml


class MqttProperties:
    topic: str
    username: str
    password: str
    client_id: str
    broker: str

    def __init__(self, path: str):
        self.path = path
        self.read_variables()

    def read_variables(self):
        with open(self.path, "r") as stream:
            content = yaml.full_load(stream)
            properties = content["mqtt"]
            debug_enabled = bool(content["debug"])
            if debug_enabled:
                print("[DEBUG]: active")

            self.topic = properties["topic"]
            self.username = properties["username"]
            self.password = properties["password"]
            self.client_id = properties["client_id"]
            self.broker = properties["broker"]

import yaml


class ClientProperties:
    name: str
    temperature_file_path: str
    timeout: float
    debug_enabled: bool

    def __init__(self, file):
        self.path = file
        self.read_variables()

    def read_variables(self):
        with open(self.path, "r") as stream:
            content = yaml.full_load(stream)
            properties = content["client"]
            self.name = properties["name"]
            self.temperature_file_path = properties["path"]
            self.timeout = float(properties["timeout"])
            if content["debug"]:
                self.debug_enabled = True
            else:
                self.debug_enabled = False

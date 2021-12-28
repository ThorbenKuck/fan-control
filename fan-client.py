from time import sleep

import paho.mqtt.client as mqtt
from threading import Thread

from ClientProperties import ClientProperties
from MqttProperties import MqttProperties


client_props: ClientProperties = ClientProperties("fan-control.yaml")
mqtt_props: MqttProperties = MqttProperties("fan-control.yaml")
mqtt_props.topic = mqtt_props.topic.replace("+", client_props.name)
mqtt_props.client_id = mqtt_props.client_id + "-client"
debug_enabled = client_props.debug_enabled


def read_temps(path: str):
    with open(path, 'r') as f:
        lines = f.readlines()
        return int(lines[0])


def debug(*args, sep=' ', end='\n'):
    if debug_enabled:
        prefix: str
        if sep != ' ':
            prefix = "[DEBUG]: "
        else:
            prefix = "[DEBUG]:"

        print(
            prefix,
            *args,
            end=end,
            sep=sep
        )


print("creating new instance", "\"" + mqtt_props.client_id + "\"")
client = mqtt.Client(mqtt_props.client_id)
client.username_pw_set(
    username=mqtt_props.username,
    password=mqtt_props.password
)
debug("Connecting with username=", mqtt_props.username, ", password=", mqtt_props.password, sep="")
print("connecting to broker", "\"" + mqtt_props.broker + "\"", "... ", end='')
client.connect(mqtt_props.broker)
print("[OK]")


class FileModifiedHandler:

    def __init__(self, path):
        self.path = path
        self.last_known_temp = -1

        print("Starting the observer on \"" + path + "\" ... ", end="")
        self.observer = Thread(target=self.process_temps, daemon=True)
        self.observer.start()
        print("[OK]")
        print("Ready to use!")
        self.observer.join()
        print("Finished!")

    def process_temps(self):
        while True:
            sleep(client_props.timeout)
            with open(client_props.temperature_file_path) as f:
                temperature = int(f.readlines()[0].strip())
                if temperature != self.last_known_temp:
                    print("Publishing new temperature", temperature, "to topic", mqtt_props.topic, "... ", end="")
                    client.publish(
                        topic=mqtt_props.topic,
                        payload=temperature
                    ).wait_for_publish()
                    print("[OK]")
                    self.last_known_temp = temperature
                else:
                    debug("No temperature change detected")
            client_props.read_variables()


if __name__ == '__main__':
    FileModifiedHandler(client_props.temperature_file_path)

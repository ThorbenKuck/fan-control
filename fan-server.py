import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import threading

from types.MqttProperties import MqttProperties
from types.ServerProperties import ServerProperties

GPIO.setmode(GPIO.BCM)
settings_path = "/usr/local/etc/fan-control/settings.yaml"

mqtt_properties: MqttProperties = MqttProperties(settings_path)
server_properties = ServerProperties(settings_path)
mqtt_properties.client_id = mqtt_properties.client_id + "-server"


def kill_all():
    for fan in server_properties.all_fans:
        fan.stop()
        fan.release()
    GPIO.cleanup()


semaphore = threading.Semaphore(0)


def parse_temperature(message: str):
    try:
        return int(message)
    except:
        temperature = str("{:.2f}".format(float(message))).replace(".", "")
        return int(temperature + "0")


def on_message(client, userdata, message):
    try:
        server_properties.update_variables()
        rack_target = message.topic.replace("rack/", '').replace("/temp", '')

        temp = parse_temperature(message.payload.decode("utf-8"))
        print("received temps from " + rack_target, temp)

        fans_to_trigger = []
        for key, value in server_properties.all_fans.items():
            if rack_target.startswith(key):
                fans_to_trigger.append(value)
        if not fans_to_trigger:
            print("Unknown rack-target", rack_target)
        else:
            for fan in fans_to_trigger:
                fan.trigger(temp, server_properties.debug_enabled, rack_target)
    except Exception as e:
        print("Illegal message on topic " + message.topic, message.payload.decode("utf-8"))
        print(e)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK Returned code=", rc)
    else:
        print("Bad connection Returned code=", rc)


def release_waiting():
    print("Releasing semaphore")
    semaphore.release()


def main():
    print("creating new client instance", mqtt_properties.client_id)
    client = mqtt.Client(mqtt_properties.client_id)
    while True:
        try:
            client.on_connect = on_connect
            client.on_message = on_message
            client.on_disconnect = release_waiting
            client.on_connect_fail = release_waiting

            print("connecting to broker")
            client.username_pw_set(
                username=mqtt_properties.username,
                password=mqtt_properties.password
            )
            client.connect(mqtt_properties.broker)
            client.loop_start()
            print("Subscribing to topic", mqtt_properties.topic)
            client.subscribe(mqtt_properties.topic)
            semaphore.acquire()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
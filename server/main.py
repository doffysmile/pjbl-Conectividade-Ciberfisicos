import os
import json
import paho.mqtt.client as mqtt

from database import (
    initialize,
    save_measurement
)

initialize()

def on_connect(client, userdata, flags, reason_code, properties):
    print("Servidor conectado ao MQTT")
    client.subscribe("pjbl/+/environment")

def on_message(client, userdata, message):
    room = message.topic.split("/")[1]
    data = json.loads(message.payload.decode())

    print(f"\nSala: {room}")
    print("Temperatura:", data["temperature"])
    print("Ocupação:", data["occupancy"])
    save_measurement(room, data)

client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    client_id="smartspace_server"
)

client.on_connect = on_connect
client.on_message = on_message

host = os.getenv("MQTT_HOST", "localhost")
client.connect(host, 1883, 60)
client.loop_forever()

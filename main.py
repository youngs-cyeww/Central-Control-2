# main.py
import json
import paho.mqtt.client as mqtt

from config import MQTT_BROKER, MQTT_PORT
from database import update_vehicle, get_other_vehicles, get_vehicle_task
from path_planner import a_star, build_obstacle_map, should_yield

def on_connect(client, userdata, flags, rc):
    print("MQTT connected")
    client.subscribe("vehicle/+/status")

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    car_id = int(msg.topic.split("/")[1].replace("car", ""))

    x = data["x"]
    y = data["y"]

    update_vehicle(car_id, x, y, data["battery"], data["status"])

    others = get_other_vehicles(car_id)

    if should_yield(car_id, (x, y), others):
        send_cmd(car_id, x, y)
        return

    task = get_vehicle_task(car_id)
    if not task:
        send_cmd(car_id, x, y)
        return

    goal = (task["target_x"], task["target_y"])
    obstacles = build_obstacle_map(others)
    path = a_star((x, y), goal, obstacles)

    if not path or len(path) < 2:
        send_cmd(car_id, x, y)
    else:
        nx, ny = path[1]
        send_cmd(car_id, nx, ny)

def send_cmd(car_id, x, y):
    topic = f"vehicle/car{car_id}/cmd"
    payload = json.dumps({"next_x": x, "next_y": y})
    client.publish(topic, payload, qos=1)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT)
client.loop_forever()

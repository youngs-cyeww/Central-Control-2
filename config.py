# config.py

# MQTT
MQTT_BROKER = "localhost"
MQTT_PORT = 1883

# MySQL
MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "12345678",
    "database": "logistics"
}

# Map
MAP_WIDTH = 20
MAP_HEIGHT = 20

STATIC_OBSTACLES = [
    (5, 5), (5, 6), (5, 7)
]

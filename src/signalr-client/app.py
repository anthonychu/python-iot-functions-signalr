import random
from collections import deque
from time import sleep, time
from terminalplot import plot, get_terminal_size
from signalrcore.hub_connection_builder import HubConnectionBuilder

device_readings = deque(maxlen=60)
count = 0
def process_device_message(msg):
    global device_readings, count
    temperature = msg[0]["temperature"]
    device_readings.append((count, temperature))
    count += 1
    h, w = get_terminal_size()
    x, y = zip(*device_readings)
    plot(x, y, h+1, w)

connection = HubConnectionBuilder() \
    .with_url('http://localhost:7071/api') \
    .build()
connection.on('newDeviceMessage', process_device_message)
connection.start()

input("Receiving chat messages...")

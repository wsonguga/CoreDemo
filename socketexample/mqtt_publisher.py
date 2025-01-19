import paho.mqtt.client as mqtt
import time
import random
import json
import matplotlib.pyplot as plt

# MQTT Broker Settings
BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "sensor/data"

# Initialize Matplotlib figure
plt.ion()
fig, ax = plt.subplots()
x_data, y_data = [], []

def publish_data(client):
    counter = 0
    while True:
        sensor_value = round(random.uniform(20.0, 30.0), 2)  # Simulated temperature data
        timestamp = time.time()
        data = {"timestamp": timestamp, "value": sensor_value}

        # Publish to MQTT broker
        client.publish(TOPIC, json.dumps(data))
        print(f"Published: {data}")

        # Update plot
        x_data.append(counter)
        y_data.append(sensor_value)
        counter += 1

        ax.clear()
        ax.plot(x_data, y_data, marker='o', linestyle='-')
        ax.set_xlabel("Time")
        ax.set_ylabel("Temperature (°C)")
        ax.set_title("Published Sensor Data Stream")
        plt.pause(0.5)  # Refresh every 0.5 seconds

        time.sleep(1)

if __name__ == "__main__":
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)
    publish_data(client)

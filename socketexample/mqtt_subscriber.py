import paho.mqtt.client as mqtt
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
counter = 0

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    global counter
    data = json.loads(msg.payload.decode())
    print(f"Received: {data}")

    # Update plot
    x_data.append(counter)
    y_data.append(data["value"])
    counter += 1

    ax.clear()
    ax.plot(x_data, y_data, marker='o', linestyle='-')
    ax.set_xlabel("Time")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Received Sensor Data Stream")
    plt.pause(0.5)  # Refresh every 0.5 seconds

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.loop_forever()

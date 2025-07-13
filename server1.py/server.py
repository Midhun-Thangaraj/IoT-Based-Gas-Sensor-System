import paho.mqtt.client as mqtt
from flask import Flask, jsonify, request

app = Flask(__name__)

# MQTT settings
MQTT_BROKER = "localhost"  # Use your broker IP if not local
MQTT_PORT = 1883
MQTT_TOPIC = "sensor/data"

# Initialize MQTT Client
mqtt_client = mqtt.Client()

# Callback function when a message is received
def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")
    # Process the message here (e.g., store it, send notifications, etc.)

# Set up the MQTT client
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.subscribe(MQTT_TOPIC, qos=0)

# Start MQTT loop in the background
mqtt_client.loop_start()

# Route to handle GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # This handles GET requests and returns a message
        return jsonify({"message": "Python MQTT server is running!"})
    
    elif request.method == 'POST':
        # This handles POST requests (you can add your logic here)
        data = request.get_json()
        if data:
            print(f"Received POST data: {data}")
            return jsonify({"message": "POST request received", "data": data}), 200
        else:
            return jsonify({"message": "No JSON data received"}), 400

# Run Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Run Flask server

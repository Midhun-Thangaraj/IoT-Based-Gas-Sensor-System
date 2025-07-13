import http.server
import socketserver
import mysql.connector
from urllib.parse import urlparse, parse_qs

# Server port
PORT = 5000  

# MySQL Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "mahesh@1",
    "database": "gas_detection"
}

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        # Store sensor data in the database
        if "gas_value" in query_params:
            gas_value = query_params["gas_value"][0]
            self.store_data_in_db(gas_value)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Data stored successfully")

        # Fetch last 10 sensor values from the database
        elif self.path == "/get_data":
            data = self.fetch_sensor_data()
            self.send_response(200)
            self.end_headers()
            response = "\n".join([f"Sensor Value: {value}, Timestamp: {timestamp}" for value, timestamp in data])
            self.wfile.write(response.encode())

        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid Request")

    def store_data_in_db(self, gas_value):
        """Stores gas sensor value into the database."""
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sensor_data (sensor_value, timestamp) VALUES (%s, NOW())", (gas_value,))
        conn.commit()
        cursor.close()
        conn.close()

    def fetch_sensor_data(self):
        """Fetches the last 10 sensor readings from the database."""
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT sensor_value, timestamp FROM sensor_data ORDER BY timestamp DESC LIMIT 10")
        data = cursor.fetchall()
        conn.close()
        return data

# Start the HTTP server
with socketserver.TCPServer(("", PORT), MyRequestHandler) as httpd:
    print(f"Server started at port {PORT}")
    httpd.serve_forever()

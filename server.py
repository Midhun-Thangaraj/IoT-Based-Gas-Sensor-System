from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mahesh@1",
    database="gas_detection"
)
cursor = db.cursor()

# Create table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS sensor_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        gas_type VARCHAR(50),
        lpg_ppm FLOAT DEFAULT 0,
        methane_ppm FLOAT DEFAULT 0,
        hydrogen_ppm FLOAT DEFAULT 0,
        co_ppm FLOAT DEFAULT 0,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
db.commit()

# Route to Receive Data from ESP8266
@app.route('/upload', methods=['POST'])
def upload_data():
    data = request.json
    gas_type = data.get("gas_type", "No gas detected")
    lpg = data.get("lpg_ppm", 0)
    methane = data.get("methane_ppm", 0)
    hydrogen = data.get("hydrogen_ppm", 0)
    co = data.get("co_ppm", 0)

    # Insert into database
    sql = "INSERT INTO sensor_data (gas_type, lpg_ppm, methane_ppm, hydrogen_ppm, co_ppm) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (gas_type, lpg, methane, hydrogen, co))
    db.commit()

    return jsonify({"status": "success", "message": "Data received"}), 200

# Route to Fetch Latest Sensor Data
@app.route('/latest', methods=['GET'])
def latest_data():
    cursor.execute("SELECT * FROM sensor_data ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()

    if row:
        data = {
            "id": row[0],
            "gas_type": row[1],
            "lpg_ppm": row[2],
            "methane_ppm": row[3],
            "hydrogen_ppm": row[4],
            "co_ppm": row[5],
            "timestamp": str(row[6])
        }
        return jsonify(data), 200
    else:
        return jsonify({"error": "No data found"}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

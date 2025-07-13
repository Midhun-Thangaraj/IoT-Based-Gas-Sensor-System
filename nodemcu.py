# import network
# import urequests
# import machine
# import time

# # WiFi Credentials
# SSID = "YOUR_WIFI_SSID"
# PASSWORD = "YOUR_WIFI_PASSWORD"

# # Blynk Credentials
# BLYNK_AUTH = "H2WXu8uQSIZOu2A6x2vO5fNaomTHB3HS"
# BLYNK_URL = "http://blynk.cloud/external/api/update"

# # Flask Server URL (for AI-based predictions)
# SERVER_URL = "http://192.168.43.51:5000/predict"

# # Setup WiFi Connection
# wifi = network.WLAN(network.STA_IF)
# wifi.active(True)
# wifi.connect(SSID, PASSWORD)

# while not wifi.isconnected():
#     time.sleep(1)
# print("Connected to WiFi!")

# # Setup Sensors and Components
# mq2 = machine.ADC(0)    # MQ-2 Sensor (Butane, Methane)
# mq7 = machine.ADC(0)    # MQ-7 Sensor (Carbon Monoxide)
# mq135 = machine.ADC(0)  # MQ-135 Sensor (Air Quality)
# buzzer = machine.Pin(5, machine.Pin.OUT)  # Buzzer (D1 - GPIO5)
# green_led = machine.Pin(4, machine.Pin.OUT)  # Green LED (D2 - GPIO4)
# red_led = machine.Pin(0, machine.Pin.OUT)  # Red LED (D3 - GPIO0)

# # Threshold values (Adjust based on calibration)
# MQ2_THRESHOLD = 400
# MQ7_THRESHOLD = 500
# MQ135_THRESHOLD = 450

# def send_blynk_alert(sensor_name, message):
#     """Send notification and email alert through Blynk"""
#     try:
#         # Send push notification
#         urequests.get(f"{BLYNK_URL}?token={BLYNK_AUTH}&V10={message}")
#         print(f"Blynk Notification Sent: {sensor_name} Alert")
        
#         # Send email alert
#         urequests.get(f"{BLYNK_URL}?token={BLYNK_AUTH}&email=your_email@example.com&subject={sensor_name} Alert&body={message}")
#         print(f"Email Alert Sent: {sensor_name}")
#     except Exception as e:
#         print("Blynk Error:", e)

# def alert_system():
#     """Blink buzzer for warning"""
#     for _ in range(3):
#         buzzer.on()
#         time.sleep(0.5)
#         buzzer.off()
#         time.sleep(0.5)

# while True:
#     # Read sensor values
#     mq2_value = mq2.read()
#     mq7_value = mq7.read()
#     mq135_value = mq135.read()
    
#     print(f"MQ2: {mq2_value}, MQ7: {mq7_value}, MQ135: {mq135_value}")

#     danger_detected = False

#     # Check MQ2 (Butane, Methane)
#     if mq2_value > MQ2_THRESHOLD:
#         send_blynk_alert("Butane/Methane", "⚠ High Butane/Methane detected!")
#         danger_detected = True

#     # Check MQ7 (Carbon Monoxide)
#     if mq7_value > MQ7_THRESHOLD:
#         send_blynk_alert("Carbon Monoxide", "⚠ High Carbon Monoxide detected!")
#         danger_detected = True

#     # Check MQ135 (Air Quality)
#     if mq135_value > MQ135_THRESHOLD:
#         send_blynk_alert("Air Quality", "⚠ Poor Air Quality detected!")
#         danger_detected = True
    
#     if danger_detected:
#         red_led.on()
#         green_led.off()
#         alert_system()
#     else:
#         red_led.off()
#         green_led.on()
#         buzzer.off()

#     # Send Data to Flask Server for AI Prediction
#     data = {"mq2": mq2_value, "mq7": mq7_value, "mq135": mq135_value}
    
#     try:
#         response = urequests.post(SERVER_URL, json=data)
#         result = response.json()
#         print("Server Response:", result)

#         if result["danger"]:  # AI Model says danger detected
#             red_led.on()
#             green_led.off()
#             alert_system()
#         else:
#             red_led.off()
#             green_led.on()
#             buzzer.off()
    
#     except Exception as e:
#         print("Flask Server Error:", e)

#     time.sleep(5)  # Wait 5 seconds before the next reading

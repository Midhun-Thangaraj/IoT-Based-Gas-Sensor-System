#define BLYNK_TEMPLATE_ID "TMPL3XjQb11fo"
#define BLYNK_TEMPLATE_NAME "AI Gas Detection"
#define BLYNK_AUTH_TOKEN "SO0by6yMrZ-An3UHbVu-5ZiT35rhXG8v"

#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <BlynkSimpleEsp8266.h>
#include <ArduinoJson.h>

// WiFi Credentials
#define WIFI_SSID "goku"
#define WIFI_PASS "00000000"

// Pin Definitions
#define MQ2_SENSOR A0   // MQ-2 Sensor connected to A0
#define BUZZER_PIN D5   // Buzzer for alerts
#define GREEN_LED D6    // Green LED for normal condition
#define RED_LED D7      // Red LED for gas detection alert

// Gas Detection Threshold
#define GAS_THRESHOLD 600

ESP8266WebServer server(80);

// Global variables to store sensor data
struct SensorData {
  int mq2Value;
  float voltage;
  bool isAlert;
  bool greenLed;
  bool redLed;
} sensorData;

void setup() {
    Serial.begin(115200);
    delay(1000);
    Serial.println("\n🚀 NodeMCU is Starting...");

    // Configure Pins
    pinMode(BUZZER_PIN, OUTPUT);
    pinMode(GREEN_LED, OUTPUT);
    pinMode(RED_LED, OUTPUT);

    digitalWrite(GREEN_LED, HIGH);
    digitalWrite(RED_LED, LOW);
    digitalWrite(BUZZER_PIN, LOW);

    // Connect to WiFi
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    Serial.print("🔄 Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        Serial.print(".");
        delay(500);
    }
    Serial.println("\n✅ WiFi Connected!");
    Serial.print("📡 IP Address: ");
    Serial.println(WiFi.localIP());

    // Connect to Blynk
    Blynk.begin(BLYNK_AUTH_TOKEN, WIFI_SSID, WIFI_PASS);
    Serial.println("✅ Connected to Blynk");

    // Setup API endpoints
    server.enableCORS(true);
    server.on("/api/sensor", HTTP_GET, handleGetSensorData);
    server.begin();
    Serial.println("🌐 HTTP server started");
}

void handleGetSensorData() {
    DynamicJsonDocument doc(1024);
    doc["mq2Value"] = sensorData.mq2Value;
    doc["voltage"] = sensorData.voltage;
    doc["isAlert"] = sensorData.isAlert;
    
    JsonObject ledStatus = doc.createNestedObject("ledStatus");
    ledStatus["green"] = sensorData.greenLed;
    ledStatus["red"] = sensorData.redLed;

    String response;
    serializeJson(doc, response);
    
    server.send(200, "application/json", response);
}

void updateSensorData() {
    // Read sensor data
    sensorData.mq2Value = analogRead(MQ2_SENSOR);
    sensorData.voltage = (sensorData.mq2Value / 1023.0) * 3.3;
    sensorData.isAlert = sensorData.mq2Value > GAS_THRESHOLD;

    // Update LED states
    if (sensorData.isAlert) {
        digitalWrite(GREEN_LED, LOW);
        digitalWrite(RED_LED, HIGH);
        digitalWrite(BUZZER_PIN, HIGH);
        delay(100);
        digitalWrite(BUZZER_PIN, LOW);
        
        sensorData.greenLed = false;
        sensorData.redLed = true;
        
        Blynk.logEvent("Gas_Detection", "⚠ Gas Leakage Detected!");
    } else {
        digitalWrite(GREEN_LED, HIGH);
        digitalWrite(RED_LED, LOW);
        digitalWrite(BUZZER_PIN, LOW);
        
        sensorData.greenLed = true;
        sensorData.redLed = false;
    }

    // Send data to Blynk
    Blynk.virtualWrite(V1, sensorData.mq2Value);

    // Debug output
    Serial.print("📊 MQ2 ADC Value: ");
    Serial.print(sensorData.mq2Value);
    Serial.print(" | Voltage: ");
    Serial.print(sensorData.voltage, 2);
    Serial.println("V"); 
}

void loop() {
    Blynk.run();
    server.handleClient();
    updateSensorData();
    delay(1000); // Small delay to prevent overwhelming the server
}

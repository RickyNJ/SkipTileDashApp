#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "LAPTOP-M6EHQK4G";
const char* password = "&iC17169";
const char* mqtt_server = "192.168.137.1";

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(9600);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  while (!client.connected()) {
    Serial.println("Connecting to MQTT broker...");
    if (client.connect("ESP32Client")) {
      Serial.println("Connected to MQTT broker");
    } else {
      Serial.print("Failed to connect to MQTT broker, rc=");
      Serial.print(client.state());
      Serial.println(" retrying in 5 seconds");
      delay(5000);
    }
  }
}

void loop() {
  client.loop();

  String message = "yeet";
  message += String(millis());

  client.publish("matten/1", message.c_str());
  
  // delay(5000);
}

void callback(char* topic, byte* payload, unsigned int length) {
  // Do something when a message is received
}

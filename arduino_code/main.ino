#include <WiFi.h>
#include <PubSubClient.h>

#define TRIG 5
#define ECHO 18

const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";
const char* mqtt_server = "broker.hivemq.com";

WiFiClient espClient;
PubSubClient client(espClient);

long duration;
float distance;
float binHeight = 30.0;

void setup() {
  Serial.begin(115200);
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  client.setServer(mqtt_server, 1883);
}

void reconnect() {
  while (!client.connected()) {
    client.connect("SmartBinESP32");
  }
}

float getDistance() {
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);

  duration = pulseIn(ECHO, HIGH);
  distance = duration * 0.034 / 2;
  return distance;
}

void loop() {
  if (!client.connected()) reconnect();
  client.loop();

  float d = getDistance();
  float fill = 100 - ((d / binHeight) * 100);

  if (fill < 0) fill = 0;
  if (fill > 100) fill = 100;

  String payload = "{";
  payload += "\"distance\":" + String(d) + ",";
  payload += "\"fill\":" + String(fill);
  payload += "}";

  client.publish("smartbin/data", payload.c_str());

  if (fill > 80) {
    client.publish("smartbin/alert", "BIN_FULL");
  }

  delay(3000);
}

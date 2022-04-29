#include <ESP8266WiFi.h>
#include <PubSubClient.h>


const char* ssid = "BELL839"; // Wifi SSID
const char* password = "checkmate"; // Wifi Password
const char* subTopic = "onoff"; 
const int LED_pin = 2; // LEd pin

//AskSensors MQTT config
const char* mqtt_server = "192.168.2.13";
unsigned int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  Serial.println("*****************************************************");
  Serial.println("Set LED as output");
  pinMode(LED_pin, OUTPUT); // set led as output
  digitalWrite(LED_pin, 1);
  
  Serial.print("********** connecting to WIFI : ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("->WiFi connected");
  Serial.println("->IP address: ");
  Serial.println(WiFi.localIP());
  
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  
  if (!client.connected()) 
    reconnect();
  Serial.print(subTopic);
  // susbscribe
  client.subscribe(subTopic);
}

void loop() {
  client.loop();
}


void callback(char* topic, byte* payload, unsigned int length) {

  for (int i = 0; i < length; i++) {
    Serial.println((char)payload[i]);
  }
  if((char)payload[0]=='1'){ 
    digitalWrite(LED_pin, 0);
    Serial.println("LED is ON");
  
  } else{
    digitalWrite(LED_pin, 1);
    Serial.println("LED is OFF");
  }
}

void reconnect() {
// Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("********** Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP32Client")) { 
      Serial.println("-> MQTT client connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println("-> try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

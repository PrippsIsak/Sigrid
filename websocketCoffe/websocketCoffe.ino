#include <ESP8266WiFi.h>
#include <ESPAsyncTCP.h>
#include <ESPAsyncWebServer.h>

const char *ssid = "NAME";
const char *password = "PASSWORD";

AsyncWebSocket ws("/ws");
AsyncWebServer server(5002);


void initWifi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi...");
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
    attempts++;
    if(attempts > 20) { // Print debug info if unable to connect after 20 seconds
      Serial.println("Failed to connect to WiFi");
      Serial.println("WiFi status: " + String(WiFi.status()));
      Serial.println("WiFi SSID: " + WiFi.SSID());
      Serial.println("WiFi password: " + WiFi.psk());
      break;
    }
  }
  if(WiFi.status() == WL_CONNECTED) {
    Serial.println("\nConnected to WiFi");
    Serial.println("IP Address: " + WiFi.localIP().toString());
  }
}

void notifyLight(bool state) {
  Serial.println("Inside light func");
  Serial.println(state ? "On" : "Off");
  if(state == true){
    digitalWrite(LED_BUILTIN, HIGH);
    delay(100);
  }
  else {
    digitalWrite(LED_BUILTIN, LOW);
    delay(100);
  }
  
  delay(100);
}

void handleWebSocketMessage(void *arg, uint8_t *data, size_t len) {
  AwsFrameInfo *info = (AwsFrameInfo *)arg;
  if (info->final && info->index == 0 && info->len == len && info->opcode == WS_TEXT) {
    data[len] = 0;
    String message = (char *)data;
    // Check if the message is "On" or "Off"
    Serial.println(message);
    if (strcmp((char *)data, "On") == 0) {
      
      notifyLight(true);
    }
    if (strcmp((char *)data, "Off") == 0) {
      notifyLight(false);
    }
  }
}

void onEvent(AsyncWebSocket *server, AsyncWebSocketClient *client, AwsEventType type, void *arg, uint8_t *data, size_t len) {
  Serial.println("inside event");
  switch (type) {
    case WS_EVT_CONNECT:
      Serial.printf("WebSocket client #%u connected from %s\n", client->id(), client->remoteIP().toString().c_str());
      break;
    case WS_EVT_DISCONNECT:
      Serial.printf("WebSocket client #%u disconnected\n", client->id());
      break;
    case WS_EVT_DATA:
      handleWebSocketMessage(arg, data, len);
      Serial.println("Inside evt data");
      
      break;
    case WS_EVT_PONG:
    case WS_EVT_ERROR:
      break;
  }
}

void initWebSocket() {
  ws.onEvent(onEvent);
  server.addHandler(&ws);
}

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  initWifi();  // Corrected 'initWiFi' to 'initWifi'
  initWebSocket();
  server.begin();
}

void loop() {
}

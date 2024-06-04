git#include <ESP8266WiFi.h>
#include <ESPAsyncTCP.h>
#include <ESPAsyncWebServer.h>

const char *ssid = "Pixel_4625";
const char *password = "isakaxelsson";

AsyncWebSocket ws("/ws");
AsyncWebServer server(5002);


void initWifi() {
  WiFi.mode(WIFI_STA);  // Corrected 'Wifi' to 'WiFi'
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("trying to connect..");
    delay(10000);
  }
  Serial.println(WiFi.localIP());
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

#include <OSCMessage.h>
#include <esp_now.h>
#include <WiFi.h>

// Define the MAC addresses of the receiving ESP32s
uint8_t peerMacA[] {0x94, 0xB9, 0x7E, 0xF9, 0x10, 0xF0};
uint8_t peerMacB[] {0x94, 0xB9, 0x7E, 0xF9, 0x10, 0xF1};
// Add more MAC addresses here for additional ESP32s

// Define the structure to receive data
typedef struct MyData {
  int tempo;
  int openclose;
} MyData;

MyData myData;
esp_now_peer_info_t peerInfo;

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  
  // Initialize ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("ESP-NOW initialization failed");
    return;
  }

  // Register the receiving ESP32s' MAC addresses
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;

  memcpy(peerInfo.peer_addr, peerMacA, 6);
  if (esp_now_add_peer(&peerInfo) != ESP_OK) {
    Serial.println("Failed to add peer A");
    return;
  }

  memcpy(peerInfo.peer_addr, peerMacB, 6);
  if (esp_now_add_peer(&peerInfo) != ESP_OK) {
    Serial.println("Failed to add peer B");
    return;
  }

  // Add more peers here for additional ESP32s
}

void loop() {
  if (Serial.available()) {
    OSCMessage msg;
    while (Serial.available() > 0) {
      msg.fill(Serial.read());
    }
    if (!msg.hasError()) {
      if (msg.fullMatch("/grid")) {
        Serial.println("OSC message received");

        // Save the message contents in a new variable
        myData.tempo = msg.getInt(0);
        myData.openclose = msg.getInt(1);
        // Send the message contents to the other ESP32 using ESP-NOW. one by one.
        esp_now_send(peerMacA, (uint8_t*) &myData, sizeof(myData));

        // Save the message contents in a new variable and send the data to corresponding ESP32
        myData.tempo = msg.getInt(0);
        myData.openclose = msg.getInt(2);
        esp_now_send(peerMacB, (uint8_t*) &myData, sizeof(myData));

        // Send confirmation message to Python
        Serial.write("OK\n");
      }
    }
    msg.empty();
  }
}

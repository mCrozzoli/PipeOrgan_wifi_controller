#include <esp_now.h>
#include <WiFi.h>

//id:1 mac address: peerMacA[] {0x94, 0xB9, 0x7E, 0xF9, 0x10, 0xF0};

// Define the structure to send data
typedef struct MyData {
  int tempo;
  int openclose;
} MyData;

String num_str;
int old_tempo;
float spb;
int delay_tempo;

MyData myData;

const int RELAY_PIN = 22;

//callback function that will be executed when data is received
void onDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len) {
  memcpy(&myData, incomingData, sizeof(myData));
  Serial.print("tempo: ");
  Serial.println(myData.tempo);
  Serial.print("openclose: ");
  Serial.println(myData.openclose);
  Serial.println();
}

void setup() {
  Serial.begin(115200);
  pinMode(RELAY_PIN, OUTPUT);

  //Set the device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);
  
  // Initialize ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("ESP-NOW initialization failed");
    return;
  }

  // Register the callback function to handle received data
  esp_now_register_recv_cb(onDataRecv);

  delay_tempo = 1000;
  old_tempo = 0;
}

void loop() {
  num_str = String(myData.openclose);
  
  if (old_tempo != myData.tempo && myData.tempo != 0){
    old_tempo = myData.tempo;
    spb = 60.0 / myData.tempo;  // Calculate seconds per beat
    delay_tempo = spb * 1000;  // Convert seconds to milliseconds 
    Serial.print("Tempo: ");
    Serial.println(myData.tempo);
    Serial.print("millisec: ");
    Serial.println(delay_tempo);
    
  }

  for (int i = 1; i < num_str.length(); i++) {
    int digit = num_str.charAt(i) - '0';
    
    if (digit == 0) {
      digitalWrite(RELAY_PIN, HIGH);
      Serial.println(digit);
      delay(delay_tempo);
    }
    else if (digit == 1) {
      digitalWrite(RELAY_PIN, LOW);
      Serial.println(digit);
      delay(delay_tempo);
    }
  }
}

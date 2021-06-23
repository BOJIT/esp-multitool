#include <Arduino.h>

// SLAVE CODE

#include <common.h>

static uint8_t broadcast_addr[] = { 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF };

typedef struct test_struct {
    int x;
    int y;
} test_struct_t;

// callback when data is sent
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  char macStr[18];
  Serial.print("Packet to: ");
  // Copies the sender mac address to a string
  snprintf(macStr, sizeof(macStr), "%02x:%02x:%02x:%02x:%02x:%02x",
           mac_addr[0], mac_addr[1], mac_addr[2], mac_addr[3], mac_addr[4], mac_addr[5]);
  Serial.print(macStr);
  Serial.print(" send status:\t");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
}

void OnDataRecv(const uint8_t * mac, const uint8_t *data, int len) {

  test_struct* test =(test_struct*) data;

  Serial.println(test->x);
  Serial.println(test->y);

}

void setup()
{
    // xTaskCreate(sensingTask, "sensing", 2048, NULL, 1, NULL);
    // xTaskCreate(freqTask, "freq", 2048, NULL, 2, NULL);

    Serial.begin(BAUD_RATE);

    Serial.println("Slave");

    Serial.print("ESP Board MAC Address:  ");
    Serial.println(WiFi.macAddress());

    WiFi.mode(WIFI_STA);

    if(esp_now_init() != ESP_OK) {
        Serial.println("Error initializing ESP-NOW");
        return;
    }

    // esp_now_register_send_cb(OnDataSent);

    esp_now_register_recv_cb(OnDataRecv);

    // // register peer
    // esp_now_peer_info_t peerInfo;
    // peerInfo.channel = 0;
    // peerInfo.encrypt = false;
    // // register first peer
    // memcpy(peerInfo.peer_addr, broadcast_addr, 6);
    // if (esp_now_add_peer(&peerInfo) != ESP_OK){
    //     Serial.println("Failed to add peer");
    //     return;
    // }
}

// Unused Task - using FreeRTOS as Scheduler
void loop() {
    vTaskDelete(NULL);

    // Serial.println("Still Slave");

    // vTaskDelay(1000);
}

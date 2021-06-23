// Common definitions

#define BAUD_RATE 115200

#include <esp_now.h>
#ifdef ESP32
    #include <WiFi.h>
#else
    #include <ESP8266WiFi.h>
#endif
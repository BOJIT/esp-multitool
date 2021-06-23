// Common definitions

#define BAUD_RATE 115200

#include <esp_now.h>
#ifdef ESP32
    #include <WiFi.h>
#else
    #include <ESP8266WiFi.h>
#endif

/**
    @brief ESP-Multitool header:
    all packets from this library include this 32-bit header. As all slaves
    listen to the broadcast address, this header reduces the likelihood of other
    ESP-NOW packets interfering with the operation of this library. The value
    is simply the CRC-32 of the string 'esp-multitool':
    https://crccalc.com/?crc=esp-multitool&method=crc32&datatype=ascii&outtype=hex
**/
#define ESPM_HDR   0x0B51C2E8

typedef enum {
    ESPM_NULL = 0,
    ESPM_SRV_REQ,
    ESPM_SRV_RESP,
    ESPM_SRV_CTRL
} espm_type;
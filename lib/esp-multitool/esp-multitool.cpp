/**
 * \file
 * \brief esp-multitool main handler
 *
 * This is the actual handler code for the esp-multitool. The same codebase
 * builds for both the master and the slave, but only slave methods are included
 * by default. This is overriden by a macro.
 */

/* -------------------------------------------------------------------------- */
/* ------------------------------ INCLUDES ---------------------------------- */
/* -------------------------------------------------------------------------- */


#include "esp-multitool.h"
#include "packet.h"


#include <esp_now.h>
#ifdef ESP32
    #include <WiFi.h>
#else
    #include <ESP8266WiFi.h>
#endif /*  */


/* -------------------------------------------------------------------------- */
/* ------------------------------- MACROS ----------------------------------- */
/* -------------------------------------------------------------------------- */




/* -------------------------------------------------------------------------- */
/* ------------------------------ GLOBALS ----------------------------------- */
/* -------------------------------------------------------------------------- */


static const uint8_t broadcast_addr[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};



/* -------------------------------------------------------------------------- */
/* ----------------------------- FUNCTIONS ---------------------------------- */
/* -------------------------------------------------------------------------- */


/**
  * \brief Callback function of receiving ESPNOW data
  * \param mac peer MAC address
  * \param data received data
  * \param len length of received data
  */
void esp_now_recv_cb(const uint8_t *mac, const uint8_t *data, int len)
{
    // @todo pass by reference
    espm_msg_buf_t tmp;

    /* Copy across MAC address and packet payload */
    memcpy(tmp.mac, broadcast_addr, sizeof(broadcast_addr));

}


/**
 * @brief esp-multitool protocol handler task
 * @param args pointer to struct of any runtime arguments
 */
static void handlerTask(void *args)
{
    /* Initialise ESP-NOW */


    for(;;) {

        /* Initialise ESP-NOW hardware */
        WiFi.mode(WIFI_STA);
        if(esp_now_init() != ESP_OK) {
            ESPM_LOG.println("Error initializing ESP-NOW");
            vTaskDelete(NULL);
            return;
        }




    }
}

/* -------------------------------------------------------------------------- */
/* ------------------------ CLASS IMPLEMENTATION ---------------------------- */
/* -------------------------------------------------------------------------- */

ESPMultitool::ESPMultitool(void)
{
    _msgQueue = xQueueCreate(ESPM_RX_BUF_LEN, sizeof(espm_msg_buf_t));
    xTaskCreate(handlerTask, "esp-multitool", 2048, NULL, 1, &_handler);
}

ESPMultitool::~ESPMultitool(void)
{
    vQueueDelete(_msgQueue);

    vTaskDelete(_handler);
}
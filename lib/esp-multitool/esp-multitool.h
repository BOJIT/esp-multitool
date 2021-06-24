/**
 *\file
 *\brief esp-multitool main header
 *
 * This is the header that should be included for instantiating a class on
 * esp-multitool slave devices.
 */

#ifndef __ESPM_MAIN_H__
#define __ESPM_MAIN_H__

/* -------------------------------------------------------------------------- */
/* ------------------------------ INCLUDES ---------------------------------- */
/* -------------------------------------------------------------------------- */


#include "Stream.h"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"


/* -------------------------------------------------------------------------- */
/* ------------------------------- MACROS ----------------------------------- */
/* -------------------------------------------------------------------------- */


/* By default only master code is included if not overridden */
#ifndef ESPM_MASTER
    #define ESPM_SLAVE
#endif /* ESPM_MASTER */

/* ESP-NOW RX queue length - if the CPU is very busy increase queue size */
#ifndef ESPM_RX_BUF_LEN
    #define ESPM_RX_BUF_LEN 5
#endif /* ESPM_RX_BUF_LEN */

/* ESP-NOW TX queue length - if the CPU is very busy increase queue size */
#ifndef ESPM_TX_BUF_LEN
    #define ESPM_TX_BUF_LEN 5
#endif /* ESPM_TX_BUF_LEN */

#ifndef ESPM_LOG
    #define ESPM_LOG Serial
#endif /* ESPM_LOG */

/* -------------------------------------------------------------------------- */
/* ---------------- ----------- ENUMERATIONS -------------------------------- */
/* -------------------------------------------------------------------------- */



/* -------------------------------------------------------------------------- */
/* ------------------------------ TYPEDEFS ---------------------------------- */
/* -------------------------------------------------------------------------- */





/* -------------------------------------------------------------------------- */
/* -------------------------- CLASS DECLARATION ----------------------------- */
/* -------------------------------------------------------------------------- */


class ESPMultitool {
private:
    QueueHandle_t _msgQueue;
    TaskHandle_t _handler;

public:
    class Serial: public Stream {
        private:
    };

    ESPMultitool(void);
    ~ESPMultitool(void);
};


/* -------------------------------------------------------------------------- */
/* -------------------------------------------------------------------------- */
/* -------------------------------------------------------------------------- */

#endif /* __ESPM_MAIN_H__ */
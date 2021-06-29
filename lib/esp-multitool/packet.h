/**
 * \file
 * \brief esp-multitool packet structures
 *
 * This file contains the data structures for packets used by the esp-multitool.
 */

#ifndef __ESPM_PACKET_H__
#define __ESPM_PACKET_H__

/* -------------------------------------------------------------------------- */
/* ------------------------------ INCLUDES ---------------------------------- */
/* -------------------------------------------------------------------------- */


#include <stdint.h>
#include <stdbool.h>


/* -------------------------------------------------------------------------- */
/* ------------------------------- MACROS ----------------------------------- */
/* -------------------------------------------------------------------------- */


/**
    \def ESP-Multitool header:
    \brief All packets from this library include this 32-bit header. As all slaves
    listen to the broadcast address, this header reduces the likelihood of other
    ESP-NOW packets interfering with the operation of this library. The value
    is simply the CRC-32 of the string 'esp-multitool':
    https://crccalc.com/?crc=esp-multitool&method=crc32&datatype=ascii&outtype=hex
**/
#define ESPM_HDR   0x0B51C2E8


/* -------------------------------------------------------------------------- */
/* ---------------------------- ENUMERATIONS -------------------------------- */
/* -------------------------------------------------------------------------- */


/**
 * \enum espm_err
 * \brief Error enumeration for ESP-NOW packets
 */
enum {
    ESPM_ERR_OK = 0,
    ESPM_ERR_MEM,
};
typedef uint8_t espm_err_t;

/**
 * \enum espm_type
 * \brief Message type for ESP-NOW
 */
enum {
    ESPM_MSG_NULL = 0,
    ESPM_MSG_SRV_REQ,
    ESPM_MSG_SRV_RESP,
    ESPM_MSG_OTA_REQ,
    ESPM_MSG_OTA_RESP,
    ESPM_MSG_SERIAL_REQ,
    ESPM_MSG_SERIAL_RESP,
    ESPM_MSG_CTRL_REQ,
    ESPM_MSG_CTRL_RESP,
    ESPM_MSG_STAT_REQ,
    ESPM_MSG_STAT_RESP
};
typedef uint8_t espm_type_t;

/* -------------------------------------------------------------------------- */
/* ------------------------------ TYPEDEFS ---------------------------------- */
/* -------------------------------------------------------------------------- */


/**
 * \struct espm_header
 * \brief Message header for ESP-NOW
 */
typedef struct __attribute__((packed)) {
    uint32_t id;        /* ESPM ID: Packets with non-matching IDs are dropped */
    espm_type_t type;   /* Message type (see #espm_type_t) */
} espm_header_t;

/**
 * \struct espm_buf
 * \brief Message struct for non-structured buffers that may span multiple
 * ESP-Now packets and may need dynamic allocation.
 */
typedef struct __attribute__((packed)) {
    uint32_t len;   /* Total number of bytes in the entire packet sequence */
    uint32_t seq;   /* Index of this packet in the entire packet sequence */
    /* Buffer - sized to fill the remainder of an ESP-NOW packet */
    uint8_t buf[250 - sizeof(espm_header_t) - sizeof(len) - sizeof(seq)];
} espm_buf_t;

/**
 * \struct espm_ack
 * \brief Message struct for responses that don't need to return any data.
 */
typedef struct __attribute__((packed)) {
    espm_err_t err;
} espm_ack_t;

/**
 * \struct espm_srv_req
 * \brief Service request packet
 */
typedef struct __attribute__((packed)) {
    bool query_locked;  /* If set to true, 'locked' devices will respond */
} espm_srv_req_t;

/**
 * \struct espm_serial_req
 * \brief Serial request packet - while technically a 'request', this packet
 * does not request any information, instead sending a stream buffer
 */
typedef struct __attribute__((packed)) {
    espm_buf_t buf;  /* Serial stream buffer */
} espm_serial_req_t;

/**
 * \struct espm_srv_resp
 * \brief Service response packet
 */
typedef struct __attribute__((packed)) {
    espm_err_t err; /* Error code */
    char name[20];  /* Human-readable slave device name: can be used as
                        identifier instead of MAC address if unique */
    bool ota;       /* Set to true if slave accepts OTA firmware updates */
    bool serial;    /* Set to true if virtual slave port is created */
    bool ctrl;      /* Set to true if control parameter map is available */
    bool stat;      /* Set to true if status parameter map is available */
} espm_srv_resp_t;

/**
 * \struct espm_serial_resp
 * \brief Serial response packet - standard acknowledgement
 */
typedef struct __attribute__((packed)) {
    espm_ack_t ack; /* Serial buffer packet acknowledgement */
} espm_serial_resp_t;

/**
 * \struct espm_msg_buf_t
 * \brief Message buffer - sized at the maximum ESP-NOW Message size
 */
typedef struct __attribute__((packed)) {
    uint8_t mac[6];         /* Mac address */
    espm_header_t header;   /* Header buffer */
    union {                 /* Union of all possible message types */
        espm_srv_req_t srv_req;
        espm_serial_req_t serial_req;
        espm_srv_resp_t srv_resp;
        espm_serial_resp_t serial_req;
    } msg;
} espm_msg_buf_t;


/* -------------------------------------------------------------------------- */
/* -------------------------------------------------------------------------- */
/* -------------------------------------------------------------------------- */

#endif /* __ESPM_PACKET_H__ */

/**
 ******************************************************************************
 * @file           : usbd_cdc_if.h
 * @version        : v1.0_Cube
 * @brief          : Header for usbd_cdc_if.c file.
 ******************************************************************************
 * @attention
 *
 * <h2><center>&copy; Copyright (c) 2021 STMicroelectronics.
 * All rights reserved.</center></h2>
 *
 * This software component is licensed by ST under Ultimate Liberty license
 * SLA0044, the "License"; You may not use this file except in compliance with
 * the License. You may obtain a copy of the License at:
 *                             www.st.com/SLA0044
 *
 ******************************************************************************
 */

#pragma once

#ifdef __cplusplus
extern "C"
{
#endif

#include "usbd_cdc.h"

#define APP_RX_DATA_SIZE 2048
#define APP_TX_DATA_SIZE 2048

    /* CDC Interface callback. */
    extern USBD_CDC_ItfTypeDef USBD_CDC_Interface_fops_FS;

    uint8_t CDC_Transmit_FS(uint8_t *Buf, uint16_t Len);

#ifdef __cplusplus
}
#endif

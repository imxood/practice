/**
 ******************************************************************************
 * @file           : usbd_storage_if.h
 * @version        : v1.0_Cube
 * @brief          : Header for usbd_storage_if.c file.
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

/* Includes ------------------------------------------------------------------*/
#include "usbd_msc.h"
    extern USBD_StorageTypeDef USBD_Storage_Interface_fops_FS;

#ifdef __cplusplus
}
#endif

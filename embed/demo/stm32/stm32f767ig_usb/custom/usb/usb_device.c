#include "usbd_composite.h"
#include "usbd_desc.h"

/* USB Device Core handle declaration */
USBD_HandleTypeDef hUsbDeviceFS;

/* init function */
void USB_DEVICE_Init(void)
{
    /* Init Device Library, Add Supported Class and Start the library*/
    USBD_Init(&hUsbDeviceFS, &FS_Desc, DEVICE_FS);

    USBD_RegisterClass(&hUsbDeviceFS, &USBD_COMPOSITE);

    // USBD_MSC_RegisterStorage(&hUsbDeviceFS, &USBD_Storage_Interface_fops_FS);

    USBD_Start(&hUsbDeviceFS);
}

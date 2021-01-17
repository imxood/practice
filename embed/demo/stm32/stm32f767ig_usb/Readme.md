## 配置

在 main.c 中, 调用 MX_USB_DEVICE_Init 完成对 USB 设备的初始化

在 usb_device.c 中, MX_USB_DEVICE_Init 函数:

    1. USBD_Init(&hUsbDeviceFS, &FS_Desc, DEVICE_FS)

        在 usbd_desc.c 中, USBD_FS_DeviceDesc 定义了 设备描述符

    2. USBD_RegisterClass(&hUsbDeviceFS, &USBD_CUSTOM_HID)

        在 usbd_customhid.c 中, USBD_CUSTOM_HID_CfgFSDesc 定义了 配置描述符 并 包含 接口描述符 及 端点描述符

    3. USBD_CUSTOM_HID_RegisterInterface(&hUsbDeviceFS, &USBD_CustomHID_fops_FS)

        在 usbd_custom_hid_if.c 中, CUSTOM_HID_ReportDesc_FS 定义了 HID 报告描述符

## HOST 发送 数据

在 USB 的中断处理函数 HAL_PCD_IRQHandler 中,

# zephyr笔记

## 环境搭建

    https://docs.zephyrproject.org/latest/getting_started/index.html

    west init zephyrproject

    cd zephyrproject
    west update
    west zephyr-export

    pip install -r zephyr/scripts/requirements.txt --user

    aria2c -x 16 -s 16 -j 16 https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v0.11.4/zephyr-sdk-0.11.4-setup.run

    chmod +x zephyr-sdk-0.11.4-setup.run
    ./zephyr-sdk-0.11.4-setup.run

    west completion bash > ~/west-completion.bash

    echo "source ~/west-completion.bash" >> ~/.bashrc

    sudo cp ~/zephyr-sdk/sysroots/x86_64-pokysdk-linux/usr/share/openocd/contrib/60-openocd.rules /etc/udev/rules.d
    sudo udevadm control --reload

## f767

    cd zephyrproject
    git clone https://github.com/imxood/stm32f7_app.git

## west 命令

    west build -b stm32f767i_disco -- -DBOARD_ROOT=.

    west build -t menuconfig

    west flash


## 调试 west

    west 主文件: ~/.local/lib/python3.7/site-packages/west/app/main.py

    {
        "name": "debug west",
        "type": "python",
        "request": "launch",
        "cwd": "${workspaceFolder}/stm32f7_app",
        "module": "west",
        "justMyCode": false,
        "args": [
            "-vv",
            "flash",
            "--skip-rebuild"
        ]
    }

## 调试 zephyr.elf

    在vscode中 用这个 zephyr-sdk/arm-zephyr-eabi/bin/arm-zephyr-eabi-gdb 无法使用, "ln -s" 创建软连接/usr/bin/arm-none-eabi-gdb也不行
    需要使用官方的 arm-none-eabi-gdb

    {
        "name": "Cortex Debug",
        "cwd": "${workspaceRoot}",
        "executable": "build/zephyr/zephyr.elf",
        "request": "launch",
        "type": "cortex-debug",
        "servertype": "openocd",
        "configFiles": [
            "board/stm32f7discovery.cfg"
        ]
    }

## zephyr 笔记

    zephyr设备树, 详细的介绍: https://docs.zephyrproject.org/latest/reference/devicetree/api.html

    stm32f7_app/build/zephyr/zephyr.dts, 编译后的设备树
    stm32f7_app/build/zephyr/include/generated/devicetree_unfixed.h, 根据设备树生成的头文件

    #define DT_DRV_COMPAT st_stm32_sdmmc, 访问设备树时, 需要通过 DT_DRV_COMPAT 去访问对应的设备树实例
    DT_DRV_INST(0)


### west 命令

    cd zephyrproject/zephyr

    编译:
        west build -p auto -b stm32f769i_disco samples/hello_world -- -DCMAKE_EXPORT_COMPILE_COMMANDS=ON

    后面参数只需要一次就可以了: west build

    烧写:
        west flash

### 启用 shell

    CONFIG_SHELL=y

### 使用UART3

     1. 添加自定义 DTS 设备树文件 custom.overlay:

        &usart3 {
            pinctrl-0 = <&usart3_tx_pb10 &usart3_rx_pb11>;
            current-speed = <115200>;
            status = "okay";
        };

    2. 在 CMakeLists.txt 中, 在 "find_package(Zephyr..." 前 添加:
       set(DTC_OVERLAY_FILE "${CMAKE_CURRENT_SOURCE_DIR}/custom.overlay")

    3. 在 prj.conf 中添加:
        CONFIG_UART_CONSOLE_ON_DEV_NAME="UART_3"
        CONFIG_UART_SHELL_ON_DEV_NAME="UART_3"

### 启用 usb

    pinctrl-0 中的配置可以在 devicetree_unfixed.h 中找到

    1. 添加自定义 DTS 设备树文件 custom.overlay:
        &usbotg_fs {
            pinctrl-0 = <&usb_otg_fs_dm_pa11 &usb_otg_fs_dp_pa12>;
            status = "okay";
        };

    2. 在 CMakeLists.txt 中, 在 "find_package(Zephyr..." 前 添加:
       set(DTC_OVERLAY_FILE "${CMAKE_CURRENT_SOURCE_DIR}/custom.overlay")

    3. 在 prj.conf 中添加:

        CONFIG_USB=y
        CONFIG_USB_DC_STM32=y
        CONFIG_USB_DEVICE_STACK=y

        CONFIG_USB_CDC_ACM=y

    4. 在 main.c 中添加code, 开启USB:

        #include <usb/usb_device.h>

        static void fn_usb_dc_status_callback(enum usb_dc_status_code cb_status,
                        const uint8_t *param)
        {
            printk("cb_status: %d\n", cb_status);
        }

        void main(void)
        {
            printk("Hello World! %s\n", CONFIG_BOARD);
            int ret = usb_enable(fn_usb_dc_status_callback);
            if (ret) {
                printk("usb enable failed\n");
            }
        }

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
        "executable": "stm32f7_app/build/zephyr/zephyr.elf",
        "request": "launch",
        "type": "cortex-debug",
        "servertype": "openocd",
        "configFiles": [
            "stm32f7_app/boards/arm/stm32f767i_disco/support/openocd.cfg"
        ],
        "armToolchainPath": "/develop/programs/gcc-arm-none-eabi-9-2020-q2-update/bin"
    }

## zephyr 笔记

    stm32f7_app/build/zephyr/zephyr.dts, 编译后的设备树
    stm32f7_app/build/zephyr/include/generated/devicetree_unfixed.h, 根据设备树生成的头文件

    #define DT_DRV_COMPAT st_stm32_sdmmc, 访问设备树时, 需要通过 DT_DRV_COMPAT 去访问对应的设备树实例
    DT_DRV_INST(0), 与 DT 相关的DEFINE, 内部都是用 DT_DRV_COMPAT 去拼凑 DEFINE 的

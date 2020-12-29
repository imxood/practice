## 使用串口烧写bin文件

    使用软件 STM32CubeProgrammer 烧写 bin程序

    连接:

        PA9 (TX)  --  Adapter Rx
        PA10(RX)  --  Adapter Tx
        GND       --  Adapter GND
        5V        --  Adapter 5V

        BOOT0     --  1
        BOOT1     --  0

    上电后, 先按一下Reset, 才能继续操作

    STM32CubeProgrammer:

        选择UART, 使用默认设置, "Connect"

        左边, 侧栏, 点击 "Erasing & programming", 点击 "Browser", 选择bin文件

        点击 "Start Programming"

## 编译 daplink (gcc版本)

    安装必要的工具:
        pip3 install --user mbed-cli mercurial

    vi ~/.hgrc

    [http_proxy]
    host=your_proxy_address:port
    [https_proxy]
    host=your_proxy_address:port

    git clone https://github.com/flit/DAPLink.git

    cd DAPLink
    git checkout feature/gcc

    pip3 install --user -r requirements.txt

    mbed deploy --verbose

    project-name 定义在 projects.yaml 中的 "projects":

        progen generate -t make_gcc_arm -p stm32f103xb_bl

        cd projectfiles/make_gcc_arm/stm32f103xb_bl
        make -j

        得到 build/stm32f103xb_bl.bin

    实际的配置, 但是没找到在代码中的定义:

        PA4 -> SWDIO  to target device
        PA5 -> SWCLK  to target device
        PA6 -> nRESET to target device

        PA2 : USART TX (to target device's RX)
        PA3 : USART RX (to target device's TX)

        PA11 : USB DM (to host)
        PA12 : USB DP (to host)

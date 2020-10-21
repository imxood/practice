# qemu stm32 编译

## code

git clone https://github.com/beckus/qemu_stm32.git

## 必要的环境

    sudo apt-get install -y --no-install-recommends binutils-arm-none-eabi ca-certificates libnewlib-arm-none-eabi findutils gcc libglib2.0-dev libfdt-dev libpixman-1-dev make openssh-client pkgconf python zlib1g-dev

    sudo apt install python3-virtualenv python2

## 编译

    cd qemu_stm32

    进入到python2环境:
        virtualenv -p python2 py2venv
        source ./py2venv/bin/activate

    ./configure --target-list="arm-softmmu" --enable-debug --disable-werror --extra-cflags=-DSTM32_UART_NO_BAUD_DELAY --extra-cflags=-DSTM32_UART_ENABLE_OVERRUN --disable-gtk
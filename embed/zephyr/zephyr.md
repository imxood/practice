# zephyr笔记

## 环境搭建

    west init zephyrproject
    cd zephyrproject
    west update
    west zephyr-export
    pip install -r zephyr/scripts/requirements.txt --user
    aria2c -x 10 -s 10 -j 10 https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v0.11.3/zephyr-sdk-0.11.3-setup.run
    chmod +x zephyr-sdk-0.11.3-setup.run
    ./zephyr-sdk-0.11.3-setup.run

    west completion bash > ~/west-completion.bash

    echo "source ~/west-completion.bash" >> ~/.bashrc

    sudo cp ~/zephyr-sdk/sysroots/x86_64-pokysdk-linux/usr/share/openocd/contrib/60-openocd.rules /etc/udev/rules.d
    sudo udevadm control --reload

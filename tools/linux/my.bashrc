
export PATH="$PATH"

export http_proxy=http://127.0.0.1:1081
export https_proxy=http://127.0.0.1:1081

arm_none_eabi_gdb=$HOME/programs/gcc-arm-none-eabi-8-2019-q3-update
export PATH=$arm_none_eabi_gdb/bin:$PATH


export IDF_PATH=/home/imxood/develop/sources/esp-idf
export PATH=$HOME/programs/xtensa-esp32-elf/bin:$IDF_PATH/tools:$PATH


export PATH=$HOME/programs/Qt5.13.0/Tools/QtCreator/bin:$PATH


export PATH=/usr/lib/go-1.12/bin:$PATH
export GOROOT=/usr/lib/go-1.12
export GOPATH=$HOME/develop/go


export ZEPHYR_SDK_INSTALL_DIR=$HOME/programs/zephyr-sdk
. $HOME/develop/sources/zephyrproject/zephyr/zephyr-env.sh


# eval "$(pyenv activate py3.7 || true)"
export PYENV_VIRTUALENV_DISABLE_PROMPT=1

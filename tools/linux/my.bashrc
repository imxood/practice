
export PATH="$HOME/.local/bin:$PATH"

export http_proxy=http://127.0.0.1:1081
export https_proxy=http://127.0.0.1:1081

arm_none_eabi_gdb=/home/imxood/programs/gcc-arm-none-eabi-8-2019-q3-update
export PATH=$arm_none_eabi_gdb/bin:$PATH


export IDF_PATH=/home/imxood/develop/sources/esp-idf
export PATH=~/programs/xtensa-esp32-elf/bin:$IDF_PATH/tools:$PATH


export PATH=~/programs/Qt5.13.0/Tools/QtCreator/bin:$PATH


export PATH=/usr/lib/go-1.12/bin:$PATH
export GOROOT=/usr/lib/go-1.12
export GOPATH=~/develop/go


export ZEPHYR_SDK_INSTALL_DIR=~/programs/zephyr-sdk
. ~/develop/sources/zephyrproject/zephyr/zephyr-env.sh


#eval "$(pyenv virtualenv-init - || true)"
#export PYENV_VIRTUALENV_DISABLE_PROMPT=1

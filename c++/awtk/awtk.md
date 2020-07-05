## ubuntu环境

    pip3 install --user scons
    sudo apt-get install libsndio-dev libgtk-3-dev libglu1-mesa libglu1-mesa-dev libgl1-mesa-glx libgl1-mesa-dev libasound2-dev git vim clang-format

## 缺少hb.h

3rd/SDL/SConscript:60

添加:
    '/usr/include/harfbuzz'

# qt 学习笔记

## ubuntu 安装qt

    sudo apt-get install build-essential g++
    sudo apt-get install libgl1-mesa-dev libglu1-mesa-dev freeglut3-dev

qt creator 下载地址: http://download.qt.io/archive/qt/5.14/5.14.0

设置环境变量

    export QTDIR=$HOME/programs/Qt5.14.0/5.14.0/gcc_64
    export PATH=$QTDIR/bin:$PATH

无法输入中文

    cp /usr/lib/x86_64-linux-gnu/qt5/plugins/platforminputcontexts ~/programs/Qt5.14.0/Tools/QtCreator/lib/Qt/plugins/platforminputcontexts/


## ubuntu 源码编译qt15

    下载源码:
        http://download.qt.io/archive/qt/5.15/5.15.0/single/qt-everywhere-src-5.15.0.tar.xz


    用于编译qdoc, 没什么用:
        sudo apt install clang llvm


    System requirements
    ------------------
    - Perl 5.8 or later
    - Python 2.7 or later
    - C++ compiler supporting the C++11 standard


    ./configure -opensource -confirm-license -skip qtlocation -skip qtvirtualkeyboard

    make -j10

    sudo make install


     -skip qtlocation -skip qtwayland -skip qtscript

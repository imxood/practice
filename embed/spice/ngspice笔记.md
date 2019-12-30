# ngspice笔记

    sudo apt install automake libtool libxaw7-dev libreadline-dev
    
    git clone https://git.code.sf.net/p/ngspice/ngspice ngspice-ngspice

    cd ngspice-ngspice

    ./autogen.sh
    mkdir -p debug && cd debug
    ../configure --with-x --with-readline=yes
    make -j
    sudo make install

    cd ..
    ngspice
    source examples/soi/inv_tr.sp
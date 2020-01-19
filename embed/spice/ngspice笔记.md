# ngspice笔记

## 源码编译

    sudo apt install automake libtool libxaw7-dev libreadline-dev

    git clone https://git.code.sf.net/p/ngspice/ngspice

    cd ngspice

    ./autogen.sh

    mkdir -p debug && cd debug

    ../configure --with-ngshared --enable-cider --enable-xspice  --with-x --enable-stepdebug --enable-cpdebug

    make -j4
    sudo make install

    cd ..
    ngspice
    source examples/soi/inv_tr.sp


    如果发生错误: Undefined symbol error 'hcomp' when using libngspice.so
    可能是这有的操作:
        Clean folder -> normal build -> shared lib build -> problem occurs.
    请考虑, 应该可以解决:
        Clean folder -> shared lib build -> OK.

## 源码分析

    var_alloc(char *name, struct variable *next)

    void cp_vset(char *varname, enum cp_types type, void *value);

        设置一个参数列表: struct variable *variables; varname是不重复的


    ngSpice_Init():

        cp_vset("rndseed", CP_NUM, 1);

        cp_vset("sharedmode", CP_BOOL, True);

    cp_init

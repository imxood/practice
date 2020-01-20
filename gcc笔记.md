# gcc笔记

## gcc安装

sudo apt install software-properties-common
sudo add-apt-repository ppa:ubuntu-toolchain-r/test

sudo apt install gcc-9 g++-9

sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 90 --slave /usr/bin/g++ g++ /usr/bin/g++-9 --slave /usr/bin/gcov gcov /usr/bin/gcov-9
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-5 90 --slave /usr/bin/g++ g++ /usr/bin/g++-5 --slave /usr/bin/gcov gcov /usr/bin/gcov-5

sudo update-alternatives --config gcc


## gcc源码编译

sudo apt install libgmp-dev libmpfr-dev libmpc-dev

svn checkout http://gcc.gnu.org/svn/gcc/trunk gcc-source

mkdir gcc-source/objdir

cd gcc-source/objdir

../configure --enable-languages=c,c++ --enable-checking=release --disable-multilib --disable-checking

make -j10

sudo make install

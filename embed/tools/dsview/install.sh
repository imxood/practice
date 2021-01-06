cd libsigrok4DSL
./autogen.sh
./configure
make -j
sudo make install
cd ..

cd libsigrokdecode4DSL
./autogen.sh
./configure
make -j
sudo make install
cd ..

cd DSView
mkdir build && cd build && cmake ..
make -j
sudo make install

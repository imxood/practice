# DSView

## 编译

	git clone https://github.com/DreamSourceLab/DSView.git

	sudo apt-get install git-core build-essential cmake autoconf automake libtool pkg-config \
	libglib2.0-dev libzip-dev libudev-dev libusb-1.0-0-dev \
	python3-dev qt5-default libboost-dev libboost-test-dev libboost-thread-dev libboost-system-dev libboost-filesystem-dev check libfftw3-dev

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

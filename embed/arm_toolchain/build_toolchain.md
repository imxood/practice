
## 下载 arm-none-eabi gnu toolchain sources

	下载 src tar package

	https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads

	下面是我用来编译的过程:

		sudo su
		apt-get install software-properties-common

		# Ensure package for Ubuntu Trusty are chosen by default
		echo 'APT::Default-Release "trusty";' > /etc/apt/apt.conf.d/00default

		dpkg --add-architecture i386

		apt-get install gcc-mingw-w64-i686 g++-mingw-w64-i686 binutils-mingw-w64-i686

		apt-get -f install -y \
			build-essential \
			autoconf \
			autogen \
			bison \
			dejagnu \
			flex \
			flip \
			gawk \
			git \
			gperf \
			gzip \
			nsis \
			openssh-client \
			p7zip-full \
			perl \
			python-dev \
			libisl-dev \
			scons \
			tcl \
			texinfo \
			tofrodos \
			wget \
			zip \
			texlive \
			texlive-extra-utils \
			libncurses5-dev

		exit

		mkdir -p ~/programs/toolchain
		cp gcc-arm-none-eabi-9-2020-q2-update-src.tar.bz2 ~/programs/toolchain

		cd ~/programs/toolchain
		tar -xjf gcc-arm-none-eabi-9-2020-q2-update-src.tar.bz2

		cd gcc-arm-none-eabi-9-2020-q2-update/
		./install-sources.sh --skip_steps=mingw32
		./build-prerequisites.sh --skip_steps=mingw32
		./build-toolchain.sh --skip_steps=mingw32

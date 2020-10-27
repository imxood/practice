# freecad 使用笔记

## 编译 vtk

	sudo apt install cmake libavcodec-dev libavformat-dev libavutil-dev libboost-dev libdouble-conversion-dev libeigen3-dev libexpat1-dev libfontconfig-dev libfreetype6-dev libgdal-dev libglew-dev libhdf5-dev libjpeg-dev libjsoncpp-dev liblz4-dev liblzma-dev libnetcdf-dev libnetcdf-cxx-legacy-dev libogg-dev libpng-dev libpython3-dev libqt5opengl5-dev libqt5x11extras5-dev libsqlite3-dev libswscale-dev libtheora-dev libtiff-dev libxml2-dev libxt-dev qtbase5-dev qttools5-dev zlib1g-dev

	git clone https://gitlab.kitware.com/vtk/vtk.git VTK

	git checkout v8.2.0

	mkdir VTK/build
	cd VTK/build
	cmake .. -DCMAKE_BUILD_TYPE:STRING=Debug -GNinja \
			-DCMAKE_INSTALL_RPATH=$HOME/vtk-inst \
			-DVTK_Group_Qt=ON \
			-DVTK_QT_VERSION=5 \
			-DVTK_Group_Imaging=ON \
			-DVTK_Group_Views=ON \
			-DModule_vtkRenderingFreeTypeFontConfig=ON \
			-DVTK_WRAP_PYTHON=ON \
			-DVTK_PYTHON_VERSION=3 \
			-DPYTHON_EXECUTABLE=/usr/bin/python3 \
			-DPYTHON_INCLUDE_DIR=/usr/include/python3.8 \
			-DPYTHON_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython3.8.so \
			-DBUILD_TESTING=OFF \
			-DVTK_USE_SYSTEM_LIBRARIES=ON \
			-DVTK_USE_SYSTEM_LIBPROJ4=OFF \
			-DVTK_USE_SYSTEM_GL2PS=OFF \
			-DVTK_USE_SYSTEM_LIBHARU=OFF \
			-DVTK_USE_SYSTEM_PUGIXML=OFF \
			-DCMAKE_BUILD_TYPE=Release \
			-GNinja



## 源码编译

	sudo apt-get install doxygen-latex  doxygen-doc doxygen-gui graphviz
	sudo apt install libboost-all-dev libxerces-c-dev libocct-data-exchange-dev libvtkgdcm-dev

	sudo apt-get install build-essential cmake python python-matplotlib libtool libcoin80-dev \
		libsoqt4-dev libxerces-c-dev libboost-dev libboost-filesystem-dev libboost-regex-dev  \
		libboost-program-options-dev libboost-signals-dev libboost-thread-dev libboost-python-dev \
		libqt4-dev libqt4-opengl-dev qt4-dev-tools python-dev python-pyside pyside-tools 'liboce*-dev' \
		oce-draw libeigen3-dev libqtwebkit-dev libshiboken-dev libpyside-dev libode-dev swig libzipios++-dev \
		libfreetype6 libfreetype6-dev





	git clone https://github.com/FreeCAD/FreeCAD.git

	mkdir FreeCAD/build
	cd FreeCAD/build
	cmake .. -DBUILD_QT5=ON -DPYTHON_EXECUTABLE=/usr/bin/python3 -GNinja





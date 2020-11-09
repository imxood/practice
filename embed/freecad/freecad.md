# freecad 使用笔记

## 源码编译

	sudo apt build-dep freecad

	sudo apt install cmake cmake-gui libboost-date-time-dev libboost-dev libboost-filesystem-dev libboost-graph-dev libboost-iostreams-dev libboost-program-options-dev libboost-python-dev libboost-regex-dev libboost-serialization-dev libboost-thread-dev libcoin-dev libeigen3-dev libgts-bin libgts-dev libkdtree++-dev libmedc-dev libocct-data-exchange-dev libocct-ocaf-dev libocct-visualization-dev libopencv-dev libproj-dev libpyside2-dev libqt5opengl5-dev libqt5svg5-dev libqt5webkit5-dev libqt5x11extras5-dev libqt5xmlpatterns5-dev libshiboken2-dev libspnav-dev libvtk7-dev libx11-dev libxerces-c-dev libzipios++-dev occt-draw pyside2-tools python3-dev python3-matplotlib python3-pivy python3-ply python3-pyside2.qtcore python3-pyside2.qtgui python3-pyside2.qtsvg python3-pyside2.qtwidgets qtbase5-dev qttools5-dev swig 
	
	python3-pyside2uic

	git clone https://github.com/FreeCAD/FreeCAD.git freecad-source

	mkdir freecad-build
	cd freecad-build
	cmake ../freecad-source -DBUILD_QT5=ON -DPYTHON_EXECUTABLE=/usr/bin/python3 -GNinja

## 入门

	点击实体图标, 创建实体

	点击创建草图, 创建草图

	选择一个工作平面

	ps: 首选项中, "草绘", 勾选 "显示网络", 勾选 "网络捕获" 和 "自动约束"

## 绘制 PCB 外壳

	创建实体, 添加一张草绘, 选择XY平面

	先画一个矩形，它将自动拥有水平约束和垂直约束

	给矩形的两个长边添加相对于x轴的对称约束
	给矩形的两个宽边添加相对于y轴的对称约束

	添加长和宽的长度约束, 长: 30mm, 宽: 30mm，完成草图

	添加凸台，设置高度为2mm
	添加倒圆角，设置圆角半径：0.5mm

	
	切换到顶视图, 选中底座的上平面，新建草图

	重复上面草图中的操作, 添加一个长和宽分别为26mm和26mm的方形, 完成草图

	添加凸台，设置高度为5mm


	选中最顶部的面, 创建草绘，切换到辅助线模式 （蓝色的是辅助线模式, 白色的是正常模式）

	用前面的方式在草绘上话一个长和宽分别是24mm和24mm的方形, 用于挖孔

	切换到正常绘图模式

	在4条辅助线上各画一条线段, 并用画圆弧把每条线段连起来, 共形成4条圆弧

	然后把4条线段和4条圆弧组合到一起









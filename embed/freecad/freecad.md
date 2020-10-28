# freecad 使用笔记

## 源码编译

	sudo apt build-dep freecad
	sudo apt install libqt5xmlpatterns5-dev

	git clone https://github.com/FreeCAD/FreeCAD.git freecad-source

	mkdir freecad-build
	cd freecad-build
	cmake ../freecad-source -DBUILD_QT5=ON -DPYTHON_EXECUTABLE=/usr/bin/python3 -GNinja

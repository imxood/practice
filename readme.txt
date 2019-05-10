
All MSBuild C++ projects can now #include any installed libraries.
Linking will be handled automatically.
Installing new libraries will make them instantly available.

CMake projects should use: "-DCMAKE_TOOLCHAIN_FILE=E:/Develop/source/vcpkg/scripts/buildsystems/vcpkg.cmake"



cmake_minimum_required(VERSION 3.0.0)
project(hello VERSION 0.1.0)

include(CTest)
enable_testing()

find_package(Tesseract REQUIRED)

add_executable(hello main.cpp)
target_link_libraries(hello PRIVATE libtesseract)

message(STATUS "CMAKE_BINARY_DIR: ${CMAKE_BINARY_DIR}  PROJECT_SOURCE_DIR: ${PROJECT_SOURCE_DIR}")

install(
	DIRECTORY ${CMAKE_SOURCE_DIR}/images ${CMAKE_SOURCE_DIR}/tessdata DESTINATION ${CMAKE_BINARY_DIR}
)

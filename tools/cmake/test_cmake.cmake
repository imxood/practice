
# 定义一个全局(<GLOBAL | DIRECTORY | TARGET | SOURCE | TEST | VARIABLE | CACHED_VARIABLE>)的属性名"ZEPHYR_LIBS"
define_property(
    GLOBAL PROPERTY ZEPHYR_LIBS
    BRIEF_DOCS "Global list of all Zephyr CMake libs that should be linked in"
    FULL_DOCS  "Global list of all Zephyr CMake libs that should be linked in. zephyr_library() appends libs to this list."
)
# 设置属性值
set_property(GLOBAL PROPERTY ZEPHYR_LIBS "zzz")
# 获取属性值
get_property(zephyr_libs GLOBAL PROPERTY ZEPHYR_LIBS)
message(STATUS "zephyr_libs: '${zephyr_libs}'")



# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.13.1)

set(DTC_OVERLAY_FILE ${CMAKE_CURRENT_SOURCE_DIR}/dts/stm32.overlay.dts)

include($ENV{ZEPHYR_BASE}/cmake/app/boilerplate.cmake NO_POLICY_SCOPE)
project(hello_world)

file(
    GLOB SOURCE_LIST
    src/main.c
    init/pinmux.c
    tests/kernel/sleep/test.c
    tests/kernel/sleep/usleep.c
)

target_sources(app PRIVATE ${SOURCE_LIST})

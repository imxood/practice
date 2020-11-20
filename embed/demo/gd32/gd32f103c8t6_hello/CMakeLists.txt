cmake_minimum_required(VERSION 3.12)

set(CMAKE_SYSTEM_NAME      Generic)
set(CMAKE_SYSTEM_VERSION   1)
set(CMAKE_SYSTEM_PROCESSOR arm)

set(CMAKE_C_COMPILER			arm-none-eabi-gcc)
set(CMAKE_CXX_COMPILER			arm-none-eabi-g++)
set(CMAKE_ASM_COMPILER			arm-none-eabi-gcc)
set(CMAKE_OBJCOPY				arm-none-eabi-objcopy)
set(CMAKE_OBJDUMP				arm-none-eabi-objdump)
set(CMAKE_SIZE_UTIL				arm-none-eabi-size)

set(CPU  "-mcpu=cortex-m3")
# set(FPU  "-mfpu=fpv4-sp-d16")
# set(FLOAT-ABI  "-mfloat-abi=hard")
set(FPU  "")
set(FLOAT-ABI  "")
set(MCU  "${CPU} -mthumb  ${FPU} ${FLOAT-ABI}")

set(LDSCRIPT "${CMAKE_SOURCE_DIR}/board/GD32F103C8T6.ld")

set(CMAKE_C_FLAGS "${MCU} -Og -Wno-unused-function -Wall -fdata-sections -ffunction-sections -MMD -MP" CACHE INTERNAL "c compiler flags")
set(CMAKE_CXX_FLAGS "${MCU} -Og -Wall -fdata-sections -ffunction-sections -MMD -MP" CACHE INTERNAL "cxx compiler flags")
set(CMAKE_ASM_FLAGS "-Og -Wall -fdata-sections -ffunction-sections" CACHE INTERNAL "asm compiler flags")
set(CMAKE_EXE_LINKER_FLAGS "-specs=nano.specs -specs=nosys.specs -lm -T${LDSCRIPT} -Wl,-Map=output.map,--cref -Wl,--gc-sections" CACHE INTERNAL "exe link flags")


set(CMAKE_C_FLAGS_DEBUG "-g -gdwarf-2")
set(CMAKE_ASM_FLAGS_DEBUG "-g -gdwarf-2")

set(CMAKE_C_FLAGS_RELEASE "-O3")
set(CMAKE_ASM_FLAGS_RELEASE "-O3")

project(gd32f103c8t6_hello)
ENABLE_LANGUAGE(ASM C CXX)

set(CMAKE_BUILD_TYPE Debug)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON CACHE INTERNAL "export compile commands")

aux_source_directory(Libraries/GD32F10x_standard_peripheral/Source GD32_LIB_SRCS)

set(SOURCES
	applications/main.c
	${GD32_LIB_SRCS}
	Libraries/CMSIS/GD/GD32F10x/Source/system_gd32f10x.c
	board/startup_gd32f10x_md.s
)
set(EXECUTABLE ${PROJECT_NAME}.elf)

add_executable(${EXECUTABLE} ${SOURCES})

target_include_directories(${EXECUTABLE} PRIVATE
	Libraries/CMSIS
	Libraries/CMSIS/Include
	Libraries/CMSIS/GD/GD32F10x/Include
	Libraries/GD32F10x_standard_peripheral/Include
	board
	applications
)

target_compile_definitions(${EXECUTABLE} PRIVATE
	-DGD32F10X_MD
)

add_custom_command(
	TARGET ${EXECUTABLE} POST_BUILD
	COMMAND ${CMAKE_SIZE_UTIL} ${EXECUTABLE}
	COMMAND ${CMAKE_OBJCOPY} -O ihex ${EXECUTABLE} ${PROJECT_NAME}.hex
	COMMAND ${CMAKE_OBJCOPY} -O binary ${EXECUTABLE} ${PROJECT_NAME}.bin
)

add_custom_target(flash
	DEPENDS ${EXECUTABLE}
	COMMAND openocd -f ${CMAKE_SOURCE_DIR}/board/openocd_gd32f1x.cfg
					-c \"program ${EXECUTABLE} 0x8000000 reset\; halt\; resume\; exit\"
)

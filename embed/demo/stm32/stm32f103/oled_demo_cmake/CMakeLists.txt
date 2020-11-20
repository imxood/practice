cmake_minimum_required(VERSION 3.12)

set(CMAKE_SYSTEM_NAME      Generic)
set(CMAKE_SYSTEM_VERSION   1)
set(CMAKE_SYSTEM_PROCESSOR arm)

set(CMAKE_C_COMPILER			arm-none-eabi-gcc)
set(CMAKE_ASM_COMPILER			arm-none-eabi-gcc)
set(CMAKE_CXX_COMPILER			arm-none-eabi-g++)
set(CMAKE_OBJCOPY				arm-none-eabi-objcopy)
set(CMAKE_OBJDUMP				arm-none-eabi-objdump)
set(CMAKE_SIZE_UTIL				arm-none-eabi-size)

set(CPU  "-mcpu=cortex-m3")
# set(FPU  "-mfpu=fpv4-sp-d16")
# set(FLOAT-ABI  "-mfloat-abi=hard")
set(FPU  "")
set(FLOAT-ABI  "")
set(MCU  "${CPU} -mthumb  ${FPU} ${FLOAT-ABI}")

set(LDSCRIPT "${CMAKE_SOURCE_DIR}/STM32F103C8Tx_FLASH.ld")

set(CMAKE_C_FLAGS "${MCU} -Og -Wno-unused-function -Wall -fdata-sections -ffunction-sections -MMD -MP" CACHE INTERNAL "c compiler flags")
set(CMAKE_CXX_FLAGS "${MCU} -Og -Wall -fdata-sections -ffunction-sections -MMD -MP" CACHE INTERNAL "cxx compiler flags")
set(CMAKE_ASM_FLAGS "-Og -Wall -fdata-sections -ffunction-sections" CACHE INTERNAL "asm compiler flags")
set(CMAKE_EXE_LINKER_FLAGS "-specs=nano.specs -specs=nosys.specs -lm -T${LDSCRIPT} -Wl,-Map=output.map,--cref -Wl,--gc-sections" CACHE INTERNAL "exe link flags")


set(CMAKE_C_FLAGS_DEBUG "-g -gdwarf-2")
set(CMAKE_ASM_FLAGS_DEBUG "-g -gdwarf-2")

set(CMAKE_C_FLAGS_RELEASE "-O3")
set(CMAKE_ASM_FLAGS_RELEASE "-O3")

project(f103c8t6_hello)
ENABLE_LANGUAGE(ASM C CXX)

set(CMAKE_BUILD_TYPE Debug)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON CACHE INTERNAL "export compile commands")

file(GLOB U8G2_SRCS Libs/u8g2/src/*.c)

set(SOURCES
	${U8G2_SRCS}
	Libs/myfont/myfont.c
	Src/u8g2.c
	Src/main.c
	Src/stm32f1xx_it.c
	Src/stm32f1xx_hal_msp.c
	Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_gpio_ex.c
	Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_i2c.c
	Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal.c
	Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_rcc.c
	Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_rcc_ex.c
	Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_gpio.c
	Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_dma.c
	Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_cortex.c
	Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_pwr.c
	Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_flash.c
	Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_flash_ex.c
	Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_exti.c
	Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_tim.c
	Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_tim_ex.c
	Src/system_stm32f1xx.c
	Src/gpio.c
	Src/i2c.c
	startup_stm32f103xb.s
)
set(EXECUTABLE ${PROJECT_NAME}.elf)

add_executable(${EXECUTABLE} ${SOURCES})

target_include_directories(${EXECUTABLE} PRIVATE
	Libs/u8g2/inc
	Libs/myfont
	Inc
	Drivers/STM32F1xx_HAL_Driver/Inc
	Drivers/STM32F1xx_HAL_Driver/Inc/Legacy
	Drivers/CMSIS/Device/ST/STM32F1xx/Include
	Drivers/CMSIS/Include
)

target_compile_definitions(${EXECUTABLE} PRIVATE
	-DUSE_HAL_DRIVER
	-DSTM32F103xB
)

add_custom_command(
	TARGET ${EXECUTABLE} POST_BUILD
	COMMAND ${CMAKE_SIZE_UTIL} ${EXECUTABLE}
	COMMAND ${CMAKE_OBJCOPY} -O ihex ${EXECUTABLE} ${PROJECT_NAME}.hex
	COMMAND ${CMAKE_OBJCOPY} -O binary ${EXECUTABLE} ${PROJECT_NAME}.bin
)

add_custom_target(flash
	DEPENDS ${EXECUTABLE}
	COMMAND openocd -f ${CMAKE_SOURCE_DIR}/openocd_stm32f1x.cfg
					-c \"program ${EXECUTABLE} 0x8000000 reset exit\"
)

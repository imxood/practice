/*
 * Copyright (c) 2018 Yong Jin
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <kernel.h>
#include <device.h>
#include <init.h>
#include <pinmux.h>
#include <sys_io.h>

#include <pinmux/stm32/pinmux_stm32.h>

/* pin assignments for STM32F769I-DISCO board */
static const struct pin_config pinconf[] = {
#ifdef CONFIG_UART_3
	{STM32_PIN_PB10, STM32F7_PINMUX_FUNC_PB10_USART3_TX},
	{STM32_PIN_PB11, STM32F7_PINMUX_FUNC_PB11_USART3_RX},
#endif
};

static int pinmux_stm32_init(struct device *port)
{
	ARG_UNUSED(port);

	stm32_setup_pins(pinconf, ARRAY_SIZE(pinconf));

	return 0;
}

SYS_INIT(pinmux_stm32_init, PRE_KERNEL_1, CONFIG_PINMUX_STM32_DEVICE_INITIALIZATION_PRIORITY);

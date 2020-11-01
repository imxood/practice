#include "main.h"
#include <u8g2.h>
#include <myfont.h>
#include <stdio.h>

static u8g2_t u8g2;
extern I2C_HandleTypeDef hi2c1;

void delay_us(uint32_t time)
{
	uint32_t i = 8 * time;
	while (i--)
		;
}

uint8_t u8x8_byte_hw_i2c(u8x8_t *u8x8, uint8_t msg, uint8_t arg_int, void *arg_ptr)
{
	static uint8_t buffer[32]; /* u8g2/u8x8 will never send more than 32 bytes */
	static uint8_t buf_idx;
	uint8_t *data;

	switch (msg)
	{
	case U8X8_MSG_BYTE_SEND:
		data = (uint8_t *)arg_ptr;
		while (arg_int > 0)
		{
			buffer[buf_idx++] = *data;
			data++;
			arg_int--;
		}
		break;
	case U8X8_MSG_BYTE_INIT:
		break;
	case U8X8_MSG_BYTE_SET_DC:
		break;
	case U8X8_MSG_BYTE_START_TRANSFER:
		buf_idx = 0;
		break;
	case U8X8_MSG_BYTE_END_TRANSFER:
		if (HAL_I2C_Master_Transmit(&hi2c1, u8x8_GetI2CAddress(u8x8), buffer, buf_idx, 10) != HAL_OK)
		{
			return 0;
		}
		break;
	default:
		return 0;
	}
	return 1;
}

uint8_t u8x8_stm32_gpio_and_delay(u8x8_t *u8x8, uint8_t msg, uint8_t arg_int, void *arg_ptr)
{
	switch (msg)
	{
	case U8X8_MSG_DELAY_100NANO: // delay arg_int * 100 nano seconds
		__NOP();
		break;
	case U8X8_MSG_DELAY_10MICRO: // delay arg_int * 10 micro seconds
		for (uint16_t n = 0; n < 320; n++)
		{
			__NOP();
		}
		break;
	case U8X8_MSG_DELAY_MILLI: // delay arg_int * 1 milli second
		HAL_Delay(1);
		break;
	case U8X8_MSG_DELAY_I2C: // arg_int is the I2C speed in 100KHz, e.g. 4 = 400 KHz
		delay_us(5);
		break;					  // arg_int=1: delay by 5us, arg_int = 4: delay by 1.25us
	case U8X8_MSG_GPIO_I2C_CLOCK: // arg_int=0: Output low at I2C clock pin
		break;					  // arg_int=1: Input dir with pullup high for I2C clock pin
	case U8X8_MSG_GPIO_I2C_DATA:  // arg_int=0: Output low at I2C data pin
		break;					  // arg_int=1: Input dir with pullup high for I2C data pin
	case U8X8_MSG_GPIO_MENU_SELECT:
		u8x8_SetGPIOResult(u8x8, /* get menu select pin state */ 0);
		break;
	case U8X8_MSG_GPIO_MENU_NEXT:
		u8x8_SetGPIOResult(u8x8, /* get menu next pin state */ 0);
		break;
	case U8X8_MSG_GPIO_MENU_PREV:
		u8x8_SetGPIOResult(u8x8, /* get menu prev pin state */ 0);
		break;
	case U8X8_MSG_GPIO_MENU_HOME:
		u8x8_SetGPIOResult(u8x8, /* get menu home pin state */ 0);
		break;
	default:
		u8x8_SetGPIOResult(u8x8, 1); // default return value
		break;
	}
	return 1;
}

void draw(u8g2_t *u8g2)
{
	static int temp = 1;
	static char temp_str[10] = {0};
	u8g2_ClearBuffer(u8g2);

	u8g2_SetFontDirection(u8g2, 0);
	u8g2_SetFontMode(u8g2, 1);

	u8g2_SetFont(u8g2, u8g2_font_wqy12_myfont);
	u8g2_DrawUTF8(u8g2, 5, 25, "温度:");

	u8g2_SetFont(u8g2, u8g2_font_6x10_tf);

	u8g2_SetFont(u8g2, u8g2_font_inb21_mf);

	sprintf(temp_str, "%d\0", temp);
	if (temp < 10)
		u8g2_DrawStr(u8g2, 71, 45, temp_str);
	else
		u8g2_DrawStr(u8g2, 50, 45, temp_str);


	u8g2_DrawCircle(u8g2, 99, 24, 3, U8G2_DRAW_ALL);
	u8g2_DrawStr(u8g2, 100, 45, "C");

	if (++temp >= 100)
	{
		temp = 0;
	}
	// u8g2_SendBuffer(u8g2);
}

void u8g2_init(void)
{
	/* init u8g2 结构体 */
	u8g2_Setup_ssd1306_i2c_128x64_noname_f(&u8g2, U8G2_R0, u8x8_byte_hw_i2c, u8x8_stm32_gpio_and_delay);

	/* 设置 i2c slave 地址*/
	// u8g2_SetI2CAddress(&u8g2, 0x78);

	u8g2_InitDisplay(&u8g2);
	u8g2_SetPowerSave(&u8g2, 0);
	// u8g2_ClearDisplay(&u8g2);
}

void u8g2_loop(void)
{
	/* usage 1 */
	u8g2_ClearBuffer(&u8g2);
	draw(&u8g2);
	// u8g2_DrawCircle(&u8g2, 64, 32, 30, U8G2_DRAW_ALL);
	u8g2_SendBuffer(&u8g2);

	/* usage 2 */
	// u8g2_FirstPage(&u8g2);
	// do
	// {
	// 	draw(&u8g2);
	// } while (u8g2_NextPage(&u8g2));

	HAL_Delay(500);
}

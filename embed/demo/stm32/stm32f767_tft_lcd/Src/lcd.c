#include "main.h"
#include <stdio.h>

#define LCD_WIDTH 240
#define LCD_HIGHT 320

typedef struct
{
	volatile uint16_t CMD;
	volatile uint16_t DATA;
} LCD_Type_Def;

#define LCD_BASE ((uint32_t)0x6007FFFE)
#define LCD ((LCD_Type_Def *)LCD_BASE)

/* define LCD commands */
#define SET_X_CMD 0x2A
#define SET_Y_CMD 0x2B
#define WRAM_CMD 0x2C
#define RRAM_CMD 0x2E
#define RID_CMD 0xD3

/* define LCD colors */
#define LIGHTBLUE 0X7D7C //浅蓝色
#define DARKBLUE 0X01CF	 //深蓝色
#define GRAYBLUE 0X5458	 //灰蓝色

extern SRAM_HandleTypeDef hsram1;
static uint16_t lcd_device_id;

static inline void LCD_WriteCmd(volatile uint16_t cmd)
{
	LCD->CMD = cmd;
}

static inline void LCD_WriteData(volatile uint16_t data)
{
	LCD->DATA = data;
}

static inline uint16_t LCD_ReadDATA(void)
{
	return LCD->DATA;
}

/**
 * 设置当前位置
 */
void LCD_SetCursor(uint16_t x, uint16_t y)
{
	LCD_WriteCmd(SET_X_CMD);
	LCD_WriteData(x >> 8);
	LCD_WriteData(x & 0xFF);

	LCD_WriteCmd(SET_Y_CMD);
	LCD_WriteData(y >> 8);
	LCD_WriteData(y & 0xFF);
}

/**
 * 读点
 */
uint32_t LCD_ReadPoint(uint16_t x, uint16_t y)
{
	uint16_t r = 0, g = 0, b = 0;
	if (x >= LCD_WIDTH || y >= LCD_HIGHT)
		return 0;
	LCD_SetCursor(x, y);
	LCD_WriteCmd(RRAM_CMD);
	r = LCD_ReadDATA(); // dummy Read
	r = LCD_ReadDATA();
	b = LCD_ReadDATA();
	g = (r & 0xFF) << 8;									   // 第一次读取的是RG的值,R在前,G在后,各占8位
	return (((r >> 11) << 11) | ((g >> 10) << 5) | (b >> 11)); //公式转换一下
}

/**
 * 画点
 */
void LCD_PaintPoint(uint16_t x, uint16_t y, uint32_t color)
{
	LCD_SetCursor(x, y);
	LCD_WriteCmd(WRAM_CMD);
	LCD_WriteData(color);
}

/**
 * 在指定的区域填充单一颜色
 */
void LCD_Fill(uint16_t x1, uint16_t y1, uint16_t x2, uint16_t y2, uint16_t color)
{
	uint16_t i, j;
	for (i = y1; i <= y2; i++)
	{
		LCD_SetCursor(x1, i);
		LCD_WriteCmd(WRAM_CMD);
		for (j = x1; j <= x2; j++)
			LCD_WriteData(color);
	}
}

/**
 * 在指定的区域填充单一颜色
 */
void LCD_FillColor(uint16_t x1, uint16_t y1, uint16_t x2, uint16_t y2, uint16_t *color)
{
	uint16_t i, j;
	uint16_t w, h;
	w = x2 - x1 + 1;
	h = y2 - y1 + 1;
	for (i = 0; i < h; i++)
	{
		LCD_SetCursor(x1, y1 + i);
		LCD_WriteCmd(WRAM_CMD);
		for (j = 0; j < w; j++)
			LCD_WriteData(color[i * w + j]);
	}
}

/**
 * 点亮背光
 */
void LCD_Led(uint8_t set)
{
	set ? HAL_GPIO_WritePin(GPIOB, GPIO_PIN_5, GPIO_PIN_SET) : HAL_GPIO_WritePin(GPIOB, GPIO_PIN_5, GPIO_PIN_RESET);
}

/**
 * LCD 初始化序列
 */
void LCD_Init(void)
{
	HAL_Delay(50);
	LCD_WriteCmd(RID_CMD);
	lcd_device_id = LCD_ReadDATA(); // dummy
	lcd_device_id = LCD_ReadDATA(); // 0x00
	lcd_device_id = LCD_ReadDATA(); // 0x93
	lcd_device_id <<= 8;
	lcd_device_id |= LCD_ReadDATA(); // 0x41

	LCD_WriteCmd(0xCF);
	LCD_WriteData(0x00);
	LCD_WriteData(0xC1);
	LCD_WriteData(0X30);
	LCD_WriteCmd(0xED);
	LCD_WriteData(0x64);
	LCD_WriteData(0x03);
	LCD_WriteData(0X12);
	LCD_WriteData(0X81);
	LCD_WriteCmd(0xE8);
	LCD_WriteData(0x85);
	LCD_WriteData(0x10);
	LCD_WriteData(0x7A);
	LCD_WriteCmd(0xCB);
	LCD_WriteData(0x39);
	LCD_WriteData(0x2C);
	LCD_WriteData(0x00);
	LCD_WriteData(0x34);
	LCD_WriteData(0x02);
	LCD_WriteCmd(0xF7);
	LCD_WriteData(0x20);
	LCD_WriteCmd(0xEA);
	LCD_WriteData(0x00);
	LCD_WriteData(0x00);
	LCD_WriteCmd(0xC0);	 // Power control
	LCD_WriteData(0x1B); // VRH[5:0]
	LCD_WriteCmd(0xC1);	 // Power control
	LCD_WriteData(0x01); // SAP[2:0];BT[3:0]
	LCD_WriteCmd(0xC5);	 // VCM control
	LCD_WriteData(0x30); // 3F
	LCD_WriteData(0x30); // 3C
	LCD_WriteCmd(0xC7);	 // VCM control2
	LCD_WriteData(0XB7);
	LCD_WriteCmd(0x36); // Memory Access Control
	LCD_WriteData(0x48);
	LCD_WriteCmd(0x3A);
	LCD_WriteData(0x55);
	LCD_WriteCmd(0xB1);
	LCD_WriteData(0x00);
	LCD_WriteData(0x1A);
	LCD_WriteCmd(0xB6); // Display Function Control
	LCD_WriteData(0x0A);
	LCD_WriteData(0xA2);
	LCD_WriteCmd(0xF2); // 3Gamma Function Disable
	LCD_WriteData(0x00);
	LCD_WriteCmd(0x26); // Gamma curve selected
	LCD_WriteData(0x01);
	LCD_WriteCmd(0xE0); // Set Gamma
	LCD_WriteData(0x0F);
	LCD_WriteData(0x2A);
	LCD_WriteData(0x28);
	LCD_WriteData(0x08);
	LCD_WriteData(0x0E);
	LCD_WriteData(0x08);
	LCD_WriteData(0x54);
	LCD_WriteData(0XA9);
	LCD_WriteData(0x43);
	LCD_WriteData(0x0A);
	LCD_WriteData(0x0F);
	LCD_WriteData(0x00);
	LCD_WriteData(0x00);
	LCD_WriteData(0x00);
	LCD_WriteData(0x00);
	LCD_WriteCmd(0XE1); // Set Gamma
	LCD_WriteData(0x00);
	LCD_WriteData(0x15);
	LCD_WriteData(0x17);
	LCD_WriteData(0x07);
	LCD_WriteData(0x11);
	LCD_WriteData(0x06);
	LCD_WriteData(0x2B);
	LCD_WriteData(0x56);
	LCD_WriteData(0x3C);
	LCD_WriteData(0x05);
	LCD_WriteData(0x10);
	LCD_WriteData(0x0F);
	LCD_WriteData(0x3F);
	LCD_WriteData(0x3F);
	LCD_WriteData(0x0F);
	LCD_WriteCmd(0x2B);
	LCD_WriteData(0x00);
	LCD_WriteData(0x00);
	LCD_WriteData(0x01);
	LCD_WriteData(0x3f);
	LCD_WriteCmd(0x2A);
	LCD_WriteData(0x00);
	LCD_WriteData(0x00);
	LCD_WriteData(0x00);
	LCD_WriteData(0xef);
	LCD_WriteCmd(0x11); // Exit Sleep
	HAL_Delay(120);
	LCD_WriteCmd(0x29); // display on
}

void lcd_init(void)
{
	LCD_Init();
	LCD_Led(1);										// 点亮屏幕
	LCD_Fill(0, 0, LCD_WIDTH, LCD_HIGHT, DARKBLUE); // 从(0, 0)到(LCD_WIDTH, LCD_HIGHT)的位置填充单一的深蓝色
}

# 结合例子对u8g2lib分析

	U8G2_SSD1306_128X64_NONAME_F_SW_I2C u8g2(U8G2_R0, /* clock=*/ SCL, /* data=*/ SDA, /* reset=*/ U8X8_PIN_NONE);

	在Arduino/libraries/U8g2/src/U8g2lib.h中

	定义了 U8G2_SSD1306_128X64_NONAME_F_SW_I2C 类:
		u8g2_Setup_ssd1306_i2c_128x64_noname_f(&u8g2, rotation, u8x8_byte_arduino_sw_i2c, u8x8_gpio_and_delay_arduino);
		u8x8_SetPin_SW_I2C(getU8x8(), clock,  data,  reset);

	找到 u8x8_byte_arduino_sw_i2c 的定义:
		该函数有好几处定义，不过不需要知道具体的， 关键一点是 "sw"， 根据 clock 和 data 引脚， u8x8_gpio_and_delay_arduino 这个函数定义了对 gpio 的初始化和 delay 的实现, 于是很容易实现软件模拟i2c时序

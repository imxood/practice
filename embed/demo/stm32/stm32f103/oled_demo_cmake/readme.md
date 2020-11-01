# oled demo

	stm32f103c8t6

	硬件i2c:
		PB6 I2C1_SCL
		PB7 I2C1_SDA

	使用u8g2库

		https://github.com/olikraus/u8g2

		u8g2 api, 在调用 u8g2 画图 api 前应该先阅读:
			https://github.com/olikraus/u8g2/wiki/u8g2reference

		u8g2 默认的库包含的字体可以在这里查看:
			https://github.com/olikraus/u8g2/wiki/fntlistall
			https://github.com/olikraus/u8g2/wiki/fntlist8x8

			https://github.com/olikraus/u8g2/wiki/internal

		文泉驿点阵宋体
			https://github.com/larryli/u8g2_wqy

	生成u8g2字体:
		需要的是:
			1. 一个map文件, 可以使用 chineses2map.py, 这个map文件中包含所有文字对应的编码信息
			2. 一个bdf文件, 使用u8g2_wqy中提供的
			3. bdfconv, 由u8g2/tools提供

		把需要的汉字放在 chineses2map.py 中的 chineses 变量中, 执行:
			python chineses2map.py

		调用 bdfconv 程序, 需要 make 编译:
			./Libs/u8g2/tools/font/bdfconv/bdfconv -b 0 -f 1 -M myfont.map -n u8g2_font_wqy12_t_myfont -o _u8g2_font_wqy12_t_myfont.c Libs/u8g2_wqy/bdf/wenquanyi_9pt.bdf

		生成的 _u8g2_font_wqy12_t_myfont.c 即是所需的字体信息

		添加文件:
			myfont.h
			myfont.c

	需要实现的是:

		u8g2_Setup_ssd1306_i2c_128x64_noname_f(&u8g2, U8G2_R0, u8x8_byte_hw_i2c, u8x8_stm32_gpio_and_delay);

		这里的 u8g2_Setup_ssd1306_i2c_128x64_noname_f 函数要选择正确, 这个是i2c的, 如果用软件i2c或者是spi, 或者是别的接口, 需要找出合适的
		u8x8_byte_hw_i2c 这个是实现了 硬件i2c 的通信接口
		u8x8_stm32_gpio_and_delay 是需要实现的 gpio 和 delay 相关的函数


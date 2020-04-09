# openocd笔记

openocd -f board/stm32f7discovery.cfg

telnet localhost 4444

program <filename> [address] [verify] [reset] [exit], 写可执行程序到flash上, 只有binary images才需要address

    ex: program output.bin 0x08000000 reset; halt; reg; resume; exit

halt, 进入挂起状态

reg [REG [value]] , 查看或设置寄存器, 可能需要在halt状态下

resume, 恢复到当前代码段

reset [run|halt|init], 重置, 进入特定状态, 默认是run

reg, 查看寄存器内容, 在halt状态下才会显示内容


## gdb

```
arm-zephyr-eabi-gdb /home/imxood/develop/code/sources/zephyrproject/zephyr/builds/zephyr/zephyr.elf

GDB Shell:

Common Command:
    l, list source
    c, continue
    b, 加断点
        b 16, 在当前第16行加断点
        b i=1, 在i=1时加断点
        b main, 在main函数入口添加断点
    i, info
        i b, 查看断点信息
    d, delet
        d break, 删除所有的断点
        d break 1, 删除序号为1的断点
    s, step
    n, next
    u, util
        u 16, 即运行到第16行
    finish, 完成并跳出当前的子函数
    p, print
    display, 自动显示变量的值
        display variable1, 每当执行停止时会自动显示变量的值
    bt, backtrace
    -, 进入tui模式
    Ctrl + X + A, 退出tui模式
Monitor Command:
	monitor help, 查看所有monitor支持的命令
	monitor reset, 重置设备
	monitor halt, 暂停cpu
	monitor reg, 查看所有寄存器内容
	monitor reg PC, 查看PC寄存器内容

烧写程序:
gdb BinFile
target remote localhost:3333
load
monitor reset

## Makefile
```sh
$(VariableName)

自动化变量:
    $@ 表示目标集
    $< 表示依赖集

@echo "正在编译"

两行命令加";"

命令前加"-",报错继续执行,否则停止
make的"-k", 某个规则失败, 其它规则继续执行

x = foo, x会受后面影响
x := foo, x不受后面影响
FOO ?= bar, 若果FOO未被定义,则值为bar, 否则不处理
objects += another.o, 追加

$(foo:.o=.c), 把结尾是.o的字符串替换为.c结尾
$(foo:%.o=%.c), 同上
$($(x)), 把变量的值当做变量

override <variable> = <value>
override <variable> := <value>

```

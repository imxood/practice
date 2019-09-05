.PHONY: all clean asm

all: asm

asm:
	nasm -felf64 hello.asm && ld hello.o -o hello.bin
	nasm -felf64 puts.asm && gcc -no-pie puts.o -o puts.bin

clean:
	rm -f *.o *.s *.lst *.bin a.out

.PHONY: all clean asm

all: asm

asm:
	nasm -felf64 hello.nasm && ld hello.o -o hello.bin
	nasm -felf64 puts.nasm && gcc -no-pie puts.o -o puts.bin
	nasm -felf64 fib.nasm && gcc -no-pie fib.o -o fib.bin

	nasm -felf64 maxofthree.nasm && gcc -no-pie maxofthree.o callmaxofthree.c -o maxofthree.bin

	nasm -felf64 -l test_addr.lst test_addr.nasm && gcc -no-pie test_addr.o -o test_addr.bin

clean:
	rm -f *.o *.s *.lst *.bin a.out

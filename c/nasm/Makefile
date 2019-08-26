all:
	nasm -felf64 *.asm
	gcc -m64 -c -g *.c
	ld -m elf_x86_64 *.o

asm:
	nasm -felf64 *.asm
	gcc -m64 -c -g *.c
	gcc *.o -o a.out
	objdump -d a.out > asm.lst

clean:
	rm -f *.o *.s *.lst a.out

.PHONY: all clean asm

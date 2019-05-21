#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

int main(int argc, char** argv)
{
	uint32_t a1 = 1, a2 = 2;
	int c = abs(a1 - a2);
	printf("c: %d\n", c);
	return 0;
}

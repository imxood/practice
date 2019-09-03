#include <stdio.h>
#include <stdlib.h>

int main(int argc, char const *argv[])
{
	char *name = "abc\0def";
	printf("name: %s, size: %d\n", name, strlen(name));

	char buf[512] = {0};
	sprintf(buf, "%d\012345", 123);

	printf("buf: %s, size: %d\n", buf, strlen(buf));
	return 0;
}

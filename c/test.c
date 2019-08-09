#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>

static char CASE_NAME_BUFFER[128];
static char CASE_NAME_ARGS[128];

static char *INT_CAT(int argc, ...)
{
	static volatile unsigned char pos = 0;

	char *init_buffer = CASE_NAME_ARGS + pos;
	char *buffer = init_buffer;

	char *arg = NULL;

	va_list valist;
	va_start(valist, argc);

	for (int i = 0; i < argc; i++)
	{
		int arg = va_arg(valist, int);
		sprintf(buffer, "%d", arg);
		pos += strlen(buffer);
		buffer += strlen(buffer);
		*buffer = '_';
		buffer++;
	}

	buffer--;
	*buffer = '\0';

	return init_buffer;
}

static char *CASE_NAME(int argc, ...)
{
	char *buffer = CASE_NAME_BUFFER;
	char *arg = NULL;

	va_list valist;
	va_start(valist, argc);

	for (int i = 0; i < argc; i++)
	{
		char *arg = va_arg(valist, char *);
		strcpy(buffer, arg);
		buffer += strlen(arg);
		*buffer = '_';
		buffer++;
	}

	buffer--;
	*buffer = '\0';

	return CASE_NAME_BUFFER;
}

int main(int argc, char const *argv[])
{
	char *name = NULL;

	name = INT_CAT(2, 11, 22);
	printf("%s\n", name);

	name = INT_CAT(4, 1, 2, 3, 4);
	printf("%s\n", name);

	name = CASE_NAME(3, "hello", "world", "1");
	printf("%s\n", name);

	name = CASE_NAME(3, "hello", "world", INT_CAT(2, 1, 2));
	printf("%s\n", name);


	return 0;
}

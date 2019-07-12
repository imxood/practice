
#include <stdio.h>
#include <stdint.h>

struct test1 {
    char c;
    int i;
};

struct __attribute__ ((__packed__)) test2 {
    char c;
    int i;
};

struct test3 {
    char c[10];
    int i;
};

struct __attribute__ ((__packed__)) test4 {
    char c[10];
    int i;
};

struct test5 {
	uint32_t cmd;

#define DATA_FRAME_SIZE 256
	uint8_t payload[DATA_FRAME_SIZE - 5];
	uint8_t len;
	uint8_t len1;
};

struct __attribute__ ((__packed__)) test6 {
	uint32_t cmd;

#define DATA_FRAME_SIZE 256
	uint8_t payload[DATA_FRAME_SIZE - 5];
	uint8_t len;
	uint8_t len1;
};

int main()
{
	printf("size of test1: %lu\n", sizeof(struct test1));

    printf("size of test2: %lu\n", sizeof(struct test2));

	printf("size of test3: %lu\n", sizeof(struct test3));

	printf("size of test4: %lu\n", sizeof(struct test4));

	printf("size of test5: %lu\n", sizeof(struct test5));

	printf("size of test6: %lu\n", sizeof(struct test6));

	return 0;
}

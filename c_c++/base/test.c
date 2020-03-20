#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

void test_struct()
{

	// #pragma pack(4)

	struct test1
	{
		char a[31];
		short b;
		char b_1;
		char b_2;
		char b_3;
		char b_4;
		int c;
		double d;
	};

	struct __attribute__((__packed__)) test2
	{
		char a[31];
		short b;
		char b_1;
		char b_2;
		char b_3;
		char b_4;
		int c;
		double d;
	};

	struct __attribute__((aligned(32))) test3
	{
		char a[31];
		short b;
		char b_1;
		char b_2;
		char b_3;
		char b_4;
		int c;
		double d;
	};

	printf("size of struct test1: %lu\n", sizeof(struct test1));

	printf("size of __packed__ struct test2: %lu\n", sizeof(struct test2));

	printf("size of aligned(16) struct test3: %lu\n", sizeof(struct test3));
}

void test_bitfield()
{
	struct __attribute__ ((aligned(64))) bit_field
	{
		uint8_t a : 4; /* 独占一个 uint8_t */
		uint8_t b : 5; /* 4+5 > 8, 从新的存储单元开始存放*/
		uint8_t : 3;   /* 空域, 5+3 = 8, 这个位域和前一个位域刚好填满一个存储单元*/
		uint32_t c : 3; /* 独占一个 uint32_t */
	};

	printf("size of bit_field: %lu\n", sizeof(struct bit_field));
}

int main(int argc, char const *argv[])
{

	test_struct();

	test_bitfield();

	return 0;
}

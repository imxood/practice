#include <stdio.h>
#include <getopt.h>

static int enable_add = 0;

/**
 * --add
 * --multiply ARG1, or, --multiply=ARG1
 * --subtract, or, --subtract ARG2
 */

static struct option long_options[] = {
	{"add", no_argument, &enable_add, 1},
	{"multiply", required_argument, NULL, 2},
	{"subtract", optional_argument, NULL, 3}
};

/**
 * -a
 * -m 10
 * -s or -s10, Note: no space!
 */
const char* short_options = "am:s::";

int main(int argc, char** argv)
{

	int option_index = 0;
	int opt;

	while((opt = getopt_long(argc, argv, short_options, long_options, &option_index)) != -1) {
		switch (opt) {
			case 0:
				printf("long option: --add");
				printf("\n\n");
				break;

			case 1:
				printf("long option: --multiply");
				if (optarg != NULL) {
					printf(" %s", optarg);
				}
				printf("\n\n");
				break;

			case 2:
				printf("long option: --subtract");
				if (optarg != NULL) {
					printf(" %s", optarg);
				}
				printf("\n\n");
				break;

			case 'a':
				printf("short option: -a\n\n");
				break;

			case 'm':
				printf("short option: -m %s\n\n", optarg);
				break;

			case 's':
				printf("short option: -s");
				if (optarg != NULL) {
					printf(" %s", optarg);
				}
				printf("\n\n");
				break;
		}
	}

	if (opt == -1) {
		printf("getopt_long return -1\n\n");
		return 0;
	}

	return 0;
}

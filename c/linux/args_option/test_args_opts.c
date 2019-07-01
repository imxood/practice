#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <getopt.h>

int main(int argc, char **argv)
{
	const char *short_options = "vhVo:";

	const struct option long_options[] = {
		{"verbose", optional_argument, NULL, 'v'},
		{"help", no_argument, NULL, 'h'},
		{"version", no_argument, NULL, 'V'},
		{"output", optional_argument, NULL, 'o'},
		{NULL, 0, NULL, 0}, /*Require daten do farray.*/
	};

	const usage = 	"-s SPEED               | --speed SPEED \n"
					"-m MODE                | --mode MODE \n"
					"-b BAUDRATE            | --baudrate BAUDRATE \n"
					"-f FRAME-DELAY-TIME_MS | --frame-delay FRAME-DELAY-TIME_MS \n"
					"-l LOOP_COUNT          | --loop LOOP_COUNT \n";

	int c;

	for (;;)
	{
		c = getopt_long(argc, argv, short_options, long_options, NULL);
		if (c == -1)
		{
			break;
		}
		switch (c)
		{
		case 'h':
			printf(usage);
			exit(0);

		case 'v':
			printf("set the program's log verbose...\n");
			break;

		case 'V':
			printf("The version is 0.1...\n");
			break;

		case 'o':
			printf("The output file is %s.\n", optarg);
			break;

		case '?':
			printf("Invalid option, abort the program.");
			exit(-1);

		default: //unexpected
			abort();
		}
	}

	printf("ret: %d\n", c);

	return 0;
}

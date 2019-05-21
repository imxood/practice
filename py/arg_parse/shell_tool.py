#!/usr/bin/env python3

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Build tool")
    parser.add_argument("--version", action='version', version='%(prog)s 1.0')
    parser.add_argument("-t", "--target", action='append')
    parser.add_argument("-c", action='append')
    parser.add_argument("-d", action='store_true')
    parser.add_argument('-v', '--verbose', action='count')
    parser.add_argument('-s')
    parser.add_argument('-a', nargs="?")
    return parser.parse_args()

if __name__ == "__main__":
    options = parse_arguments()
    print(options)

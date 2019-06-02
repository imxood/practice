#!/usr/bin/env python3
import os,sys
import argparse


log_file = None
VERBOSE = 1

if os.isatty(sys.stdout.fileno()):
    TERMINAL = True
    COLOR_NORMAL = '\033[0m'
    COLOR_RED = '\033[91m'
    COLOR_GREEN = '\033[92m'
    COLOR_YELLOW = '\033[93m'
    COLOR_BLUE = '\033[94m'
    COLOR_CYAN = '\033[96m'
else:
    TERMINAL = False
    COLOR_NORMAL = ''
    COLOR_RED = ''
    COLOR_GREEN = ''
    COLOR_YELLOW = ''
    COLOR_BLUE = ''
    COLOR_CYAN = ''

# Debug Functions
def log_info(what, color=COLOR_GREEN):
    sys.stdout.write(color + what + COLOR_NORMAL + "\n")
    sys.stdout.flush()
    if log_file:
        log_file.write(what + "\n")
        log_file.flush()

def log_print(what):
    log_info(what, COLOR_NORMAL)

def log_warn(what):
    log_info(what, COLOR_YELLOW)

def log_error(what):
    sys.stderr.write(COLOR_RED + what + COLOR_NORMAL + "\n")
    if log_file:
        log_file(what + "\n")
        log_file.flush()

def log_debug(what):
    if VERBOSE >= 1:
        log_info(what, COLOR_CYAN)


def log_verbose(what):
    if VERBOSE >= 2:
        log_info(what, COLOR_BLUE)

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

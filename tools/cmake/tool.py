#!/usr/bin/env python3

import os
import sys
import argparse as ap

RunEnv = {
    'SCRIPT_FILE': os.path.realpath(__file__),
    'SCRIPT_DIR': os.path.dirname(os.path.realpath(__file__))
}

WORKDIR = RunEnv['SCRIPT_DIR']
OUTPUT = '{}/output'.format(WORKDIR)

def clean():
    os.system('rm -rf {}'.format(OUTPUT))

def config():
    os.system('cmake -H{} -B{}'.format(WORKDIR, OUTPUT))

def exit(status=0, msg=''):
    if msg != '':
        print(msg)
    sys.exit()

def parse_args():
    parser = ap.ArgumentParser()
    parser.add_argument('-C', '--clean', action='store_true', help='clean output files')
    parser.add_argument('-c', '--config', action='store_true', help='config project')
    return parser


def _main():

    parser = parse_args()
    args = parser.parse_args()

    print(args)

    if args.clean:
        clean()

    if args.config:
        config()


if __name__ == "__main__":
    _main()

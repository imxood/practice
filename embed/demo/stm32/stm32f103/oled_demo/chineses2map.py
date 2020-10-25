import os
import sys
import re
from pathlib import Path
import subprocess as sp


map_file = 'myfont.map'
chineses = '''你好世界
温度
'''


def run_cmd(cmd, env=os.environ):
    '''run shell command'''
    print('run cmd: %s' % cmd)
    with sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT, env=env) as p:
        for line in p.stdout:
            print(line.decode().strip())
        return p.poll()


def make_mapfile(chineses, map_file):

    chineses = re.sub(r'\s', '', chineses).encode('unicode_escape').decode()
    chineses = re.sub(
        r'\\u([0-9a-f]{4})', r'$\1,' + os.linesep, chineses).strip().upper()

    map_content = '32-128,' + os.linesep + chineses
    print(map_content)

    with open(map_file, 'w') as f:
        f.write(map_content)


def make_font(bdfconv_file, map_file, bdf_file, font_name):

    cmd = '{0} -g 32 -b 0 -f 1 -M {1} -n {2} -o {2}.c {3}'.format(
        bdfconv_file, map_file, font_name, bdf_file)

    ret = run_cmd(cmd)
    if ret:
        print('generate font failed!')
    else:
        print('generate font successfully!')

    with open('{}.c'.format(font_name), 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith('const uint8_t {}'.format(font_name)):
                return lines[i:]
    return []


def make_font_library(font_name, font_lib_c, font_lib_h, font_lib_c_lines, font_lib_h_lines):

    font_lib_dir = Path(font_lib_c).parent
    font_lib_dir.mkdir(parents=True, exist_ok=True)

    with open(font_lib_c, 'w') as f:
        f.write(''.join(font_lib_c_lines))

    with open(font_lib_h, 'w') as f:
        f.write(os.linesep.join(font_lib_h_lines))


if __name__ == "__main__":

    bdfconv_file = './Libs/u8g2/tools/font/bdfconv/bdfconv'
    font_lib_c = 'Libs/myfont/myfont.c'
    font_lib_h = 'Libs/myfont/myfont.h'
    map_file = 'myfont.map'

    font_oncifg = [
        [
            'u8g2_font_wqy9_myfont',
            'Libs/u8g2_wqy/bdf/wenquanyi_9pt.bdf'
        ],
        [
            'u8g2_font_wqy12_myfont',
            'Libs/u8g2_wqy/bdf/wenquanyi_12pt.bdf'
        ],
        [
            'u8g2_font_wqy13_myfont',
            'Libs/u8g2_wqy/bdf/wenquanyi_13px.bdf'
        ]
    ]

    font_lib_c_lines = ['#include "u8g2.h"' + os.linesep + os.linesep]
    font_lib_h_lines = ['#pragma once', '#include "u8g2.h"']

    for font_name, bdf_file in font_oncifg:
        make_mapfile(chineses, map_file)
        font_info = make_font(bdfconv_file, map_file, bdf_file, font_name)
        font_info.append(os.linesep)
        font_lib_c_lines.extend(font_info)
        font_lib_h_lines.append(
            'extern const uint8_t {0}[] U8G2_FONT_SECTION("{0}");'.format(font_name))

    make_font_library(font_name, font_lib_c, font_lib_h,
                      font_lib_c_lines, font_lib_h_lines)

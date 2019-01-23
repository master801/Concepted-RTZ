#!/usr/bin/env python3

import argparse
import os
import glob

if not __debug__:  # Dev workspace
    from src import rtz, constants
else:
    import rtz
    import constants


def __main__():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', dest='input_dir', required=True, nargs=1, type=str, help='Input directory')
    parser.add_argument('--output', dest='output_dir', required=True, nargs=1, type=str, help='Output directory')
    parser.add_argument('--mode', dest='mode', required=True, nargs=1, type=str, choices=[constants.MODE_DECODE, constants.MODE_ENCODE], help='Mode')
    args = parser.parse_args()

    mode = args.mode[0]
    input_dir = args.input_dir[0]
    output_dir = args.output_dir[0]

    found_files = find_files(mode, input_dir)
    if found_files is not None:
        for found_file in found_files:
            if not found_file == 'in/script\\a_00_00.rtz':  # TODO REMOVE - DEBUG
                continue
            read_file(found_file, mode)
            continue
    else:
        print('Failed to find files!')
    return


def find_files(mode, directory):
    if mode == constants.MODE_DECODE:
        rtz_files = []
        for root, subdirs, files in os.walk(directory):
            if len(files) < 1:  # Skip dirs with no files
                continue
            for _rtz in glob.iglob(root + '\\' + '*.rtz'):
                rtz_files.append(_rtz)
        return rtz_files
    elif mode == constants.MODE_ENCODE:
        json_files = []
        for root, subdirs, files in os.walk(directory):
            if len(files) < 1:  # Skip dirs with no files
                continue
        for _bin in glob.iglob(root + '\\' + '*.json'):
            json_files.append(_bin)
        return json_files
    return None


def read_file(input_file, mode):
    file = open(input_file, 'rb')
    length = os.stat(input_file).st_size

    if mode == constants.MODE_DECODE:
        return rtz.read_rtz_file(file, length)
    elif mode == constants.MODE_ENCODE:
        return  # TODO

    file.close()
    return


if __name__ == '__main__':
    __main__()

#!/usr/bin/env python3

import struct
import re

if not __debug__:  # Dev workspace
    from src import constants
else:
    import constants


def read_rtz_file(rtz_file, length):
    header_imports = read_header_imports(rtz_file)  # Doesn't do anything...
    text_lines = read_text(rtz_file, length)

    print()
    return


def read_header_imports(rtz_file):

    """
    Only made because of boredom and for documentation reasons...
    Doesn't do anything
    """
    rtz_file.seek(0x00)
    import_entries = struct.unpack('>H', rtz_file.read(0x02))

    headers = []
    for import_index in range(import_entries[0]):
        import_length = struct.unpack('>B', rtz_file.read(0x1))[0]
        import_name = str(rtz_file.read(import_length))
        headers.append(
            {
                'import_name_length': import_length,
                'import_name': import_name
            }
        )
        continue

    return headers


def read_text(rtz_file, length):
    rtz_file.seek(0x00)
    raw = rtz_file.read(length)
    indexed = raw.index(constants.BYTES_PATTERN)

    start = indexed + len(constants.BYTES_PATTERN)
    read_from = raw[start:length]

    block_lists = []

    new_seek = 0x4
    indices = struct.unpack('>I', read_from[0x00:0x04])[0] - 1
    for block in range(0x00, indices):
        value_block = read_from[new_seek:new_seek + 0x4]  # I honestly don't know what this does, but I assume it's a value
        new_seek += 0x04

        name_length = struct.unpack('>B', read_from[new_seek:new_seek + 0x1])[0]  # Get length of name
        new_seek += 0x01

        name = read_from[new_seek:new_seek + name_length]  # Get name
        new_seek += name_length

        block_lists.append({value_block, name})
        continue

    new_seek += 0x19

    actual_seek = start + new_seek

    # TODO

    print()
    return

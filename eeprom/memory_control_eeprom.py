
import sys
import re

MIN_PYTHON = (3, 7)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)


def set_bit(n, index, bit):
    mask = 1 << index
    n &= ~mask
    if bit:
        n |= mask
    return n


def generate_bits(controls):
    output = 0
    for index, (control, value) in enumerate(controls.items()):
        output = set_bit(output, index, 0 if value else 1)
    return output


# Ends of memory (not base)
START_ROM = 0x0
ROM_SIZE = 0x400

IN = 0x400
OUT = 0x401
START_VRAM = 0x1000
VRAM_SIZE = 0x1000


def generate_controls(input):
    controls = {
        "chipEnableVRAM": 0,
        "chipEnableROM": 0,
        "chipEnableRAM": 0,
        "enableIn": 0,
        "loadOut": 0,
    }

    # bit 15
    selector = bool(int(input[0]))

    # bit 14 is intentionally skipped

    # bit 0-13
    address = int(input[1:15], 2)

    if selector:
        controls["chipEnableRAM"] = 1
        return controls

    if (address >= START_ROM and address < START_ROM + ROM_SIZE):
        controls["chipEnableROM"] = 1
    elif (address >= START_VRAM and address < START_VRAM + VRAM_SIZE):
        controls["chipEnableVRAM"] = 1
    elif (address == IN):
        controls["enableIn"] = 1
    elif (address == OUT):
        controls["loadOut"] = 1

    return controls


# print(generate_bits(controls))
# generate_bits(controls)

with open("./out/memory_control.txt", "w") as f:
    f.write("v3.0 hex words plain\n")
    for i in range(0, 2**15):
        # 13 address + 1 write + 1 enable = 15
        input_bits = bin(i)[2:].zfill(15)
        f.write(hex(generate_bits(generate_controls(input_bits)))[2:] + " ")

# print(bin(generate_bits(generate_controls("0")))[2:].zfill(11))

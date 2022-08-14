
import sys
import re

MIN_PYTHON = (3, 7)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)


ENABLES = {
    "001": "AHigh",
    "010": "ALow",
    "011": "B",
    "100": "C",
    "101": "RAM",
    "110": "IRHigh",
    # "111": "ALU"
}
LOADS = {
    "001": "AHigh",
    "010": "ALow",
    "011": "B",
    "100": "C",
    "101": "RAM",
}


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


def generate_controls(input):
    controls = {
        # Each section represents a unique physical PCB
        # Instruction Register
        "loadIRHigh": 0,
        "loadIRLow": 0,
        "enableIRHigh": 0,
        "enableIRLow": 0,

        # A Register
        "loadAHigh": 0,
        "loadALow": 0,
        "enableAHigh": 0,
        "enableALow": 0,

        # B Register
        "loadB": 0,
        "enableB": 0,

        # C Register
        "loadC": 0,
        "enableC": 0,

        # Inputs to RAM / Memory helper
        "enablePC": 1,
        "enableA": 0,

        # Program counter
        "loadPC": 0,
        "notCount": 0,
        "clearMicrocode": 0,

        # RAM
        "loadRAM": 0,
        "enableRAM": 0,
    }
    input = re.sub('\s+', '', input)
    microcode = input[0:2]
    instruction = input[2:10]
    enable = instruction[0:3]
    load = instruction[3:6]

    print(enable)
    # Put low byte of instruction into IRLow
    if microcode == "00":
        controls["enableRAM"] = 1
        controls["loadIRLow"] = 1
        return controls

    # Put high byte of instruction into IRHigh and do not increment program counter
    if microcode == "01":
        controls["notCount"] = 1
        controls["enableRAM"] = 1
        controls["loadIRHigh"] = 1
        return controls

    # Execute the instruction
    if microcode == "10":
        controls["enableA"] = 1
        controls["clearMicrocode"] = 1

    # if enable == "111":
    #     controls["enableIRHigh"] = 1

    if enable in ENABLES:
        controls["enable" + ENABLES[enable]] = 1

    if load in LOADS:
        controls["load" + LOADS[load]] = 1

    return controls


# print(generate_bits(controls))
# generate_bits(controls)

with open("control_eeprom.txt", "w") as f:
    f.write("v3.0 hex words plain\n")
    for i in range(0, 2**11):
        # 8 instruction + 3 microcode clock = 11
        input_bits = bin(i)[2:].zfill(11)
        f.write(hex(generate_bits(generate_controls(input_bits)))[2:] + " ")

print(bin(generate_bits(generate_controls("10 1110 0000 0")))[2:].zfill(11))

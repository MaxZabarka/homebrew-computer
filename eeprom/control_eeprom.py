
import sys
import re
from constants import ENABLES, LOADS, JUMPS

# Control inputs
# aaaaaaaa xx znc mm
# a = IRLow
# m = microcode
# z = not zero flag
# n = negative flag
# c = not carry flag


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

        # ALU
        "enableALU": 0
    }
    input = re.sub('\s+', '', input)
    instruction = input[0:8]
    alu_flags = input[10:13]
    microcode = input[13:15]

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
        controls["enablePC"] = 0
        controls["clearMicrocode"] = 1

    is_computation_instruction = instruction[0]
    load = instruction[1:4]

    if load in LOADS:
        controls["load" + LOADS[load]] = 1

    if int(is_computation_instruction):
        controls["enableALU"] = 1
        zero = not bool(int(alu_flags[0]))
        negative = bool(int(alu_flags[1]))
        carry = not bool(int(alu_flags[2]))
        print(zero, negative, carry)
        jump_bits = instruction[4:8]
        should_jump = False
        if jump_bits in JUMPS:
            should_jump = True      
            condition = JUMPS[jump_bits]
            for flag, expected_value in condition.items():
                if flag == "zero" and zero != expected_value:
                    should_jump = False
                if flag == "negative" and negative != expected_value:
                    should_jump = False
                if flag == "carry" and carry != expected_value:
                    should_jump = False
        print(should_jump)
        if should_jump:
            controls["loadPC"] = 1
    else:
        enable = instruction[4:7]
        if enable in ENABLES:
            controls["enable" + ENABLES[enable]] = 1

    # if enable == "111":
    #     controls["enableIRHigh"] = 1

    return controls


# print(generate_bits(controls))
# generate_bits(controls)

# with open("./out/control_eeprom.txt", "w") as f:
#     f.write("v3.0 hex words plain\n")
#     for i in range(0, 2**15):
#         input_bits = bin(i)[2:].zfill(15)
#         f.write(hex(generate_bits(generate_controls(input_bits)))[2:] + " ")

print(bin(generate_bits(generate_controls("100000110010110"))))
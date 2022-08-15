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

# get instruction, mask, then if the result is greater than 0 jump
# cnz
# c = carry
# n = negative
# z = zero

JUMPS = {
    "0001": {"zero": True, "negative": True},
    "0010": {"negative": True},
    "0011": {"zero": True},
    "0100": {"zero": False, "negative": False},
    "0101": {"negative": False},
    "0110": {"carry": True},
    "0111": {"carry": False},
    "1000": {}
}
JUMP_NAMES = {
    "JLE":"0001",
    "JLT":"0010",
    "JEQ":"0011",
    "JGT":"0100",
    "JGE":"0101",
    "JC":"0110",
    "JNC":"0111",
    "JMP":"1000",
}
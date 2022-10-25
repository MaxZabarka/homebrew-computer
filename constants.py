LOADS = {
    "001": "AHigh",
    "010": "ALow",
    "011": "B",
    "100": "C",
    "101": "RAM",
}

ENABLES = {
    "001": "AHigh",
    "010": "ALow",
    "011": "B",
    "100": "C",
    "101": "RAM",
    "110": "IRHigh",
    # "111": "ALU"
}

JUMP_NAMES = {
    "JLE": "0001",
    "JLT": "0010",
    "JEQ": "0011",
    "JGT": "0100",
    "JGE": "0101",
    "JC": "0110",
    "JNC": "0111",
    "JMP": "1000",
    "JNE": "1001",
}


def SHOULD_JUMP(jumpBits, negative, zero, carry):
    if jumpBits == JUMP_NAMES["JLE"]:
        return negative or zero
    elif jumpBits == JUMP_NAMES["JLT"]:
        return negative and (not zero)
    elif jumpBits == JUMP_NAMES["JEQ"]:
        return zero
    elif jumpBits == JUMP_NAMES["JGT"]:
        return (not negative) and (not zero)
    elif jumpBits == JUMP_NAMES["JGE"]:
        return (not negative) or zero
    elif jumpBits == JUMP_NAMES["JC"]:
        return carry
    elif jumpBits == JUMP_NAMES["JNC"]:
        return not carry
    elif jumpBits == JUMP_NAMES["JMP"]:
        return True
    elif jumpBits == JUMP_NAMES["JNE"]:
        return not zero
    return False

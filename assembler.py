
from constants import ENABLES, LOADS

# Reverse keys and values
ENABLES = {v: k for k, v in ENABLES.items()}
LOADS = {v: k for k, v in LOADS.items()}


with open('source.zab', 'r') as file:
    data = file.read()

print("v3.0 hex words plain")
for instruction in data.split("\n"):
    [destination, source] = instruction.split("=")
    source = source.strip()
    destination = destination.strip()
    destination_bits = LOADS[destination]

    if (source.startswith("c")):
        computation_bits = source.split("c")[1]
        low_byte = "1" + destination_bits + "0000"
        high_byte = computation_bits + "00"
    else:
        if (source.isdigit()):
            source_bits = ENABLES["IRHigh"]
        else:
            source_bits = ENABLES[source]
        low_byte = "0" + destination_bits + source_bits + "0"
        if (source.isdigit()):
            high_byte = bin(int(source))[2:].zfill(8)
        else:
            high_byte = "0"*8

    # print(low_byte, high_byte)
    print(hex(int(low_byte, 2))[2:], end=" ")
    print(hex(int(high_byte, 2))[2:], end=" ")

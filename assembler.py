
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

    if (source.isdigit()):
        source_bits = ENABLES["IRHigh"]
    else:
        source_bits = ENABLES[source]

    destination_bits = LOADS[destination]

    output = source_bits + destination_bits + "00"
    print(hex(int(output, 2))[2:], end=" ")
    if (source.isdigit()):
        print(hex(int(source))[2:], end=" ")
    else:
        print("0", end=" ") 

    # source_bits = ENABLES[]

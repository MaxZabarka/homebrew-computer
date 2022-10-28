#!/usr/bin/env python3.10


# TODO 
# More operation
# Pointers
  # dereference
  # addrof
# Array subscripting
# EEPROM I2C IO
# Assembly optimization (remove redundant A assignments)
# While loops
# For loops
# Multiplication and division

# pop pointer-16-8 (put an 8 bit value into a 16 bit address)
# pop local-16 (put an 16 bit value into a two local variables)
# push local-16 (push a 16 bit local variable)
# pop argument-16-8 (^)
# push argument-16-8 (^)
# # push constant-16


import argparse
from arguments import parse_file_io
import subprocess
import os

parser = argparse.ArgumentParser(
    description="Compile a high level source file into machine code")

args = parse_file_io(parser, "bin")

no_ext_output = os.path.splitext(args.output)[0]


def run(command):
    try:
        subprocess.check_call(command)
    except subprocess.CalledProcessError as e:
        exit(1)
        # # print("123 ASDSADASDASDASD")
        # raise "aSDASD"


run(["./compiler/code_generator.py", args.file, "-o", no_ext_output + ".vm"])

run(["./virtual_machine/virtual_machine.py",
     no_ext_output+".vm", "-o", no_ext_output + ".zab"])

run(["./assembler.py", no_ext_output+".zab", "-o", args.output])

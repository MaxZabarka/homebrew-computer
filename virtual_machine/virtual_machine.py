#!/usr/bin/env python3.10


import argparse
import sys
import os
import tempfile
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from arguments import parse_file_io
from check_file import check_file
from helpers import remove_comments

parser = argparse.ArgumentParser(
    description='Compile a virtual machine file into assembly')
parser.add_argument("-r", "--ram", action="store_true",
                    help="Generate code that will run in the memory space of the RAM instead of ROM")
args = parse_file_io(parser, "zab")

arithmetic = ["add", "subtract", "not",
              "equal", "or", "greater_than", "less_than", "left_shift", "bitwise_and", "less_than_or_equal", "greater_than_or_equal", "inequal"]
# operations that the computer can do in one hardware cycle
built_in_arithmetic = ["add", "subtract", "or", "bitwise_and", "left_shift"]

STACK_START = 9

class Parser:
    def __init__(self, file_name):
        check_file(file_name)

        self.input_file = open(file_name)

        temp_file_name = tempfile.NamedTemporaryFile().name

        # Turn input_file into a list of instructions (vm_list)
        with open(temp_file_name, 'w', encoding='utf-8') as f:
            f.write(remove_comments(self.input_file.read()))

        with open(temp_file_name, 'r', encoding='utf-8') as f:
            self.vm_list = []
            for i in f.readlines():
                to_append = i.replace("\n", "")
                if to_append:
                    self.vm_list.append(to_append)
        self.input_file.close()
        self.current_index = 0
        self.current_command = self.vm_list[self.current_index]

    def advance(self):
        self.current_index += 1
        self.current_command = self.vm_list[self.current_index]

    def has_more_commands(self):
        if self.current_index < len(self.vm_list) - 1:
            return True
        else:
            return False

    def command_type(self):
        command_list = self.current_command.split()
        if command_list[0].lower() in arithmetic:
            return "C_ARITHMETIC"
        elif command_list[0] == "push":
            return "C_PUSH"
        elif command_list[0] == "pop":
            return "C_POP"
        elif command_list[0] == "label":
            return "C_LABEL"
        elif command_list[0] == "goto":
            return "C_GOTO"
        elif command_list[0] == "if-goto":
            return "C_IF"
        elif command_list[0] == "if-not-goto":
            return "C_IF_NOT"
        elif command_list[0] == "call":
            return "C_CALL"
        elif command_list[0] == "return":
            return "C_RETURN"
        elif command_list[0] == "function":
            return "C_FUNCTION"
        else:
            raise NotImplementedError(command_list[0])

    def arg1(self):
        if self.current_command.split()[0] in arithmetic:
            # Return arithmetic operation
            return self.current_command.split()[0]
        else:
            # Return segment
            return self.current_command.split()[1]

    def arg2(self):
        # Return integer
        return self.current_command.split()[2]


segments = ["LOCAL", "ARGUMENT"]


class CodeWriter:
    def __init__(self, filename, is_ram=False, origin=0x8000):
        self.filename = filename
        if filename.endswith('.vm'):
            self.filename = filename[:-3]
        self.instructions_list = []
        self.origin = origin
        self.id = 0
        self.is_ram = is_ram
        self.uid = 0
        self.write_bootstrap()

    def write_arithmetic(self, op):
        if (op in built_in_arithmetic):
            self.instructions_list += [
                "AHigh = STACK_POINTER.h",  # SP--
                "ALow = STACK_POINTER.l",
                "B = RAM",
                "RAM = (B-1)",
                "ALow = (B-1)",  # C = arg1
                "AHigh = 128",
                "C=RAM",
                "AHigh = STACK_POINTER.h",  # B = arg2
                "ALow = STACK_POINTER.l",
                "B = RAM",
                "ALow = (B-1)",
                "AHigh = 128",
                "B = RAM",
            ]
            if op == "add":
                self.instructions_list.append("RAM = (B+C)")
            elif op == "subtract":
                self.instructions_list.append("RAM = (B-C)")
            elif op == "or":
                self.instructions_list.append("RAM = (B|C)")
            elif op == "bitwise_and":
                self.instructions_list.append("RAM = (B&C)")
            elif op == "left_shift":
                self.uid += 1
                uid = self.uid

                self.write_label(f"left_shift_{uid}")
                self.instructions_list += [
                    # if c == 0 goto end
                    f"AHigh = end_{uid}.h",
                    f"ALow = end_{uid}.l",
                    "(C), JEQ",

                    # C--
                    "ALow = B",
                    "B = 255",
                    "C = (B+C)",
                    "B = ALow",

                    # B << 1
                    "B = (B+B)",
                    f"AHigh = left_shift_{uid}.h",
                    f"ALow = left_shift_{uid}.l",
                    "JMP",
                ]
                self.write_label(f"end_{uid}")
                self.instructions_list += [
                    "C = B",
                    "AHigh = 128",
                    "ALow = STACK_POINTER.l",
                    "B = RAM",
                    "ALow = (B-1)",
                    "RAM = C",
                ]

            else:
                raise NotImplementedError
        else:
            if (op == "not"):
                self.uid += 1
                self.instructions_list += [
                    # B = arg
                    "AHigh = 128",
                    "ALow = STACK_POINTER.l",
                    "B = RAM",
                    "ALow = (B-1)",
                    "B = RAM",

                    f"AHigh = false_{self.uid}.h",
                    f"ALow = false_{self.uid}.l",
                    "(B), JEQ",

                    "AHigh = 128",
                    "ALow = STACK_POINTER.l",
                    "B = RAM",
                    "ALow = (B-1)",
                    "RAM = 0"]
                self.write_goto(f"end_{self.uid}")

                self.write_label(f"false_{self.uid}")
                self.instructions_list += [
                    "AHigh = 128",
                    "ALow = STACK_POINTER.l",
                    "B = RAM",
                    "ALow = (B-1)",
                    "RAM = 1"
                ]

                self.write_label(f"end_{self.uid}")
            elif (op in ["equal", "greater_than", "less_than", "inequal", "greater_than_or_equal", "less_than_or_equal"]):
                if op == "equal":
                    command = "JEQ"
                elif op == "greater_than":
                    command = "JGT"
                elif op == "less_than":
                    command = "JLT"
                elif op == "inequal":
                    command = "JNE"
                elif op == "greater_than_or_equal":
                    command = "JGE"
                elif op == "less_than_or_equal":
                    command = "JLE"
        


                self.uid += 1
                self.instructions_list += [
                    # SP--
                    "AHigh = 128",
                    "ALow = STACK_POINTER.l",
                    "B = RAM",
                    "RAM = (B-1)",

                    # C = arg1
                    "ALow = RAM",
                    "C = RAM",

                    # B = arg2
                    "AHigh = 128",
                    "ALow = STACK_POINTER.l",
                    "B = RAM",
                    "ALow = (B-1)",
                    "AHigh = 128",
                    "B = RAM",

                    f"AHigh = equal_{self.uid}.h",
                    f"ALow = equal_{self.uid}.l",
                    f"(B-C), {command}",

                    "AHigh = 128",
                    "ALow = STACK_POINTER.l",
                    "B = RAM",
                    "ALow = (B-1)",
                    "RAM = 0"]
                self.write_goto(f"end_{self.uid}")

                self.write_label(f"equal_{self.uid}")
                self.instructions_list += [
                    "AHigh = 128",
                    "ALow = STACK_POINTER.l",
                    "B = RAM",
                    "ALow = (B-1)",
                    "RAM = 1"
                ]

                self.write_label(f"end_{self.uid}")
            else:
                raise NotImplementedError(op)

    def write_point_a(self):
        self.instructions_list += [
            "AHigh = STACK_POINTER.h",
            "ALow = STACK_POINTER.l",
            "AHigh = 128",
            "ALow = RAM",
        ]

    def write_push_pop(self, command, segment, index):
        if (command == "C_PUSH"):
            self.write_push(segment, index)
        elif (command == "C_POP"):
            self.write_pop(segment, index)
        else:
            raise NotImplementedError

    def write_push(self, segment, index):
        if (segment == "constant"):
            self.write_point_a()
            self.instructions_list += [

                f"RAM={index}"
            ]
            self.write_increment_sp()

        elif (segment in ["argument", "local"]):
            self.instructions_list += [
                f"C={index}",

                # A = index + segment
                "AHigh = 128",
                f"ALow = {segment.upper()}.l",
                "B=RAM",
                "ALow=(B+C)",

                # C = segment[index]
                "C = RAM",

                # RAM[SP] = C
                "ALow = STACK_POINTER.l",
                "ALow = RAM",
                "RAM = C",

                # SP++
                "ALow = STACK_POINTER.l",
                "B = RAM",
                "RAM = (B+1)"
            ]
        else:
            raise NotImplementedError(segment)

    def write_halt(self):
        if (not self.is_ram):
            self.instructions_list.append("#origin 0")
        self.instructions_list += [
            "halt:",
            "AHigh = halt.h",
            "ALow = halt.l",
            "JMP"
        ]
        if (not self.is_ram):
            self.instructions_list.append(f"#origin {self.origin}")

    def write_pop(self, segment, index):
        if (segment in ["argument", "local"]):
            self.instructions_list += [
                # LCL/ARG = segment + index
                f"ALow = {segment.upper()}.l",
                f"C={index}",
                "B=RAM",
                "RAM=(B+C)",

                # SP--
                "AHigh = 128",
                "ALow = STACK_POINTER.l",
                "B=RAM",
                "RAM=(B-1)",

                # C = popped value
                "ALow = RAM",
                "C = RAM",

                # segment[index] = C
                f"ALow = {segment.upper()}.l",
                "ALow = RAM",
                "RAM = C",

                # LCL/arg = segment - index
                f"ALow = {segment.upper()}.l",
                f"C={index}",
                "B=RAM",
                "RAM=(B-C)",

            ]
        else:
            raise NotImplementedError(segment)

    def write_label(self, label):
        if (not self.is_ram):
            self.instructions_list.append("#origin 0")

        self.instructions_list.append(f"{label}:")

        if (not self.is_ram):
            self.instructions_list.append(f"#origin {self.origin}")

    def write_goto(self, label):
        self.instructions_list += [
            f"AHigh = {label}.h",
            f"ALow = {label}.l",
            "JMP"
        ]

    def write_function(self, name, local_variables):
        if (not self.is_ram):
            self.instructions_list.append(f"#origin 0x0")
        self.instructions_list.append(f"{name}:")
        if (not self.is_ram):
            self.instructions_list.append(f"#origin {self.origin}")
        if (int(local_variables) > 0):
            # make space for local variables
            self.instructions_list += [
                f"C={int(local_variables)}",
                "AHigh = 128",
                "ALow = STACK_POINTER.l",
                "B = RAM",
                "RAM = (B+C)"
            ]

    def write_return(self):
        self.instructions_list += [
            # TEMP_2 = FRAME
            "AHigh = 128",
            "ALow = LOCAL.l",
            "B=RAM",
            "ALow = TEMP_2.l",
            "RAM=B",
        ]

        # TEMP_0 = high return byte
        # TEMP_1 = low return byte
        for return_byte in [0, 1]:
            self.instructions_list += [
                f"C={len(segments)+1+return_byte}",
                "C=(B-C)",
                "ALow = C",
                "C = RAM",
                f"ALow = TEMP_{return_byte}.l",
                "RAM = C"
            ]

        # *ARG = pop()
        # / ARG[0] = top of stack
        self.instructions_list += [
            "ALow = STACK_POINTER.l",
            "B=RAM",
            "RAM=(B-1)",
            "ALow=RAM",
            "C=RAM",
            "ALow = ARGUMENT.l",
            "ALow = RAM",
            "RAM=C"
        ]

        # SP = ARG + 1
        self.instructions_list += [
            "ALow = ARGUMENT.l",
            "B=RAM",
            "ALow = STACK_POINTER.l",
            "RAM=(B+1)"
        ]

        # Restore segments
        # Argument = *(FRAME-1)
        # Local = *(FRAME-2)
        for i, segment in enumerate(segments[::-1]):
            self.instructions_list += [
                # B = *(FRAME-x)
                "ALow = TEMP_2.l",
                "B = RAM",
                f"C = {i + 1}",
                "B = (B-C)",
                "ALow = B",
                "B = RAM",

                # Restore segment
                f"ALow = {segment.upper()}.l",
                "RAM=B"

            ]

        # Jump to return
        self.instructions_list += [
            "ALow = TEMP_1.l",
            "B = RAM",
            "ALow = TEMP_0.l",
            "AHigh = RAM",
            "ALow = B",
            "JMP"
        ]

    def write_call(self, name, arguments):
        ret = f"RETURN{name}{self.uid}"
        self.uid += 1
        # Push unique return address
        self.write_point_a()
        self.instructions_list += [
            f"RAM={ret}.l",
            "AHigh = 128",
            "ALow = STACK_POINTER.l",
            "B=RAM",
            "RAM=(B+1)",
            "ALow=RAM",
            f"RAM={ret}.h",
            "ALow = STACK_POINTER.l",
            "B=RAM",
            "RAM=(B+1)"
        ]

        # Push ARG
        for segment in segments:
            self.instructions_list += [
                "AHigh = 128",
                f"ALow = {segment}.l",
                "B = RAM",
                "ALow = STACK_POINTER.l",
                "ALow = RAM",
                "RAM = B",
                "ALow = STACK_POINTER.l",
                "B = RAM",
                "RAM = (B+1)"
            ]

        # ARG = SP-arguments-segments-2
        self.instructions_list += [
            "ALow = STACK_POINTER.l",
            "B=RAM",
            f"C={int(arguments)+len(segments)+2}",
            "B=(B-C)",
            "ALow = ARGUMENT.l",
            "RAM=B"
        ]

        # LCL = SP
        self.instructions_list += [
            "ALow = STACK_POINTER.l",
            "B=RAM",
            "ALow = LOCAL.l",
            "RAM=B"
        ]

        # Jump to called function
        self.instructions_list += [
            f"AHigh = {name}.h",
            f"ALow = {name}.l",
            "JMP"
        ]

        # Return address
        if (not self.is_ram):
            self.instructions_list.append("#origin 0")

        self.instructions_list.append(f"{ret}:")

        if (not self.is_ram):
            self.instructions_list.append(f"#origin {self.origin}")

    def write_if(self, label, logic_not=False):
        jump = "JEQ" if logic_not else "JNE"
        self.instructions_list += [
            "AHigh = 128",
            "ALow = STACK_POINTER.l",
            "B=RAM",
            "RAM=(B-1)",
            "ALow=RAM",
            "B=RAM",
            f"AHigh = {label}.h",
            f"ALow = {label}.l",
            f"(B), {jump}"
        ]

    def write_bootstrap(self):
        self.instructions_list += [
            f"#origin {self.origin}",  # start of ram
            "AHigh = STACK_POINTER.h",
            "ALow = STACK_POINTER.l",
            f"RAM={STACK_START}",  # Default stack pointer
        ]
        self.write_call("main", 0)

    def write_increment_sp(self):
        self.instructions_list += [
            "AHigh = STACK_POINTER.h",
            "ALow = STACK_POINTER.l",
            "B=RAM",
            "RAM=(B+1)"
        ]

    def close(self):
        with open(self.filename, "w") as f:
            f.write("")
            for instruction in self.instructions_list:
                f.write(instruction + "\n")


parser = Parser(args.file)

code_writer = CodeWriter(args.output, args.ram)

while True:
    if parser.command_type() == "C_ARITHMETIC":
        code_writer.write_arithmetic(parser.arg1().lower())
    elif parser.command_type() in ["C_PUSH", "C_POP"]:
        code_writer.write_push_pop(parser.command_type(),
                                   parser.arg1(),
                                   parser.arg2())
    elif parser.command_type() == "C_LABEL":
        code_writer.write_label(parser.arg1())
    elif parser.command_type() == "C_GOTO":
        code_writer.write_goto(parser.arg1())
    elif parser.command_type() == "C_IF":
        code_writer.write_if(parser.arg1())
    elif parser.command_type() == "C_IF_NOT":
        code_writer.write_if(parser.arg1(), True)
    elif parser.command_type() == "C_FUNCTION":
        code_writer.write_function(parser.arg1(), parser.arg2())
    elif parser.command_type() == "C_CALL":
        code_writer.write_call(parser.arg1(), parser.arg2())
    elif parser.command_type() == "C_RETURN":
        code_writer.write_return()
    if parser.has_more_commands():
        parser.advance()
    else:
        break
code_writer.write_halt()
code_writer.close()

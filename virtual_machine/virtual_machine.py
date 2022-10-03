#!/usr/bin/env python3.10
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from helpers import remove_comments
import argparse
from check_file import check_file

parser = argparse.ArgumentParser(
    description='Compile a Jack Virtual Machine file into Hack Assembly')
parser.add_argument(
    "file", help='The virtual machine file or directory to assemble')
parser.add_argument(
    "-o", "--output", help="Directs the output to a name of your choice")
parser.add_argument("-r", "--ram", action="store_true", help="Generate code that will run in the memory space of the RAM instead of ROM")


args = parser.parse_args()

arithmetic = ["add", "subtract"]
# operations that the computer can do in one hardware cycle
built_in_arithmetic = ["add", "subtract"]


class Parser:
    def __init__(self, file_name):
        check_file(file_name)

        self.input_file = open(file_name)

        # Turn input_file into a list of instructions (vm_list)
        with open("temp", 'w', encoding='utf-8') as f:
            f.write(remove_comments(self.input_file.read()))

        with open("temp", 'r', encoding='utf-8') as f:
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


class CodeWriter:
    def __init__(self, filename, is_ram=False, origin=0x8000):
        self.filename = filename
        if filename.endswith('.vm'):
            self.filename = filename[:-3]
        self.instructions_list = []
        self.origin = origin
        self.write_bootstrap()
        self.id = 0
        self.is_ram = is_ram

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
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError

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
        pass

    def write_label(self, label):
        pass

    def write_goto(self, label):
        pass

    def write_function(self, name, local_variables):
        pass

    def write_return(self):
        pass

    def write_call(self, name, arguments):
        pass

    def write_if(self, label):
        pass

    def write_bootstrap(self):
        self.instructions_list += [
            f"#origin {self.origin}",  # start of ram
            "AHigh = STACK_POINTER.h",
            "ALow = STACK_POINTER.l",
            "RAM=9"  # Default stack pointer
        ]

    def write_increment_sp(self):
        self.instructions_list += [
            "AHigh = STACK_POINTER.h",
            "ALow = STACK_POINTER.l",
            "B=RAM",
            "RAM=(B+1)"
        ]

    def close(self):
        with open(self.filename + ".zab", "w") as f:
            f.write("")
            for instruction in self.instructions_list:
                f.write(instruction + "\n")

    def write_constant(self, address, constant):
        pass

    def eq_gt_lt(self, command):
        if command == "eq":
            op = "JEQ"
        elif command == "gt":
            op = "JLT"
        elif command == "lt":
            op = "JGT"
        else:
            raise NotImplementedError


parser = Parser(args.file)
output_filename = "out"
if args.output:
    output_filename = args.output
elif args.file:
    output_filename = args.file

code_writer = CodeWriter(output_filename, args.ram)

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

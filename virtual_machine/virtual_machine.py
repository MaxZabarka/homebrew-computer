#!/usr/bin/env python3.10
from check_file import check_file
from helpers import remove_comments
import argparse
import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), '../'))


parser = argparse.ArgumentParser(
    description='Compile a Jack Virtual Machine file into Hack Assembly')
parser.add_argument(
    "file", help='The virtual machine file or directory to assemble')
parser.add_argument(
    "-o", "--output", help="Directs the output to a name of your choice")

args = parser.parse_args()

arithmetic = ["ADD", "SUBTRACT"]


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
        if command_list[0].upper() in arithmetic:
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
            raise NotImplementedError

    def arg1(self):
        if self.current_command.split()[0].upper() in arithmetic:
            # Return arithmetic operation
            return self.current_command.split()[0]
        else:
            # Return segment
            return self.current_command.split()[1]

    def arg2(self):
        # Return integer
        return self.current_command.split()[2]


class CodeWriter:
    def __init__(self, filename):
        self.filename = filename
        if filename.endswith('.vm'):
            self.filename = filename[:-3]
        self.instructions_list = []
        self.id = 0

    def write_arithmetic(self, op):
        pass

    def write_push_pop(self, command, segment, index):
        if (command == "C_PUSH"):
            self.write_push(segment, index)
        elif (command == "C_POP"):
            self.write_pop(segment, index)
        else:
            raise NotImplementedError

    def write_push(self, segment, index):
        if (segment == "constant"):
            self.instructions_list += [
                "AHigh = STACK_POINTER",
                "ALow = S"
            ]

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
        pass

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

code_writer = CodeWriter(output_filename)

while True:
    if parser.command_type() == "C_ARITHMETIC":
        code_writer.write_arithmetic(parser.arg1())
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
code_writer.close()

#!/usr/bin/env python3.10
from ast import Expression
from lexer import Lexer
from parser import Parser
from AST_types import *


class CodeGenerator:
    def __init__(self, parser):
        self.parser = parser
        self.global_var_symbol_table = {}
        self.function_symbol_table = {}
        self.instructions = []
        self.stack_pointer_valid = False

    def generate(self):
        instructions = []
        instructions += self.generate_init()
        for child in self.parser.AST:
            if isinstance(child, FunctionDec):
                instructions += self.generate_function_dec(child)
        print(self.function_symbol_table)
        for instruction in instructions:
            print(instruction)
        self.write_file(instructions)

    def write_file(self, instructions):
        with open("out.zab", "w") as file:
            for instruction in instructions:
                file.write(instruction + "\n")

    def generate_file_var_dec(self):
        pass

    def generate_statement(self, statement, local_symbol_table):
        if isinstance(statement, VarDec):
            self.generate_local_var_dec(statement, local_symbol_table)
            return []
        elif isinstance(statement, Constant) or isinstance(statement, BinOp):
            return self.generate_expression(statement)
        else:
            raise NotImplementedError

    def generate_expression(self, expression):
        if isinstance(expression, Constant):
            return self.generate_constant(expression)
        elif isinstance(expression, BinOp):
            return self.generate_bin_operation(expression)
        else:
            raise NotImplementedError

    def generate_constant(self, constant):
        return ["// generate constant"] + self.PUSH_CONSTANT(constant.value)

    def generate_init(self):
        instructions = ["// init"]
        instructions += self.SET_A_TO_ADDRESS_OF_SP_LOW()
        instructions.append("RAM = 3")
        instructions += self.SET_A_TO_ADDRESS_OF_SP_HIGH()
        instructions.append("RAM = 128")
        return instructions

    def generate_bin_operation(self, bin_op):

        instructions = ["// generate bin operation"]
        instructions += self.generate_expression(bin_op.a)
        instructions += self.generate_expression(bin_op.b)
        instructions += self.generate_bin_operator(bin_op.op)
        return instructions

    def generate_bin_operator(self, operator):
        instructions = ["// gen bin operator"]

        instructions += self.SUBTRACT_FROM_STACK_POINTER(2)
        instructions.append("B = RAM")
        instructions += self.INCREMENT_STACK_POINTER()
        instructions.append("C = RAM")
        instructions += self.INCREMENT_STACK_POINTER()
        if operator == "ADD":
            instructions.append("RAM = (B+C)")
        else:
            raise NotImplementedError
        return instructions

    def generate_local_var_dec(self, var_dec, local_symbol_table):
        if var_dec.name in local_symbol_table:
            raise Exception(var_dec.name + " is already defined")
        local_symbol_table[var_dec.name] = {
            "type": var_dec.type,
            "index": local_symbol_table["$local_variables"],
        }
        local_symbol_table["$local_variables"] += 1

    def generate_function_dec(self, function_dec):
        instructions = []
        if function_dec.name in self.function_symbol_table:
            raise Exception(function_dec.name + " is already defined")

        instructions.append(f"{function_dec.name}:")

        statement_instructions = []
        local_symbol_table = {"$local_variables": 0}
        for statement in function_dec.body:
            statement_instructions += self.generate_statement(
                statement, local_symbol_table
            )

        self.function_symbol_table[function_dec.name] = {
            "return_type": function_dec.return_type,
        }

        print(local_symbol_table)
        self.stack_pointer_valid = False
        instructions += self.ADD_TO_STACK_POINTER(
            local_symbol_table["$local_variables"]
        )
        self.stack_pointer_valid = False
        instructions += statement_instructions
        return instructions

    def already_defined(self, name):
        raise Exception(name + " is already defined")

    def PUSH_CONSTANT(self, value):
        instructions = []
        instructions += self.POINT_A_TO_TOP_OF_STACK()
        instructions.append(f"RAM = {value}")
        instructions += self.INCREMENT_STACK_POINTER()
        return instructions

    def INCREMENT_STACK_POINTER(self):
        instructions = []

        # increment first byte
        instructions += self.SET_A_TO_ADDRESS_OF_SP_LOW()
        instructions.append("B = RAM")
        instructions.append("RAM = (B+1)")

        return instructions

        # TODO increment second byte if carry

    def ADD_TO_STACK_POINTER(self, n):
        instructions = []

        # increment first byte
        instructions += self.SET_A_TO_ADDRESS_OF_SP_LOW()
        instructions.append("B = RAM")
        instructions.append(f"C = {n}")
        instructions.append("RAM = (B+C)")

        return instructions
        # TODO increment second byte if carry

    def SUBTRACT_FROM_STACK_POINTER(self, n):
        instructions = []

        # increment first byte
        instructions += self.SET_A_TO_ADDRESS_OF_SP_LOW()
        instructions.append("B = RAM")
        instructions.append(f"C = {n}")
        instructions.append("RAM = (B-C)")

        return instructions
        # TODO increment second byte if carry

    def POINT_A_TO_TOP_OF_STACK(self):
        instructions = []
        if not self.stack_pointer_valid:
            # ALow = *SP.l
            # AHigh = *SP.h
            instructions.append("// point A to top of stack")
            instructions.append("AHigh = STACK_POINTER_LOW.h")
            instructions.append("ALow = STACK_POINTER_LOW.l")
            instructions.append("B = RAM")
            instructions.append("AHigh = STACK_POINTER_HIGH.h")
            instructions.append("ALow = STACK_POINTER_HIGH.l")
            instructions.append("AHigh = RAM")
            instructions.append("ALow = B")

            # self.stack_pointer_valid = True
        return instructions

    def SET_A_TO_ADDRESS_OF_SP_LOW(self):
        instructions = ["// Set A to to SP_LOW"]
        instructions.append("AHigh = STACK_POINTER_LOW.h")
        instructions.append("ALow = STACK_POINTER_LOW.l")
        return instructions

    def SET_A_TO_ADDRESS_OF_SP_HIGH(self):
        instructions = ["// Set A to to SP_LOW"]
        instructions.append("AHigh = STACK_POINTER_HIGH.h")
        instructions.append("ALow = STACK_POINTER_HIGH.l")
        return instructions


if __name__ == "__main__":
    with open("./example.c") as f:
        lexer = Lexer(f)
    parser = Parser(lexer)
    parser.parse()
    code_generator = CodeGenerator(parser)
    code_generator.generate()

# TODO Cannot use B or C to store registers inbetween operations. Need to create another physical register to be able to move data around better

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

    def generate(self):
        instructions = []
        for child in self.parser.AST:
            if isinstance(child, FunctionDec):
                instructions += self.generate_function_dec(child)
        for instruction in instructions:
            print(instruction)

        self.write_file(instructions)

    def write_file(self, instructions):
        with open("out.vm", "w") as file:
            for instruction in instructions:
                file.write(instruction + "\n")

    def generate_file_var_dec(self):
        pass

    def generate_statement(self, statement):
        if isinstance(statement, VarDec):
            self.generate_local_var_dec(statement)
            return []
        elif isinstance(statement, Expression):
            return self.generate_expression(statement)
        elif isinstance(statement, Return):
            return  self.generate_return(statement)
        else:
            raise NotImplementedError
    
    def generate_return(self, return_statement):
        return self.generate_expression(return_statement.value) + ["return"]

    def generate_expression(self, expression):
        if isinstance(expression, Constant):
            return self.generate_constant(expression)
        elif isinstance(expression, BinOp):
            return self.generate_bin_operation(expression)
        elif isinstance(expression, FunctionCall):
            return self.generate_function_call(expression)
        else:
            raise NotImplementedError

    def generate_function_call(self, function_call):
        if not function_call.name in self.function_symbol_table:
            raise Exception(function_call.name + " is not defined")
        symbol_table = self.function_symbol_table[function_call.name]
        return [f"call {function_call.name} {len(symbol_table['argument_variables'])}"]

    def generate_constant(self, constant):
        return [f"push constant {constant.value}"]

    def generate_bin_operation(self, bin_op):
        return (
            self.generate_expression(bin_op.a)
            + self.generate_expression(bin_op.b)
            + [bin_op.op.lower()]
        )

    def generate_local_var_dec(self, var_dec):
        symbol_table = self.function_symbol_table[self.current_function]
        for variable in (
            symbol_table["local_variables"] + symbol_table["argument_variables"]
        ):
            if variable["name"] == var_dec.name:
                raise Exception(var_dec.name + " is already defined")

        symbol_table["local_variables"].append(
            {
                "name": var_dec.name,
                "type": var_dec.type,
                "index": len(symbol_table["local_variables"]),
            }
        )

    def generate_function_dec(self, function_dec):
        instructions = []
        if function_dec.name in self.function_symbol_table:
            raise Exception(function_dec.name + " is already defined")

        self.current_function = function_dec.name
        self.function_symbol_table[self.current_function] = {
            "local_variables": [],
            "argument_variables": [],
        }
        symbol_table = self.function_symbol_table[self.current_function]
        statement_instructions = []
        
        for parameter in function_dec.params:
            symbol_table["argument_variables"].append({
                "name":parameter.identifier,
                "type":parameter.type,
                "index":len(symbol_table["argument_variables"])
            })


        for statement in function_dec.body:
            statement_instructions += self.generate_statement(statement)

        symbol_table[
            "return_type"
        ] = function_dec.return_type

        instructions.append(
            f"function {function_dec.name} {len(symbol_table['local_variables'])}"
        )
        print(self.function_symbol_table)
        # self.stack_pointer_valid = False
        # instructions += self.ADD_TO_STACK_POINTER(
        #     local_symbol_table["$local_variables"]
        # )
        # self.stack_pointer_valid = False
        instructions += statement_instructions
        return instructions

    def already_defined(self, name):
        raise Exception(name + " is already defined")


if __name__ == "__main__":
    with open("./example.c") as f:
        lexer = Lexer(f)
    parser = Parser(lexer)
    parser.parse()
    code_generator = CodeGenerator(parser)
    code_generator.generate()

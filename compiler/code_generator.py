#!/usr/bin/env python3.10
from ast import Expression

from numpy import isin
from lexer import Lexer
from parser import Parser
from AST_types import *
import sys
import os
import argparse
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from arguments import parse_file_io


class CodeGenerator:
    def __init__(self, parser, output_file):
        self.parser = parser
        self.global_var_symbol_table = {}
        self.function_symbol_table = {}
        self.instructions = []
        self.output_file = output_file
        self.uid = 0

    def generate(self):
        instructions = []
        # instructions += self.generate_bootstrap()
        for child in self.parser.AST:
            if isinstance(child, FunctionDec):
                instructions += self.generate_function_dec(child)

        self.write_file(instructions)

    def write_file(self, instructions):
        with open(self.output_file, "w") as file:
            for instruction in instructions:
                file.write(instruction + "\n")

    # def generate_bootstrap(self):
    #     return ["call main 0"]

    def generate_global_var_dec(self):
        pass

    def generate_statements(self, statements):
        instructions = []
        for statement in statements:
            instructions += self.generate_statement(statement)
        return instructions

    def generate_statement(self, statement):
        if isinstance(statement, VarDec):
            self.generate_local_var_dec(statement)
            return []
        elif isinstance(statement, Expression):
            return self.generate_expression(statement)
        elif isinstance(statement, Return):
            return self.generate_return(statement)
        elif isinstance(statement, Assignment):
            return self.generate_assignment(statement)
        elif isinstance(statement, IfStatement):
            return self.generate_if(statement)
        elif isinstance(statement, WhileLoop):
            return self.generate_while(statement)
        elif isinstance(statement, str):
            return self.generate_expression(statement)
        else:
            raise NotImplementedError(statement)
        
    def generate_while(self, WhileLoop):
        self.uid += 1
        uid = self.uid
        instructions = []
        instructions += [f"label _{uid}_start"]
        instructions += self.generate_expression(WhileLoop.condition)
        instructions += [f"if-not-goto _{uid}_end"]
        instructions += self.generate_statements(WhileLoop.body)
        instructions += [f"goto _{uid}_start"]
        instructions += [f"label _{uid}_end"]
        return instructions

    def generate_if(self, if_statement):
        self.uid += 1
        uid = self.uid
        instructions = []

        for i, cond_block in enumerate(if_statement.cond_blocks):
            instructions += self.generate_expression(cond_block.condition)
            instructions += [f"if-goto _{uid}_BODY_{i}"]

        if (hasattr(if_statement, "else_body")):
            instructions += self.generate_statements(if_statement.else_body)

        instructions += [f"goto _{uid}_end"]

        for i, cond_block in enumerate(if_statement.cond_blocks):
            instructions += [f"label _{uid}_BODY_{i}"]
            instructions += self.generate_statements(cond_block.body)
            if (not i == len(if_statement.cond_blocks) - 1):
                instructions += [f"goto _{uid}_end"]

        instructions += [f"label _{uid}_end"]
        return instructions

    def generate_return(self, return_statement):
        return self.generate_expression(return_statement.value) + ["return"]

    def generate_assignment(self, assignment):
        instructions = []
        instructions += self.generate_expression(assignment.source)
        if (isinstance(assignment.destination, str)):
            segment, index = self.get_segment_and_index(assignment.destination)
            instructions += [f"pop {segment} {index}"]
        elif isinstance(assignment.destination, UnOp):
            if (assignment.destination.op == "DEREFERENCE"):
                # pass
                instructions += self.generate_expression(assignment.destination.a)
                instructions += ["pop pointer"]
            else:
                raise Exception("Invalid assignment")
        else:
            raise Exception("Invalid assignment")
        return instructions

    def generate_expression(self, expression):
        if isinstance(expression, Constant):
            return self.generate_constant(expression)
        elif isinstance(expression, BinOp):
            return self.generate_bin_operation(expression)
        elif isinstance(expression, FunctionCall):
            return self.generate_function_call(expression)
        elif isinstance(expression, UnOp):
            return self.generate_un_operation(expression)
        elif isinstance(expression, str):
            return self.generate_variable(expression)
        else:
            raise NotImplementedError

    def generate_un_operation(self, un_op):
        if (un_op.op == "ADDRESS_OF"):
            if (not isinstance(un_op.a, str)):
                raise Exception("& addressof operator must take a variable as argument")
            segment, index = self.get_segment_and_index(un_op.a)
            return [f"push address-of-{segment} {index}"]

        return self.generate_expression(un_op.a) + [un_op.op.lower()]

    def generate_variable(self, identifier):
        segment, index = self.get_segment_and_index(identifier)
        return [f"push {segment} {index}"]

    def get_segment_and_index(self, identifier):
        symbol_table = self.function_symbol_table[self.current_function]
        for local_variable in symbol_table["local_variables"]:
            if (identifier == local_variable["name"]):
                return ("local", local_variable["index"])

        for argument_variable in symbol_table["argument_variables"]:
            if (identifier == argument_variable["name"]):
                return ("argument", argument_variable["index"])

        raise Exception(f"{identifier} is not defined")

    def generate_function_call(self, function_call):
        if not function_call.name in self.function_symbol_table:
            raise Exception(function_call.name + " is not defined")
        symbol_table = self.function_symbol_table[function_call.name]
        instructions = []

        for argument in function_call.arguments:
            instructions += self.generate_expression(argument)

        return instructions + [
            f"call {function_call.name} {len(symbol_table['argument_variables'])}"
        ]

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
            symbol_table["local_variables"] +
                symbol_table["argument_variables"]
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

        for parameter in function_dec.params:
            symbol_table["argument_variables"].append(
                {
                    "name": parameter.identifier,
                    "type": parameter.type,
                    "index": len(symbol_table["argument_variables"]),
                }
            )

        statement_instructions = self.generate_statements(function_dec.body)

        symbol_table["return_type"] = function_dec.return_type

        size_of_local_variables = 0
        for variable in symbol_table["local_variables"]:
            if variable.type.pointer_amount >= 1:
                size_of_local_variables += 2
            else:
                size_of_local_variables += 1

        instructions.append(
            f"function {function_dec.name} {size_of_local_variables}"
        )
        instructions += statement_instructions
        return instructions

    def already_defined(self, name):
        raise Exception(name + " is already defined")


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        description='Compile a high level source file into a virtual machine file')
    args = parse_file_io(arg_parser, "vm")
    with open(args.file) as f:
        lexer = Lexer(f)
    parser = Parser(lexer)
    parser.parse()
    code_generator = CodeGenerator(parser, args.output)
    code_generator.generate()

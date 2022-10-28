#!/usr/bin/env python3.10

from ast import parse
from lexer import Lexer
from AST_types import *
from parse_expression import parse_expression
from draw_ast import draw_ast


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.AST = []
        self.file_symbol_table = {}

    def parse(self):
        self.parse_file()

    def parse_file(self):
        while self.lexer.has_more_tokens():
            type = self.parse_type()
            # function
            if not self.lexer.future_token_value() in ["=", ";"]:
                self.AST.append(self.parse_function_dec(type))
            else:
                self.AST += self.parse_var_dec(type)

        draw_ast(self.AST)

    def parse_function_dec(self, type):
        # type
        return_type = type

        # functionName
        self.verify(self.lexer.token_type() == "identifier")
        name = self.lexer.token_value()
        self.lexer.advance()

        # parameterList
        params = self.parse_param_list()

        # body
        statements = self.parse_statements()

        return FunctionDec(return_type, name, params, statements)

    def parse_var_dec(self, type):
        self.verify(self.lexer.token_type() == "identifier")
        name = self.lexer.token_value()
        if self.lexer.future_token_value() == "=":
            self.lexer.advance()
            return [VarDec(type, name), self.parse_assignment(name)]
        else:
            self.lexer.advance()
            if self.lexer.token_value() == "[":
                self.lexer.advance()
                array_size = parse_expression(self)
                self.eat("]")
                self.eat(";")
                return [VarDec(type, name, array_size)]
            self.eat(";")
            return [VarDec(type, name)]

    def parse_type(self):
        self.verify(self.lexer.token_value() in self.lexer.TYPES)
        type = self.lexer.token_value()
        self.lexer.advance()
        pointer_amount = 0
        while self.lexer.token_value() == "*":
            pointer_amount += 1
            self.lexer.advance()
        return Type(type, pointer_amount)

    def parse_param_list(self):
        param_list = []
        self.eat("(")
        if self.lexer.token_value() != ")":
            type = self.parse_type()
            name = self.lexer.token_value()
            self.lexer.advance()
            param_list.append(Parameter(type, name))
        while self.lexer.token_value() == ",":
            self.eat(",")
            type = self.parse_type()
            name = self.lexer.token_value()
            self.lexer.advance()
            param_list.append(Parameter(type, name))
        self.eat(")")
        return param_list

    def parse_function_call(self):
        self.verify(self.lexer.token_type() == "identifier")
        name = self.lexer.token_value()
        arguments = []
        self.lexer.advance()
        self.eat("(")
        while self.lexer.token_value() != ")":
            arguments.append(parse_expression(self))
            if self.lexer.token_value() == ",":
                self.lexer.advance()
        self.eat(")")
        return FunctionCall(name, arguments)

    def parse_array_subscript(self):
        self.verify(self.lexer.token_type() == "identifier")
        name = self.lexer.token_value()
        self.lexer.advance()
        self.eat("[")
        index = parse_expression(self)
        self.eat("]")
        return UnOp("DEREFERENCE", BinOp("ADD", name, index))

    def parse_statements(self):
        statements = []
        self.eat("{")
        while self.lexer.token_value() != "}":
            statements += self.parse_statement()
        self.eat("}")
        return statements

    def parse_statement(self):
        if self.lexer.token_value() in self.lexer.TYPES:
            rv = self.parse_var_dec(self.parse_type())
        elif self.lexer.token_value() == "if":
            rv = [self.parse_if()]
        elif self.lexer.token_value() == "while":
            rv = [self.parse_while()]
        elif self.lexer.token_value() == "return":
            rv = [self.parse_return()]
        # elif (
        #     self.lexer.token_type() == "identifier"
        #     and self.lexer.future_token_value() == "="
        #     and self.lexer.future_token_value(2) != "="
        # ):
        #     rv = [self.parse_assignment()]
        else:
            rv = [parse_expression(self)]
            if (
                self.lexer.token_value() == "="
            ):
                rv = [self.parse_assignment(rv[0])]
            else:
                self.eat(";")
        return rv

    def parse_assignment(self, destination):
        # destination = self.lexer.token_value()
        # self.lexer.advance()
        self.eat("=")
        source = parse_expression(self)
        self.eat(";")
        return Assignment(destination, source)

    def parse_if(self):
        cond_blocks = []
        else_body = None
        self.eat("if")
        condition = parse_expression(self)
        body = self.parse_statements()
        cond_blocks.append(CondBlock(condition, body))
        while (
            self.lexer.token_value() == "else"
            and self.lexer.future_token_value() == "if"
        ):
            self.lexer.advance()
            self.lexer.advance()
            condition = parse_expression(self)
            body = self.parse_statements()
            cond_blocks.append(CondBlock(condition, body))
        if self.lexer.token_value() == "else":
            self.lexer.advance()
            else_body = self.parse_statements()
        return IfStatement(condition, cond_blocks, else_body)

    def parse_while(self):
        self.eat("while")
        condition = parse_expression(self)
        body = self.parse_statements()
        return WhileLoop(condition, body)

    def parse_return(self):
        self.eat("return")
        rv = Return(parse_expression(self))
        self.eat(";")
        return rv

    def eat(self, value):
        self.verify(self.lexer.token_value() == value)
        self.lexer.advance()

    def unexpected_token(self):
        raise Exception(
            f"Unexpected token at line {self.lexer.token_line()} : {self.lexer.token_value()}"
        )

    def verify(self, condition):
        if not condition:
            raise Exception(
                f"Unexpected token at line {self.lexer.token_line()} : {self.lexer.token_value()}"
            )
if __name__ == "__main__":
    with open("./programs/example.c") as f:
        lexer = Lexer(f)
    parser = Parser(lexer)
    parser.parse()

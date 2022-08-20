from lexer import Lexer
from AST_types import *


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.AST = []

    def parse(self):
        self.parse_file()

    def parse_file(self):
        while self.lexer.has_more_tokens():
            type = self.parse_type()
            # function
            if (not self.lexer.future_token_value() in ["=", ";"]):
                self.AST.append(self.parse_function_dec(type))
            else:
                self.AST.append(self.parse_var_dec(type))

        for child in self.AST:
            print(child)

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
        if (self.lexer.future_token_value() == "="):
            return self.parse_var_dec_with_value(type)
        else:
            return self.parse_var_dec_without_value(type)

    def parse_type(self):
        self.verify(self.lexer.token_value() in self.lexer.TYPES)
        type = self.lexer.token_value()
        self.lexer.advance()
        return type

    def parse_var_dec_with_value(self, type):
        # name
        self.verify(self.lexer.token_type() == "identifier")
        name = self.lexer.token_value()
        self.lexer.advance()

        self.eat("=")
        expression = self.parse_expression()
        self.eat(";")
        return VarDecWithValue(type, name, expression)

    def parse_var_dec_without_value(self, type):
        # name
        self.verify(self.lexer.token_type() == "identifier")
        name = self.lexer.token_value()
        self.lexer.advance()

        self.eat(";")
        return VarDecWithoutValue(type, name)

    def parse_param_list(self):
        param_list = []
        self.eat("(")
        if (self.lexer.token_value() != ")"):
            type = self.parse_type()
            name = self.lexer.token_value()
            self.lexer.advance()
            param_list.append((type, name))
        while (self.lexer.token_value() == ","):
            self.eat(",")
            type = self.parse_type()
            name = self.lexer.token_value()
            self.lexer.advance()
            param_list.append((type, name))
        self.eat(")")
        return param_list

    def parse_statements(self):
        statements = []
        self.eat("{")
        while self.lexer.token_value() != "}":
            if (self.lexer.token_value() in self.lexer.TYPES):
                varDec = self.parse_var_dec(self.parse_type())
                statements.append(varDec)
            else:
                print(self.parse_expression())
                self.eat(";")
        self.eat("}")
        return statements

    def parse_expression(self):
        return BinOp(None, self.parse_term(), self.parse_expression_r())

    def parse_expression_r(self):
        if (self.lexer.token_value() in ["+", "-"]):
            op = self.lexer.token_value()
            self.lexer.advance()
            return BinOp(self.lexer.token_value(), self.parse_term(), self.parse_expression_r())

    def parse_term(self):
        return BinOp(None, self.parse_factor(), self.parse_term_r())

    def parse_term_r(self):
        if (self.lexer.token_value() in ["*", "/"]):
            op = self.lexer.token_value()
            self.lexer.advance()
            self.parse_factor()
            self.parse_term_r()
            print(op)

    def parse_factor(self):
        if (self.lexer.token_value() == "("):
            self.eat("(")
            expression = self.parse_expression()
            self.eat(")")
            return expression
        else:
            self.verify(self.lexer.token_type() == "integerConstant")
            constant = self.lexer.token_value()
            self.lexer.advance()
            print(constant)
            return constant

    def eat(self, value):
        self.verify(self.lexer.token_value() == value)
        self.lexer.advance()

    def unexpected_token(self):
        raise Exception(
            f"Unexpected token at line {self.lexer.token_line()} : {self.lexer.token_value()}")

    def verify(self, condition):
        if (not condition):
            raise Exception(
                f"Unexpected token at line {self.lexer.token_line()} : {self.lexer.token_value()}")


with open("./example.c") as f:
    lexer = Lexer(f)
parser = Parser(lexer)
parser.parse()

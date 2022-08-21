from AST_types import *

UNARY_OPS = {"-": "ARITHMETIC_NEGATION", "~": "BITWISE_NEGATION",
             "!": "LOGICAL_NEGATION", "*": "DEREFERENCE", "&": "ADDRESS_OF"}

OR = {"||": "OR"}
AND = {"&&": "AND"}
EQUALITY = {"==": "EQUALITY", "!=": "INEQUALITY"}
RELATIONAL = {"<": "LESS_THAN", ">": "GREATER_THAN",
              "<=": "LESS_THAN_OR_EQUAL", ">=": "GREATER_THAN_OR_EQUAL"}
ADDITIVE = {"+": "ADD", "-": "SUBTRACT"}
MULTIPLICATIVE = {"*": "MULTIPLY", "/": "DIVIDE"}

# PRECEDENCE = [OR, AND, EQUALITY, RELATIONAL, ADDITIVE, MULTIPLICATIVE]
PRECEDENCE = [ADDITIVE, MULTIPLICATIVE]


def parse_factor(self):
    if (self.lexer.token_value() == "("):
        self.eat("(")
        expression = parse_expression(self)
        self.eat(")")
        return expression
    elif self.lexer.token_value() in ["-", "~", "!", "*", "&"]:
        op = self.lexer.token_value()
        self.lexer.advance()
        factor = parse_factor(self)
        return UnOp(op, factor)
    else:
        self.verify(self.lexer.token_type() == "integerConstant")
        constant = self.lexer.token_value()
        self.lexer.advance()
        return str(constant)


def generate_expression_parsers():
    expression_parsers = [parse_factor]
    for i, operations in enumerate(PRECEDENCE[::-1]):
        def parse_arbitrary_expression(self, i=i, operations=operations, expression_parsers=expression_parsers):
            expr = expression_parsers[i](self)
            while (self.lexer.token_value() in operations.keys()):
                op = self.lexer.token_value()
                self.lexer.advance()
                expr_term = expression_parsers[i](self)
                expr = BinOp(op, expr, expr_term)
            return expr
        expression_parsers.append(parse_arbitrary_expression)
    return expression_parsers


parse_expression = generate_expression_parsers()[-1]
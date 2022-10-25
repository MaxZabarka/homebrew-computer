from AST_types import *
import helpers

UNARY_OPS = {
    "-": "ARITHMETIC_NEGATION",
    "~": "BITWISE_NEGATION",
    "!": "NOT",
    "*": "DEREFERENCE",
    # "&": "ADDRESS_OF",
}

BITWISE_AND = {"&": "BITWISE_AND"}
OR = {"|": "OR"}
AND = {"&&": "AND"}
EQUALITY = {"==": "EQUAL", "!=": "INEQUAL"}
RELATIONAL = {
    "<": "LESS_THAN",
    ">": "GREATER_THAN",
    "<=": "LESS_THAN_OR_EQUAL",
    ">=": "GREATER_THAN_OR_EQUAL",
}
SHIFT = {"<<": "LEFT_SHIFT"}
ADDITIVE = {"+": "ADD", "-": "SUBTRACT"}
MULTIPLICATIVE = {"*": "MULTIPLY", "/": "DIVIDE"}

PRECEDENCE = [OR, BITWISE_AND, AND, EQUALITY,
              RELATIONAL, SHIFT, ADDITIVE, MULTIPLICATIVE]


def parse_factor(self):
    if self.lexer.token_value() == "(":
        self.eat("(")
        expression = parse_expression(self)
        self.eat(")")
        return expression
    elif self.lexer.token_value() in UNARY_OPS.keys():
        op = UNARY_OPS[self.lexer.token_value()]
        self.lexer.advance()
        factor = parse_factor(self)
        return UnOp(op, factor)
    elif (
        self.lexer.token_type() == "identifier"
        and self.lexer.future_token_value() == "("
    ):
        return self.parse_function_call()
    elif (
        self.lexer.token_type() == "identifier"
        and self.lexer.future_token_value() == "["
    ):
        return self.parse_array_subscript()
    elif self.lexer.token_type() == "identifier":
        identifier = self.lexer.token_value()
        self.lexer.advance()
        return str(identifier)
    else:
        self.verify(self.lexer.token_type() == "integerConstant")
        constant = self.lexer.token_value()
        self.lexer.advance()
        return Constant(helpers.parse_number(constant))


def generate_expression_parsers():
    expression_parsers = [parse_factor]
    for i, operations in enumerate(PRECEDENCE[::-1]):

        def parse_arbitrary_expression(
            self, i=i, operations=operations, expression_parsers=expression_parsers
        ):
            first_chars = []
            second_chars = []
            for operator in operations.keys():
                first_chars.append(operator[0])
                if len(operator) > 1:
                    second_chars.append(operator[1])

            expr = expression_parsers[i](self)
            while self.lexer.token_value() in first_chars:
                op = self.lexer.token_value()
                if self.lexer.future_token_value() in second_chars:
                    self.lexer.advance()
                    op += self.lexer.token_value()
                if (op in operations.keys()):                    
                    op = operations[op]
                else:
                    return expr
                self.lexer.advance()

                expr_term = expression_parsers[i](self)
                expr = BinOp(op, expr, expr_term)
            return expr

        expression_parsers.append(parse_arbitrary_expression)
    return expression_parsers


parse_expression = generate_expression_parsers()[-1]

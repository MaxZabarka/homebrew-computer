class FunctionDec:
    def __init__(self, return_type, name, params, body):
        self.return_type = return_type
        self.name = name
        self.params = params
        self.body = body


class VarDec:
    def __init__(self, type, name, array_size=0):
        self.type = type
        self.name = name
        self.array_size = array_size


class IntegerConstant:
    def __init__(self, value):
        self.value = int(value)


class Assignment:
    def __init__(self, destination, source):
        self.destination = destination
        self.source = source


class UnOp:
    def __init__(self, op, a):
        self.a = a
        self.op = op


class WhileLoop:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class CondBlock:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class BinOp:
    def __init__(self, op, a, b):
        self.a = a
        self.b = b
        self.op = op


class IfStatement:
    def __init__(self, condition, cond_blocks, else_body=None):
        self.condition = condition
        self.cond_blocks = cond_blocks
        if else_body:
            self.else_body = else_body


class Type:
    def __init__(self, type, pointer_amount):
        self.type = type
        self.pointer_amount = pointer_amount
    def __repr__(self):
        return f"<Type: {self.type}{'*'*self.pointer_amount}>"


class Parameter:
    def __init__(self, type, identifier):
        self.type = type
        self.identifier = identifier


class Constant:
    def __init__(self, value):
        self.value = value


class Return:
    def __init__(self, value):
        self.value = value


class FunctionCall:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments


class ArraySubscript:
    def __init__(self, name, index):
        self.name = name
        self.index = index

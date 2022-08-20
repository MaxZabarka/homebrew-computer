class FunctionDec:
    def __init__(self, return_type, name, params, statements):
        self.return_type = return_type
        self.name = name
        self.params = params
        self.statements = statements

   
class VarDecWithoutValue:
    def __init__(self, type, name):
        self.type = type
        self.name = name


class VarDecWithValue:
    def __init__(self, type, name, expression):
        self.type = type
        self.name = name
        self.expression = expression

class UnOp:
    def __init__(self, op, a):
        self.a = a
        self.op = op


class BinOp:
    def __init__(self, op, a, b):
        self.a = a
        self.b = b
        self.op = op


class Type:
    def __init__(self, type, pointer_amount):
        self.type = type
        self.pointer_amount = pointer_amount


class Parameter:
    def __init__(self, type, identifier):
        self.type = type
        self.identifier = identifier

class Constant:
    def __init__(self, value):
        self.value = value


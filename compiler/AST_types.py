class FunctionDec:
    def __init__(self, return_type, name, params, statements):
        self.return_type = return_type
        self.name = name
        self.params = params
        self.statements = statements

    def __repr__(self):
        return f"FunctionDec {self.return_type} {self.name} {self.params} \n\t{self.statements}"


class VarDecWithoutValue:
    def __init__(self, type, name):
        self.type = type
        self.name = name

    def __repr__(self):
        return f"VarDec {self.type} {self.name}"


class VarDecWithValue:
    def __init__(self, type, name, expression):
        self.type = type
        self.name = name
        self.expression = expression

    def __repr__(self):
        return f"VarDec {self.type} {self.name} {self.expression}"


class Op:
    def __init__(self, op, a):
        self.a = a
        self.op = op

    def __repr__(self):
        return f"Op {self.op} {self.a}"


class BinOp:
    def __init__(self, op, a, b):
        self.a = a
        self.b = b
        self.op = op

    def __repr__(self):
        return f"Op {self.op} \n\tA: {self.a}, \n\tB: {self.b}"

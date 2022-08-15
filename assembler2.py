import re
from constants import LOADS, ENABLES

# Reverse keys and values
ENABLES = {v: k for k, v in ENABLES.items()}
LOADS = {v: k for k, v in LOADS.items()}

# ssss c m
# TODO add more operations (64)
ALU_OPERATIONS = {
    "A + B": "000110",
    "A - 1": "111110",
    "A + 1": "000000",
    "A - B": "011000",
}

# Remove whitespace from ALU operations
for key in ALU_OPERATIONS.copy():
    ALU_OPERATIONS[re.sub("\s+", "", key)] = ALU_OPERATIONS.pop(key)


with open('source.zab', 'r') as file:
    data = file.read()


class Tokenizer:
    def __init__(self, data):
        self.current_instruction = 0
        self.current_token = 0
        self.instructions = data.split("\n")
        print(self.instructions)

        for instruction in self.instructions:
            if instruction[-1] == "":
                del instruction[-1]

    def get_next_token(self):
        next_token = re.split("([,=])", self.instructions[self.current_instruction])[
            self.current_token]
        self.current_token += 1
        return re.sub('\s+', '', next_token)

    def eat(self, value):
        if self.get_next_token != value:
            raise Exception("Could not eat token")


    
    def next_token_exists(self):
        return self.current_token >= len(self.instructions[self.current_instruction])

    def next_instruction(self):
        self.current_instruction += 1


# class Lexer:
#     def __init__(self, tokenizer):
#         self.tokenizer = tokenizer

#     def analyze_instruction(self):
#         instruction_type = None
#         token = self.tokenizer.get_next_token()
#         if token in LOADS:
#             self.tokenizer.eat("=")
#             if self.tokenizer.get_next_token():


#         elif token in ALU_OPERATIONS:
#             instruction_type = "COMPUTE_WITHOUT_DESTINATION"

#         return instruction_type



tokenizer = Tokenizer(data)
print(tokenizer.get_next_token())
print(tokenizer.get_next_token())
print(tokenizer.get_next_token())

# print(tokenizer.get_next_tokesn())
# print(tokenizer.next_token_exists())

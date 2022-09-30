#!/usr/bin/env python3.10

import tempfile
import os
from constants import ENABLES, JUMPS, LOADS, JUMP_NAMES
import helpers
import check_file
import argparse

# Reverse keys and values
ENABLES = {v: k for k, v in ENABLES.items()}
LOADS = {v: k for k, v in LOADS.items()}

# B = C register
# A = B register
EXPRESSIONS = {
    "B+C": "100110",
    "B-1": "111110",
    "B+1": "000000",
    "B-C": "011000",
    "B-C-1": "011010"
}


class Tokenizer:
    SYMBOLS = ["=", ",", "(", ")", "+", "-", "~", "|", "^", "^", ":", "."]
    KEYWORDS = ["AHigh", "ALow", "B", "C", "RAM", "IRHigh", "JEQ",
                "JLT", "JNE", "JEQ", "JGT", "JGE", "JC", "JNC", "JMP", "l", "h", "#origin"]

    def __init__(self, input_file):
        temp_file = os.path.join(tempfile.gettempdir(), "removed_comments")
        with open(input_file, "r") as source:
            with open(temp_file, 'w', encoding='utf-8') as temp:
                temp.write(helpers.remove_comments(source.read()))
        with open(temp_file, 'r') as f:
            self.tokens = []
            token = ""
            while True:
                c = f.read(1)

                if c in self.SYMBOLS or c.isspace() or not c:
                    if (len(token) > 0):
                        if (token in self.KEYWORDS):
                            self.tokens.append((token, "keyword"))
                            token = ""
                        elif (token.isidentifier()):
                            self.tokens.append((token, "identifier"))
                            token = ""
                        elif (not helpers.parse_number(token) is False):
                            self.tokens.append((token, "constant"))
                            token = ""
                        elif token.isspace():
                            pass
                        else:
                            raise SyntaxError("Unknown token: " + token)

                    if c in self.SYMBOLS:
                        self.tokens.append((c, "symbol"))
                    if not c:
                        break
                    continue

                token += c

            self.current_token = 0
        os.remove(temp_file)

    def has_more_tokens(self):
        return not self.current_token == len(self.tokens)

    def advance(self):
        self.current_token += 1

    def token_type(self):
        return self.tokens[self.current_token][1]

    def token_value(self):
        return self.tokens[self.current_token][0]

    def future_token_type(self, i=1):
        return self.tokens[self.current_token+i][1]

    def future_token_value(self, i=1):
        return self.tokens[self.current_token+i][0]


class Assembler:
    def __init__(self, input_file, logisim_format=False):
        self.tokenizer = Tokenizer(input_file)
        self.input_file = input_file
        self.logisim_format = logisim_format
        self.symbol_table = {}
        self.current_byte = 0
        
        # assemble everything twice to build symbol table lol
        self.step = 0
        self.assemble()
        self.step = 1
        self.assemble()
        self.write_to_file()

    def write_to_file(self):
        print(self.symbol_table)
        if (self.logisim_format):
            with open(os.path.splitext(self.input_file)[0]+'.txt', "w") as file:
                file.write("v3.0 hex words plain\n")
                file.write(self.output)
        else:
            with open(os.path.splitext(self.input_file)[0]+".bin", "wb") as file:
                for hex_byte in self.output.strip().split(" "):
                    print(hex_byte)
                    # print(int(hex_byte, 16).to_bytes(1, byteorder="little"))
                    file.write(int(hex_byte, 16).to_bytes(1, byteorder="little"))

    def write_instruction(self, bits):
        if len(bits) == 8:
            self.current_byte += 1
            if self.step == 0:
                return
            print(bits)

            self.output += hex(int(bits, 2))[2:].zfill(2) + " "
        else:
            self.current_byte += 2
            low_byte = bits[0:8]
            high_byte = bits[8:16]
            if self.step == 0:
                return
            print(low_byte, high_byte)

            self.output += hex(int(low_byte, 2))[2:].zfill(2) + " "
            self.output += hex(int(high_byte, 2))[2:].zfill(2) + " "

    def assemble(self):
        self.origin = 0
        self.tokenizer.current_token = 0
        self.output = ""
        # self.output = "v3.0 hex words plain\n"
        while self.tokenizer.has_more_tokens():
            self.assemble_instruction()
        self.symbol_table["STACK_POINTER_LOW"] = 0 + self.origin
        self.symbol_table["STACK_POINTER_HIGH"] = 1 + self.origin

        self.symbol_table["LOCAL_LOW"] = 2 + self.origin
        self.symbol_table["LOCAL_HIGH"] = 3 + self.origin

        self.symbol_table["ARGUMEN_LOW"] = 4 + self.origin
        self.symbol_table["ARGUMENT_HIGH"] = 5 + self.origin

    def assemble_instruction(self):
        self.compiled_instruction = list("0"*16)

        if (self.tokenizer.token_type() == "keyword" and
            self.tokenizer.token_value() in LOADS
            ):
            if self.tokenizer.future_token_value(2) != "(":
                self.assemble_move()
            else:
                self.assemble_compute()
        elif (self.tokenizer.token_type() == "identifier"):
            self.assemble_identifier()
            return
        elif (self.tokenizer.token_type() == "constant"):
            self.compiled_instruction = list("0"*16)
            self.assemble_data()
        elif (self.tokenizer.token_type() == "keyword" and
              self.tokenizer.token_value() in JUMP_NAMES):
            self.assemble_jump()
        elif (self.tokenizer.token_type() == "keyword" and
              self.tokenizer.token_value() == "#origin"):
            self.assemble_origin()
            return
        elif self.tokenizer.token_value() == "(":
            self.assemble_compute()
        else:
            raise Exception("Unexpected token: " +
                            self.tokenizer.token_value())
        self.write_instruction("".join(self.compiled_instruction))

    def assemble_load(self):
        self.compiled_instruction[1:4] = LOADS[self.tokenizer.token_value()]
        self.tokenizer.advance()

        if (self.tokenizer.token_type() == "symbol" and
                self.tokenizer.token_value() == "="):
            self.tokenizer.advance()
        else:
            raise Exception("Expected '=', found: " +
                            self.tokenizer.token_value())

    def assemble_origin(self):
        self.tokenizer.advance()
        if (self.tokenizer.token_type() != "constant"):
            raise Exception("Unexpected token: " +
                            self.tokenizer.token_value())
        self.origin = helpers.parse_number(self.tokenizer.token_value())
        self.tokenizer.advance()

    def assemble_move(self):
        self.assemble_load()

        if (self.tokenizer.token_type() == "constant"):
            binary_value = bin(helpers.parse_number(
                self.tokenizer.token_value()))[2:].zfill(8)
            self.compiled_instruction[8:16] = binary_value
            self.compiled_instruction[4:7] = ENABLES["IRHigh"]

            self.tokenizer.advance()
        elif (self.tokenizer.token_type() == "keyword"):
            if (self.tokenizer.token_value() in ENABLES):
                self.compiled_instruction[4:7] = ENABLES[self.tokenizer.token_value(
                )]
                self.tokenizer.advance()

            else:
                raise Exception("Unable to use as a source: " +
                                self.tokenizer.token_value())
        elif (self.tokenizer.token_type() == "identifier"):
            if (self.step == 0):
                self.tokenizer.advance()
                self.tokenizer.advance()
                self.tokenizer.advance()

            else:
                self.compiled_instruction[4:7] = ENABLES["IRHigh"]
                symbol_value = self.symbol_table[self.tokenizer.token_value()]
                high_byte = bin(symbol_value & 0xFF00)[2:].zfill(8)
                low_byte = bin(symbol_value & 0x00FF)[2:].zfill(8)
                if (self.tokenizer.future_token_value() != "."):
                    raise Exception("Unexpected token: " +
                                    self.tokenizer.token_value())
                self.tokenizer.advance()
                if (self.tokenizer.future_token_value() == "l"):
                    self.compiled_instruction[8:16] = low_byte
                elif (self.tokenizer.future_token_value() == "h"):
                    self.compiled_instruction[8:16] = high_byte
                else:
                    raise Exception("Unexpected token: " +
                                    self.tokenizer.token_value())
                self.tokenizer.advance()
                self.tokenizer.advance()
        else:
            raise Exception("Unexpected token: " +
                            self.tokenizer.token_value())

    def assemble_data(self):
        binary_value = bin(helpers.parse_number(
            self.tokenizer.token_value()))[2:].zfill(8)
        self.compiled_instruction = binary_value
        self.tokenizer.advance()

    def assemble_compute(self):
        self.compiled_instruction[0] = "1"

        if (self.tokenizer.token_value() == "("):
            self.assemble_expression()
            if (self.tokenizer.token_value() == ","):
                self.tokenizer.advance()
                self.assemble_jump()
        else:
            self.assemble_load()
            self.assemble_expression()

    def assemble_expression(self):
        expression = ""
        if (self.tokenizer.token_value() != "("):
            raise Exception("Unexpected token: " +
                            self.tokenizer.token_value())
        self.tokenizer.advance()
        while (self.tokenizer.token_value() != ")"):
            expression += self.tokenizer.token_value()
            self.tokenizer.advance()
        self.tokenizer.advance()
        if (not expression in EXPRESSIONS):
            raise Exception("Unknown expression: " + expression)
        self.compiled_instruction[8:14] = list(EXPRESSIONS[expression])

    def assemble_source(self):
        pass

    def assemble_jump(self):
        self.compiled_instruction[0] = "1"
        self.compiled_instruction[4:8] = JUMP_NAMES[self.tokenizer.token_value(
        )]
        self.tokenizer.advance()

    def assemble_identifier(self):
        if (self.step == 0):
            identifier = self.tokenizer.token_value()
            if (self.tokenizer.future_token_value() != ":"):
                raise Exception("Unexpected token: " +
                                self.tokenizer.token_value())
            if (identifier in self.symbol_table):
                raise Exception(
                    "Cannot have duplicate identifier: " + identifier)
            self.symbol_table[identifier] = self.current_byte + self.origin
        self.tokenizer.advance()
        self.tokenizer.advance()


parser = argparse.ArgumentParser(
    description="Assemble a source file into machine code")

parser.add_argument("file", help="The source file to assemble")
parser.add_argument('-l', '--logisim', action='store_true',
                    help="Assemble into a format compatible with Logisim")

args = parser.parse_args()

file_name = check_file.check_file(args.file)
Assembler(file_name, args.logisim)

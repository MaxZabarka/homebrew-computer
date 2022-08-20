#!/usr/bin/env python3.10

from curses.ascii import isdigit
from typing import Set
import helpers
import os
import tempfile

SYMBOLS = {"{", "}", "(", ")", "[", "]", ".", ",", ";",
            "+", "-", "*", "/", "&&", "||", "<", ">", "<=",
            ">=", "=", "==", "~", "!"}

SYMBOL_CHARS = set()

for symbol in SYMBOLS:
    for char in symbol:
        SYMBOL_CHARS.add(char)

print(SYMBOL_CHARS)

TYPES = ["int", "int16", "char", "bool", "void"]
KEYWORDS = [ "true", "false", "if", "void"
            "else", "while", "return", "struct"] + TYPES
class Lexer:


    def __init__(self, input_file):
        temp_file = os.path.join(tempfile.gettempdir(), "removed_comments")
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(helpers.remove_comments(input_file.read()))
        with open(temp_file, 'r') as f:
            self.tokens = []
            token = ""
            isString = False
            lineNumber = 1
            c = f.read(1)
            while True:
                if not c:
                    break
                

                if (c.isspace()):
                    c = f.read(1)
                    continue
                if (c.isalpha()):
                    token += c
                    c = f.read(1)
                    while (c.isalnum()):
                        token+=c
                        c = f.read(1)
                    print(token)
                    token = ""
                    continue
                elif (c.isdigit()):
                    pass
                elif (c in SYMBOL_CHARS):
                    token += c
                    c = f.read(1)
                    while (c in SYMBOL_CHARS):
                        token+=c
                        c = f.read(1)
                    if token not in SYMBOLS:
                        raise Exception
                    token = ""
                    continue
                else:
                    raise Exception
                token +=  c
            # while True:
            #     c = f.read(1)
            #     if not c:
            #         break

            #     if c == "\n":
            #         lineNumber += 1

            #     if c == "\"":
            #         if isString:
            #             self.tokens.append(
            #                 (token, "stringConstant", lineNumber))
            #             token = ""
            #         isString = not isString
            #         continue

            #     if isString:
            #         token += c
            #         continue

            #     if c in self.SYMBOLS or c.isspace():
            #         token = token.strip()
            #         if (len(token) > 0):
            #             if (token in self.KEYWORDS):
            #                 self.tokens.append((token, "keyword", lineNumber))
            #                 token = ""
            #             elif (token.isidentifier()):
            #                 self.tokens.append(
            #                     (token, "identifier", lineNumber))
            #                 token = ""
            #             elif (token.isnumeric()):
            #                 self.tokens.append(
            #                     (token, "integerConstant", lineNumber))
            #                 token = ""
            #             elif token.isspace():
            #                 pass
            #             else:
            #                 raise SyntaxError("Unknown token: " + token)

            #         if c in self.SYMBOLS:
            #             self.tokens.append((c, "symbol", lineNumber))
            #         continue
            #     token += c
            self.currentToken = 0
        os.remove(temp_file)

    def has_more_tokens(self):
        return not self.currentToken == len(self.tokens)

    def advance(self):
        self.currentToken += 1

    def token_type(self):
        return self.tokens[self.currentToken][1]

    def token_value(self):
        return self.tokens[self.currentToken][0]

    def token_line(self):
        return self.tokens[self.currentToken][2]

    def future_token_type(self, i=1):
        return self.tokens[self.currentToken+i][1]

    def future_token_value(self, i=1):
        return self.tokens[self.currentToken+i][0]


if __name__ == "__main__":
    with open("example.c") as f:
        lexer = Lexer(f)

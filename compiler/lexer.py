#!/usr/bin/env python3.10

from curses.ascii import isdigit
from typing import Set
import helpers
import os
import tempfile


class Lexer:
    SYMBOLS = {
        "{",
        "}",
        "(",
        ")",
        "[",
        "]",
        ".",
        ",",
        ";",
        "+",
        "-",
        "*",
        "/",
        "&",
        "|",
        "<",
        ">",
        "=",
        "~",
        "!",
        "^"
    }

    TYPES = ["int", "char", "bool", "void"]
    KEYWORDS = ["true", "false", "if", "void" "else", "while", "return", "struct"] + TYPES


    def __init__(self, input_file):
        temp_file = os.path.join(tempfile.gettempdir(), "removed_comments")
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(helpers.remove_comments(input_file.read()))
        with open(temp_file, 'r') as f:
            self.tokens = []
            token = ""
            isString = False
            lineNumber = 1
            while True:
                c = f.read(1)
                if not c:
                    break

                if c == "\n":
                    lineNumber += 1

                if c == "\"":
                    if isString:
                        self.tokens.append(
                            (token, "stringConstant", lineNumber))
                        token = ""
                    isString = not isString
                    continue

                if isString:
                    token += c
                    continue

                if c in self.SYMBOLS or c.isspace():
                    token = token.strip()
                    if (len(token) > 0):
                        if (token in self.KEYWORDS):
                            self.tokens.append((token, "keyword", lineNumber))
                            token = ""
                        elif (token.isidentifier()):
                            self.tokens.append(
                                (token, "identifier", lineNumber))
                            token = ""
                        elif (not helpers.parse_number(token) is False):
                            self.tokens.append(
                                (token, "integerConstant", lineNumber))
                            token = ""
                        elif token.isspace():
                            pass
                        else:
                            raise SyntaxError("Unknown token: " + token)

                    if c in self.SYMBOLS:
                        self.tokens.append((c, "symbol", lineNumber))
                    continue
                token += c
            self.currentToken = 0
            for token in self.tokens:
                print(token)
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

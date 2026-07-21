# The lexer and parser

We switch worlds now. The last six chapters were voltages and chips; this one is the front half of a compiler. If you have read [Crafting Interpreters](https://craftinginterpreters.com/), this chapter will feel like coming home, because that book is where I learned most of what follows, and my parser is a straightforward relative of its jlox parser, written in Python and aimed at C.

The compiler lives in `compiler/` and accepts a subset of C: `int`, `char`, and `bool` (all secretly bytes), pointers, arrays, `if` and `while`, functions with arguments and locals. The honest inventory of what works is the test suite, 24 programs in `tests/`, and I will point out the missing pieces as we meet them.

## The lexer

`compiler/lexer.py` does the unglamorous first job: strip comments, then walk the source one character at a time and group characters into tokens. Each token is a `(value, type, line)` tuple, and there are five types: keyword, identifier, integer constant, string constant, and symbol. `while (i)` becomes a keyword, a symbol, an identifier, a symbol. Nothing here would surprise anyone who has written a tokenizer; its entire purpose is to let the parser think in words instead of characters.

## The parser

`compiler/parser.py` is a recursive-descent parser, the handwritten kind: one method per construct, each method consuming the tokens it expects and building a node. `parse_function_dec`, `parse_var_dec`, `parse_if`, `parse_while`, `parse_return`, and so on, with the node classes in `compiler/AST_types.py`. When `parse_if` runs, it eats `if`, eats `(`, asks the expression parser for a condition, eats `)`, and recurses into the body. The call stack of the parser mirrors the nesting of the program, which is the whole charm of recursive descent.

Expressions are where parsers earn their pay, because precedence has to come from somewhere. `2 + 3 * 4` must parse as `2 + (3 * 4)`, and the classic hand-written answer is a ladder of functions, one per precedence level, each calling the next tighter one. Crafting Interpreters walks you through writing that ladder by hand. I got lazy in the best way: `compiler/parse_expression.py` holds a table of operator tiers, from `|` at the loosest down through `&&`, equality, relational, shifts, additive, and multiplicative, and a generator function builds the ladder from the table at import time. One parsing function per tier, manufactured in a loop. Changing precedence means editing a list.

One design choice here saves the whole back half of the compiler some work. Array subscripts are desugared during parsing: `arr[i]` never reaches the code generator, because the parser rewrites it as `*(arr + i)` using a 16-bit pointer addition. Subscripts are pointer arithmetic in C anyway; this compiler just makes that identity literal, and later stages only ever see pointers.

## Draw me a tree

Now the part of this chapter I am genuinely fond of. A parser's output is a tree, and a tree you cannot see is a tree you cannot debug. While writing the parser I kept mis-building nodes in ways that were invisible in print statements, so I built myself a visualizer. `compiler/draw_ast.py` walks the node objects with `vars()` and hands the structure to Graphviz, and the parser calls it on every single compile, writing `output.png` next to the output. It started as a debugging tool and became a permanent feature: every compile draws its own syntax tree, whether you asked for it or not.

Here is `programs/example.c`, an `add` function and a `main` that calls it:

```c
int add(int a, int b) {
    return a + b;
}

int main()
{
    add(1, 2);
}
```

![The AST of example.c as drawn by draw_ast.py](../media/ast-example.png)

Blue ovals are leaf values, black ovals are node types, edge labels are field names. And a bigger program from the test suite, where you can watch a whole function unfold sideways:

![The AST of a larger test program](../media/ast.png)

## What is missing, on purpose

No `for` loops (use `while`). No structs (the keyword lexes and stops there). No casts, no strings past the lexer, no globals with initializers. And, most interesting of all, the parser happily accepts `*` and `/` in expressions, but nothing below the parser can execute them: the machine has no multiply instruction, remember. What happens to multiplication is a two-chapter story: first we need to see what the code generator turns this tree into, and then, in chapter 11, how software does arithmetic the hardware refuses to.

Next: [Code generation and the VM](10-code-generation-and-the-vm.md)

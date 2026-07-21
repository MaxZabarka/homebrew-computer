# The assembler

`assembler.py` turns `.zab` assembly into raw machine code. It is around 300 lines: a tokenizer and a single `Assembler` class that runs the source through twice.

## The language

One statement per construct, no addressing modes, no macros:

| Form | Example | Meaning |
| --- | --- | --- |
| move constant | `AHigh = 128` | load an 8-bit immediate |
| move register | `B = RAM` | one register drives the bus, one loads |
| move symbol byte | `ALow = loop.l` | low or high byte of a symbol's address |
| compute | `RAM = (B+C)` | ALU expression into a destination |
| compute and jump | `(B-C), JEQ` | evaluate, jump to the address in A if the condition holds |
| plain jump | `JMP` | unconditional jump to the address in A |
| label | `loop:` | bind a symbol to the current address |
| data | `0x55` | emit a literal byte |
| origin | `#origin 0x8000` | set the base added to subsequent labels |

Comments use C syntax and are stripped before tokenizing by the same `helpers.remove_comments` regex the compiler uses.

## Two passes

The constructor calls `assemble()` twice. Pass one emits nothing. It only advances a byte counter and records every `label:` in the symbol table at `current_byte + origin`. Pass two emits bytes, and by then every forward reference like `AHigh = end.h` can be resolved. The source comment is candid about the design: "assemble everything twice to build symbol table lol".

Six symbols are predefined before either pass so the VM's fixed addresses always resolve: STACK_POINTER through TEMP_2 at 0 through 5 (see [The VM layer](vm-layer.md)). The first `#origin` shifts these bases once, so RAM-resident code keeps its pointers inside RAM.

## Origins and split address spaces

`#origin` does not move the output cursor. Bytes are always emitted sequentially. It only changes the value that gets added to label definitions, and it can appear any number of times. The VM translator exploits this to keep two address spaces in one file: code labels are defined under `#origin 0` (ROM addresses) while the surrounding code is positioned under `#origin 32768` (RAM-based data arithmetic).

## Assembling a real program

`programs/mult.zab` is a hand-written loop that multiplies 30 by 5 through repeated addition, using labels, expressions, and conditional jumps. Assembling it:

![Assembling mult.zab and dumping the binary](media/term-assemble-mult.png)

The output is 64 bytes, each instruction a byte pair with the low byte first. Every construct in the table above appears somewhere in those bytes.

## Output format

`write_to_file` emits a flat binary, one byte at a time. The `-l` flag is declared in the argument parser for a Logisim-compatible format, but the current `write_to_file` ignores it, and the output is byte-identical with and without the flag. Logisim images for the ROM are instead produced by hand or loaded from the `v3.0 hex words plain` files like `bootloader.txt`.

## Where the code lives

The tokenizer and assembler are both in `assembler.py`. The instruction encodings it consumes are `LOADS`, `ENABLES`, and `JUMP_NAMES` in `constants.py` plus the `EXPRESSIONS` table at the top of `assembler.py`. The language notes are `information/instruction_set _v2.txt`, and `programs/` holds hand-written `.zab` files to read alongside them.

## Try it

```bash
python3 assembler.py programs/mult.zab -o mult.bin
xxd mult.bin
```

# Reference

An 8-bit computer with 16-bit addressing, designed in Logisim Evolution around 7400-series TTL chips, together with the complete software stack that targets it: a C compiler, a stack-based virtual machine, a two-pass assembler, generated microcode, and two emulators. These pages document every layer, from C source down to EEPROM contents. They are written for lookup, one page per subsystem, ordered here from the bottom of the stack up. For a narrative that reads in order, start with the [writeup](../writeup/01-why-i-built-this.md) instead.

![The emulator running fib.bin](../media/emulator-run.gif)

## The pages, bottom up

| Page | What it covers |
| --- | --- |
| [Overview](overview.md) | The whole stack in one diagram, the memory map, and how the pieces fit |
| [Hardware](hardware.md) | The Logisim chip inventory, the board partitioning, and the I2C experiment |
| [CPU and instruction set](cpu-and-instruction-set.md) | Registers, the two 16-bit instruction formats, jump conditions, a worked encoding |
| [The ALU](alu.md) | The 74181, chaining two 4-bit slices, the fixed expression table, flags |
| [Microcode and the control store](microcode-and-control-store.md) | How two Python scripts generate the 2^15-entry control tables for the EEPROMs |
| [Memory system](memory-system.md) | ROM, VRAM, and RAM regions, address decode, and the dual-port IDT7134 chips |
| [The compiler](compiler.md) | Lexer, parser, and code generator, with the supported C subset and a rendered AST |
| [The VM layer](vm-layer.md) | Stack machine semantics, segments, and the calling convention |
| [The assembler](assembler.md) | Two passes, symbols, the #origin directive, and the output format |
| [The emulators](emulators.md) | The headless instruction-stepped core and the React debugger app |
| [Running a program end to end](workflow-running-a-program.md) | Every command from a .c file to the emulator, with real output |
| [The test suite](workflow-test-suite.md) | Recompiling all 24 test programs and diffing against the committed binaries |

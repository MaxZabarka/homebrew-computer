# Homebrew computer documentation

An 8-bit computer with 16-bit addressing, designed from scratch in Logisim Evolution around 7400-series TTL chips, together with the complete software stack that targets it: a C compiler, a stack-based virtual machine, a two-pass assembler, generated microcode, and two emulators. The documentation comes in two tracks that deliberately overlap.

![The emulator running a compiled C program](media/emulator-run.gif)

## The writeup

Fifteen chapters that read in order, written in first person for someone who has done nand2tetris or follows Ben Eater. The writeup explains why the machine is shaped the way it is, and ends with what makes it unusual.

1. [Why I built this](writeup/01-why-i-built-this.md)
2. [What a 7400 chip actually is](writeup/02-what-a-7400-chip-actually-is.md)
3. [The shape of the machine](writeup/03-the-shape-of-the-machine.md)
4. [Registers and the bus](writeup/04-registers-and-the-bus.md)
5. [Two loads, one pointer](writeup/05-two-loads-one-pointer.md)
6. [The ALU](writeup/06-the-alu.md)
7. [Microcode and EEPROMs](writeup/07-microcode-and-eeproms.md)
8. [The memory system](writeup/08-the-memory-system.md)
9. [The lexer and parser](writeup/09-the-lexer-and-parser.md)
10. [Code generation and the VM](writeup/10-code-generation-and-the-vm.md)
11. [Multiplication, recursion, and other missing instructions](writeup/11-multiplication-recursion-and-other-missing-instructions.md)
12. [The assembler](writeup/12-the-assembler.md)
13. [The emulator core](writeup/13-the-emulator-core.md)
14. [The debugger](writeup/14-the-debugger.md)
15. [Architectural quirks](writeup/15-architectural-quirks.md)

## The reference

One page per subsystem, written for lookup, with field tables, file paths, and runnable commands. The [reference index](reference/index.md) orders them from the bottom of the stack up: [overview](reference/overview.md), [hardware](reference/hardware.md), [CPU and instruction set](reference/cpu-and-instruction-set.md), [ALU](reference/alu.md), [microcode and the control store](reference/microcode-and-control-store.md), [memory system](reference/memory-system.md), [compiler](reference/compiler.md), [VM layer](reference/vm-layer.md), [assembler](reference/assembler.md), [emulators](reference/emulators.md), and two workflows: [running a program end to end](reference/workflow-running-a-program.md) and [the test suite](reference/workflow-test-suite.md).

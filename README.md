## Documentation

The documentation lives in [docs/](docs/index.md), in two tracks.

The writeup, fifteen chapters that read in order:

1. [Why I built this](docs/writeup/01-why-i-built-this.md): the origin story and a tour of the whole stack
2. [What a 7400 chip actually is](docs/writeup/02-what-a-7400-chip-actually-is.md): the logic family the machine is made of
3. [The shape of the machine](docs/writeup/03-the-shape-of-the-machine.md): the wiring-difficulty principle, Harvard for simplicity, the bare minimum goal
4. [Registers and the bus](docs/writeup/04-registers-and-the-bus.md): six register bytes, one bus, and the two instruction formats
5. [Two loads, one pointer](docs/writeup/05-two-loads-one-pointer.md): 16-bit addressing over an 8-bit bus through the split A register
6. [The ALU](docs/writeup/06-the-alu.md): the 74181, two chained slices, and flags that evaporate
7. [Microcode and EEPROMs](docs/writeup/07-microcode-and-eeproms.md): the lookup-table control unit and the free conditional jump
8. [The memory system](docs/writeup/08-the-memory-system.md): the map, the EEPROM address decoder, and the dual-port VRAM
9. [The lexer and parser](docs/writeup/09-the-lexer-and-parser.md): recursive descent, generated precedence, and the AST visualizer
10. [Code generation and the VM](docs/writeup/10-code-generation-and-the-vm.md): why a stack machine sits in the middle
11. [Multiplication, recursion, and other missing instructions](docs/writeup/11-multiplication-recursion-and-other-missing-instructions.md): the algorithms that fill the hardware's gaps
12. [The assembler](docs/writeup/12-the-assembler.md): two passes and one file with two address spaces
13. [The emulator core](docs/writeup/13-the-emulator-core.md): the headless machine with a gate-level 74181
14. [The debugger](docs/writeup/14-the-debugger.md): stepping, speeds, breakpoints, and watching fib recurse
15. [Architectural quirks](docs/writeup/15-architectural-quirks.md): the parts that make this machine specifically this machine

The reference, one page per subsystem:

- [Overview](docs/reference/overview.md): the whole stack in one diagram and the memory map
- [Hardware](docs/reference/hardware.md): the Logisim chip inventory, the board partitioning, and the I2C experiment
- [CPU and instruction set](docs/reference/cpu-and-instruction-set.md): registers, the two instruction formats, jumps, a worked encoding
- [The ALU](docs/reference/alu.md): the 74181, slice chaining, expressions, and flags
- [Microcode and the control store](docs/reference/microcode-and-control-store.md): how the control tables are generated and what the address bits mean
- [Memory system](docs/reference/memory-system.md): ROM, VRAM, RAM, and the dual-port IDT7134
- [The compiler](docs/reference/compiler.md): the three stages, the supported C subset, and a rendered AST
- [The VM layer](docs/reference/vm-layer.md): stack semantics, segments, and the calling convention
- [The assembler](docs/reference/assembler.md): two passes, symbols, and #origin
- [The emulators](docs/reference/emulators.md): the headless core and the React debugger
- [Running a program end to end](docs/reference/workflow-running-a-program.md): every command from .c to the emulator
- [The test suite](docs/reference/workflow-test-suite.md): recompiling all 24 programs and diffing the results

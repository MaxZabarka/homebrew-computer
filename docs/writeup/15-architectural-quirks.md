# Architectural quirks

Every homebrew machine ends up with a personality, a handful of choices and accidents that make it specifically itself. This closing chapter collects mine in one place. Most have appeared somewhere in the previous fourteen chapters; here they get to stand next to each other, plus a few confessions that fit nowhere else.

## The control unit is a Python function

The machine's deepest quirk: there is no decode logic anywhere. The control unit is two EEPROMs and a 2-bit counter, and every branch decision the hardware will ever make was computed in advance by `SHOULD_JUMP` in `constants.py` and burned into a table. The same function runs in the emulator at run time. One Python function is simultaneously the hardware's wiring and the software's behavior, which still makes me smile. Chapter 7 tells the full story.

## Every compute instruction is armed to jump

There is no branch instruction in the instruction set, and there is also no instruction that cannot branch. Every compute carries a 4-bit condition field, checked for free because the flags are address bits into the control store. An unconditional `JMP` is just a compute whose condition is "always". The flip side: a jump cannot happen without a computation, and every branch target must be parked in A first, so generated code is full of the three-instruction ritual from chapter 5.

## One register faces all of memory

Every RAM read, every RAM write, and every jump goes through the split A register. Two address sources exist in the whole machine, the program counter and A. Hardware-wise it is the minimum possible wiring. Software-wise, A is the most contended resource on the machine, and the VM translator spends most of its emitted instructions just repointing it.

![The split A register forming a 16-bit pointer into the memory map](../media/fig-split-a.png)

## The video memory has two doors

VRAM is an IDT7134 dual-port RAM: two complete, independent ports into one 4KB block, one for the CPU and one for a display circuit, no arbitration anywhere. Most designs make video and CPU take turns; this one buys a strange chip so that neither ever waits. On the wiring scale from chapter 3, one exotic part beats a fistful of referee logic.

## The stack is 256 bytes, on purpose

The VM pins its entire stack inside one 256-byte page of RAM so that the high address byte is a constant 128 and all stack arithmetic fits in the 8-bit ALU. A 256-entry stack cap, accepted as the price of making every pointer's high byte boring. Chapter 5 walks the reasoning.

## A test program commits undefined behavior, knowingly

`fast_mult.c` never initializes `sum`, and the comment in the file admits why: the initialization would not fit in the 1KB ROM. The program relies on RAM waking up zeroed, which is exactly the sin the test suite's `RANDOMIZE` flag exists to catch. The machine's own test corpus contains a program its own test mode can flag. I keep it that way because it documents what a 1KB budget really means.

## The -l flag that does nothing

`assembler.py` declares a `-l` flag for a Logisim-formatted output. The implementation ignores it; output is byte-identical with and without. Logisim images come from hex files like `bootloader.txt` instead. The flag is a small fossil of an intended feature the toolchain routed around, and it survives in the argument parser to this day.

## The stale binary in the test suite

Each test program is committed next to the binary it should compile to. Recompiling everything on a fresh clone reproduces 21 of 22 comparable binaries byte for byte. The holdout is `array_subscripts.c`: today's compiler emits 938 bytes against a committed 1018.

![Recompiling all 24 test programs and diffing](../media/term-tests.png)

A byte diff cannot tell a regression from an improvement, so the tiebreaker is behavioral: run both binaries in the core for 200000 clocks and compare final stacks.

![Running both array_subscripts binaries in the emulator core](../media/term-tests-behavior.png)

Both end in the expected `[1, 2, 3]`. The committed binary is a snapshot of an older, chattier compiler, and the stored binaries turn out to be an accidental archaeological record of the toolchain's history.

## Smaller confessions

- The assembler resolves forward references by assembling the entire program twice, and its source comment says "assemble everything twice to build symbol table lol". I stand by it.
- The register the 74181 (4-bit ALU slice) datasheet calls A is wired to my B, and datasheet B is wired to my C. The assembler comments warn you, and now so have I, twice.
- `control_eeprom.py` writes its output into `eeprom_out/` while `memory_control_eeprom.py` writes into `out/`, and the second file gets copied over by hand. Every project has one of these.
- The zero and carry flags arrive at the control store inverted, so the generator reasons in `not zero` and `not carry` throughout.
- The emulator does not model the IN and OUT ports at 0x400 and 0x401. They belong to the physical design, where the OUT latch drives a display.

That is the machine, all the way down: a rock we taught to think, with a Python function for a brainstem and a lookup table where its decode logic should be. The [reference](../reference/index.md) has every table and file path, and [the end to end workflow](../reference/workflow-running-a-program.md) reproduces the whole journey from `fib.c` to a blinking debugger with real commands.

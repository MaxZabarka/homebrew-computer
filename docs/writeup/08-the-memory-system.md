# The memory system

The CPU sees one flat 64KB address space. Behind that clean facade sit four different physical parts with four different jobs, and something has to route each address to the right chip. This chapter is about the map, the router, and the one genuinely exotic chip in the machine.

## The map

| Range | Size | Region | Backing |
| --- | --- | --- | --- |
| 0x0000 to 0x03FF | 1KB | ROM | EEPROM, holds the program |
| 0x0400 | 1 byte | IN port | input device |
| 0x0401 | 1 byte | OUT port | output latch |
| 0x1000 to 0x1FFF | 4KB | VRAM | IDT7134 dual-port static RAM |
| 0x8000 to 0xFFFF | 32KB | RAM | 62256 static RAM |

This is the Harvard split from chapter 3 made concrete. The program sits in a 1KB ROM at the bottom of the map, physically unwritable. Data sits in 32KB of RAM in the top half, which is why every pointer you saw in chapter 5 had that high byte of 128: address 0x8000 is where RAM begins, and 128 is 0x80. In between sit two memory-mapped IO bytes and the video memory.

## The router is another EEPROM

Given an address, which chip answers? The classic answer is a decoder built from gates: check the top address bits, assert the matching chip enable. It is not much logic. It is still logic, and by now you know how I feel about wiring logic.

So the address decoder is the second EEPROM. `eeprom/memory_control_eeprom.py` enumerates the address space and, for each entry, outputs the chip enable lines: ROM below 0x400, the IN and OUT ports at their two addresses, VRAM in its 4KB window, RAM in the top half. The memory map is a file. If I wanted VRAM somewhere else tomorrow, I would edit a Python constant, rerun the generator, and burn a chip. The same trick from chapter 7, applied to a second question, and the last piece of combinational logic in the machine dissolves into a table.

A stray pointer on this machine hits either a mapped chip or dead air, and in the emulator it does something even better: `readMemory` and `writeMemory` enforce this exact map and throw on writes to ROM or on touching an unmapped hole. A wild pointer fails loudly at the moment of the crime instead of quietly corrupting memory, which during compiler debugging was worth more than any other single feature.

## The chip with two doors

Video memory has a problem all its own. A display needs to read VRAM continuously, tens of times per second, forever. The CPU wants to write to it whenever the program draws. On one ordinary RAM chip, those two users would fight over the address and data pins, and every classic design picks a loser: either the CPU waits for the blanking interval, or the display steals bus cycles from the CPU, or you build arbitration hardware to referee.

You can guess by now which option I refused: the referee, because a referee is wiring. Instead, VRAM is an IDT7134, a genuinely delightful part: 4KB of static RAM with two complete, independent ports. Two address buses, two data buses, two sets of control lines, one shared block of storage inside. The CPU owns the left door, the display circuit owns the right door, and neither knows the other exists. No arbitration, no stolen cycles, no waiting, at the price of one unusual chip instead of a fistful of glue logic.

The IN and OUT ports are humbler: two bytes just above ROM. Reading 0x400 asserts an enable line for an input device; writing 0x401 latches a byte for an output device. The emulator does not model them; they belong to the physical design, where the OUT latch drives a display.

Datasheets, decode details, and the Logisim circuits are in the [memory system reference](../reference/memory-system.md).

## The hardware is complete

Take stock, because the machine is now whole. Registers and a bus, a pointer that reaches 64KB, an ALU from 1969, a control unit that is a table, and a memory map that is also a table. Every wire accounted for, every part purchasable. What the machine lacks is anything to run. The rest of this writeup builds the software that feeds it, starting where every compiler starts: with raw text and the two classic phases that turn it into a tree.

Next: [The lexer and parser](09-the-lexer-and-parser.md)

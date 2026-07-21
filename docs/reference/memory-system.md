# Memory system

The CPU sees one flat 16-bit address space. Which physical chip answers a given address is decided by the memory control EEPROM described in [Microcode and the control store](microcode-and-control-store.md). This page covers the map itself and the chips behind it.

## The map

| Range | Size | Region | Backing |
| --- | --- | --- | --- |
| 0x0000 to 0x03FF | 1KB | ROM | EEPROM, holds the program |
| 0x0400 | 1 byte | IN port | input device |
| 0x0401 | 1 byte | OUT port | output latch |
| 0x1000 to 0x1FFF | 4KB | VRAM | IDT7134 dual-port static RAM |
| 0x8000 to 0xFFFF | 32KB | RAM | 62256-class static RAM |

The constants appear twice, once in `eeprom/memory_control_eeprom.py` where they shape the decode table, and once in `emulator_core/Computer.js` where `readMemory` and `writeMemory` enforce the same regions. The emulator throws on writes to ROM and on any access outside a mapped region, so a stray pointer fails loudly instead of corrupting state.

Two consequences of this layout show up all over the toolchain:

1. Code runs from address 0 and data lives at 0x8000 and up. The VM translator brackets every label with `#origin` directives to switch the assembler between the two bases (see [The assembler](assembler.md)).
2. The high byte of any stack address is always 128 (0x8000 >> 8). The generated assembly leans on this constantly with `AHigh = 128` before stack accesses, and the VM keeps its entire stack within one 256-byte page so that only the low byte ever needs arithmetic.

## The dual-port IDT7134

VRAM is an IDT7134, a 4K x 8 static RAM with two complete, independent ports: two address buses, two data buses, two sets of control lines. The CPU writes pixels through one port while a display circuit reads through the other, with no arbitration logic and no stolen cycles. That is the whole reason this part was chosen: video output does not slow the CPU down, and the display does not need to wait for the bus.

The Logisim design models it as the `RAM_IDT7134` circuit inside `pcb_computer.circ`, wrapped around a small register-file model, and instantiates it in the `Memory` circuit next to the ROM and the main RAM. Notes on its port logic are in `information/Ram 7134 logic.PNG`, and the manufacturer datasheets are `information/42833.pdf` and `information/datasheet.pdf`.

## The IN and OUT ports

Addresses 0x400 and 0x401 sit just above ROM and act as memory-mapped IO. A read from 0x400 asserts enableIn and a write to 0x401 asserts loadOut in the memory control table. The emulator does not model these ports. They exist for the hardware, where the OUT latch drives the display module shown in [Hardware](hardware.md).

## Where the code lives

The decode table generator is `eeprom/memory_control_eeprom.py`. The emulator's memory model is `readMemory`, `writeMemory`, and the region constants in `emulator_core/Computer.js`. The Logisim side is the `Memory`, `RAM_IDT7134`, `RAM_62256`, and `EEPROM_ROM` circuits in `pcb_computer.circ`.

# Hardware

The machine exists as a complete Logisim Evolution design, `pcb_computer.circ`, drawn around parts that can be bought and soldered. Three modules of it were built as physical PCBs, and a bit-banged I2C transmitter exists as a prototype for talking to peripherals.

## The Logisim design

The design is organized as subcircuits that each correspond to a physical chip or board. Walking the instantiation tree from `main` gives the inventory:

| Subcircuit | Models | Instances in the design |
| --- | --- | --- |
| `fixed74181` | 74181 4-bit ALU slice | 2, chained in the `ALU` circuit |
| `OctalTransceiver74245` | 74245 bus transceiver | 11 total: one per register byte, one in the ALU, four in the `AddressSelector` |
| `Register8` | one register byte, a 74377 plus a 74245 | 6, for IRHigh, IRLow, AHigh, ALow, B, and C |
| `ProgramCounter` | four cascaded 74161 counters | 1 |
| `Microcode` | the microstep counter, a 74161 | 1 |
| `Comparator74682` | 74682 zero comparator, modeled from two 7485s and a NAND | 1, for the ALU's zero flag |
| `RAM_IDT7134` | IDT7134 dual-port 4K x 8 static RAM | 1, the VRAM |
| `RAM_62256` | 32K x 8 static RAM | 1, the main RAM |
| `EEPROM_ROM` | the 1KB program ROM | 1 |

Two Logisim ROM components in `main` hold the generated control tables from [Microcode and the control store](microcode-and-control-store.md), standing in for the AT28C256 EEPROMs of a physical build. The `Bus16` and `AddressSelector` circuits arbitrate who drives the shared bus, and the 74245 transceivers are what makes that possible: every register connects to the bus through one, and its enable line is a control store output.

## The physical PCB modules

Three modules made it to fabricated boards: a clock, a counter, and a display. The video shows them working together, the counter stepping under the clock with the display showing the count:

[pcb-demo.mp4](media/pcb-demo.mp4)

The modular approach matches the control word layout. `eeprom/control_eeprom.py` groups its control lines by board ("Each section represents a unique physical PCB" in the source), so a module can be built and tested against the generated table before the next one exists.

## The I2C experiment

`i2c/i2c.js` is a bit-banged I2C master transmitter, written to prototype the protocol before committing it to hardware. It walks the full transmit sequence: a start condition (data falls while clock is high), eight data bits shifted out MSB first with a clock pulse each, then releasing the data line and sampling the acknowledge bit. The demo at the bottom of the file sends the address byte 0x50. The functions log line states instead of driving pins, so the sequence can be read and checked in a terminal.

## Where the code lives

The whole design is `pcb_computer.circ` (Logisim Evolution). Chip references are in `information/`: the IDT7134 datasheet twice (`42833.pdf` and `datasheet.pdf`), the AT28C256 EEPROM datasheet (`74878AT.pdf`), and port logic notes (`Ram 7134 logic.PNG`). The I2C prototype is `i2c/i2c.js`.

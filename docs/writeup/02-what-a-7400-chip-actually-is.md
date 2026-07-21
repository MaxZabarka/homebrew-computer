# What a 7400 chip actually is

Before we look at the machine, we should agree on what it is made of. If you have never held one, "chip" probably means something like a CPU: a mysterious black square with a billion transistors, doing things no person fully understands. The 7400 series is the opposite of that, and the whole project rests on the difference.

## A family of small, honest parts

The 7400 series is a family of logic chips introduced in the 1960s. Each one is a small black rectangle with somewhere between 14 and 24 metal legs, it runs on 5 volts, and it does exactly one thing. They look like caterpillars. The original 7400 contains four NAND gates. That is the entire chip. Four gates, fourteen pins, and a datasheet a few pages long that tells you everything there is to know.

![The 7400's four NAND gates, and the chip itself](../media/7400-chip.png)

The family grew from there, and the numbering scheme just counts upward: 7404 is six inverters, 7474 is two flip-flops, 74161 is a 4-bit counter. The parts I care about sit further up the catalog, where single chips start doing register-sized and ALU-sized jobs. But every member of the family keeps the same promise: you can read the datasheet in one sitting, you can understand the chip completely, and you can poke its pins with a wire and watch it respond. There is no firmware, no configuration, no hidden state. Voltage in, voltage out.

That promise is why I built from these parts. A machine made of 7400 chips has no black boxes anywhere in it. Every control signal in this design ends at a physical pin of a part you can buy, and when I say in later chapters that "a control line enables a register", that is a literal wire touching a literal leg.

## The main players in this machine

![The 7400-series parts this machine is built from](../media/fig-7400-family.png)

Five family members do almost all the work here:

| Part | What it is | Job in this machine |
| --- | --- | --- |
| 74377 | eight flip-flops with a shared clock enable | one of these stores one register byte |
| 74245 | eight-line bus transceiver | the valve that connects a register to the shared bus |
| 74161 | 4-bit binary counter | four of them chained form the program counter, one more runs the microcode step |
| 74181 | 4-bit ALU slice | two of them chained form the whole ALU |
| 74682 | 8-bit comparator | detects when the ALU result is zero |

The 74181 is the star, and it gets its own chapter. It is a complete 4-bit arithmetic and logic unit in one package, from an era when a "CPU" was a cabinet and this chip was one slice of its math section. The others are supporting cast, but the 74245 deserves a moment now, because you will meet it constantly. It is a set of eight switches. When its enable pin is low, eight signals pass through; when high, the chip electrically disappears. That one behavior is what lets many registers share one bus without fighting.

Three memory parts round out the machine, and they are cousins rather than family members: the 62256 (32KB of static RAM), the IDT7134 (4KB of dual-port static RAM, a strange part I will get to in chapter 8), and the AT28C256 EEPROM, a 32KB memory you program once and read forever. Remember the EEPROM. In chapter 7 it stops being a memory chip and becomes the machine's brain.

These parts sound friendly, and as objects to think with they are. Working with them in the physical world is another matter: what they cost, how long they take to arrive, and what wiring hundreds of them actually means. That story gets its full telling in chapter 7, at the moment it forced the machine's strangest decision. First, the machine these parts add up to.

Next: [The shape of the machine](03-the-shape-of-the-machine.md)

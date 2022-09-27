const { ENABLES, LOADS } = require("./constants");

START_ROM = 0x0;
ROM_SIZE = 0x400;

START_VRAM = 0x1000;
VRAM_SIZE = 0x1000;

START_RAM = 0x8000;
RAM_SIZE = 0x8000;

const toBinary = (n, pad = 8) => {
  return n.toString(2).padStart(pad, "0");
};

class Computer {
  constructor() {
    this.programCounter = 0;
    this.registers = {
      IRHigh: 0,
      IRLow: 0,
      AHigh: 0,
      ALow: 0,
      B: 0,
      C: 0,
    };
    this.memory = {
      ROM: Array(2 ** 10),
      RAM: Array(2 ** 15),
      VRAM: Array(2 ** 12),
    };
  }

  get A() {
    return (this.registers.AHigh << 8) + this.registers.ALow;
  }

  writeMemory(address, data) {
    if (address >= START_ROM && address < START_ROM + ROM_SIZE) {
      throw "Cannot write to ROM";
    }

    if (address >= START_RAM && address < START_RAM + RAM_SIZE) {
      this.memory.RAM[address - START_RAM] = data;
      return;
    }

    if (address >= START_VRAM && address < START_VRAM + VRAM_SIZE) {
      this.memory.VRAM[address - START_VRAM] = data;
      return;
    }
    throw "Memory location does not exist";
  }

  readMemory(address) {
    if (address >= START_ROM && address < START_ROM + ROM_SIZE) {
      return this.memory.ROM[address - START_ROM];
    }

    if (address >= START_RAM && address < START_RAM + RAM_SIZE) {
      return this.memory.RAM[address - START_RAM];
    }

    if (address >= START_VRAM && address < START_VRAM + VRAM_SIZE) {
      return this.memory.VRAM[address - START_VRAM];
    }
  }

  nextInstruction() {
    const lowByte = this.readMemory(this.programCounter);
    this.programCounter++;
    const highByte = this.readMemory(this.programCounter);
    this.programCounter++;
    this.registers.IRHigh = highByte;
    this.registers.IRLow = lowByte;
  }

  processMove(instruction) {
    const load = LOADS[instruction.slice(1, 4)];
    const enable = ENABLES[instruction.slice(4, 7)];
    if (load === "RAM") {
        console.log('this.registers', this.registers)
      console.log("this.A", this.A);
      this.writeMemory(this.A, this.registers[enable]);
      return;
    }
    if (enable === "RAM") {
      this.registers[load] = this.readMemory(this.A);
      return;
    }
    this.registers[load] = this.registers[enable];
  }

  clock() {
    this.nextInstruction();
    const instruction =
      toBinary(this.registers.IRLow) + toBinary(this.registers.IRHigh);

    if (instruction[0] === "0") {
      return this.processMove(instruction);
    }
  }
}
module.exports = Computer;

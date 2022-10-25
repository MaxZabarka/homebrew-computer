const {
  ENABLES,
  LOADS,
  JUMPS,
  EXPRESSIONS,
  JUMP_NAMES,
} = require("./constants");
const ALUCircuit = require("./ALUCircuit");

const toBinary = (n, pad = 8) => {
  return n.toString(2).padStart(pad, "0");
};

class Computer {
  static STACK_START = 0x9;
  static START_RAM = 0x8000;
  static RAM_SIZE = 0x8000;
  static START_ROM = 0x0;
  static ROM_SIZE = 0x400;
  static START_VRAM = 0x1000;
  static VRAM_SIZE = 0x1000;

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
      ROM: Array(2 ** 10).fill(0),
      RAM: Array(2 ** 15).fill(0),
      VRAM: Array(2 ** 12).fill(0),
    };
  }

  get A() {
    return (this.registers.AHigh << 8) + this.registers.ALow;
  }

  loadROM(bin) {
    if (bin.length > 1024) {
      throw Error("ROM too large");
    }

    for (let address = 0; address < bin.length; address++) {
      this.memory.ROM[address] = bin[address];
    }
  }

  getStack() {
    const numOfStackItems =
      this.memory.RAM[0] - Computer.STACK_START;
    const stack = this.memory.RAM.slice(
      Computer.STACK_START,
      numOfStackItems + Computer.STACK_START
    );

    return stack
  }
  getStackOnMain() {
    const stack = this.getStack()
    return stack.slice(4, stack.length)
  }

  clone() {
    const clone = Object.assign({}, this);
    Object.setPrototypeOf(clone, Computer.prototype);
    return clone;
  }

  disassemble(lowByte, highByte) {
    const lowByteBits = toBinary(lowByte);
    const highByteBits = toBinary(highByte);

    const load = LOADS[lowByteBits.slice(1, 4)];

    if (lowByteBits[0] === "0") {
      const enable = ENABLES[lowByteBits.slice(4, 7)];
      if (enable === "IRHigh") {
        return `${load}=${highByte}`;
      }
      return `${load}=${enable}`;
    } else {
      const jump = JUMP_NAMES[lowByteBits.slice(4, 8)];
      const computation = EXPRESSIONS[highByteBits.slice(0, 6)];

      if (jump === "JMP") {
        return jump;
      }

      if (load) {
        return `${load}=(${computation})`;
      }

      if (!load && jump) {
        return `(${computation}), ${jump}`;
      }

      return highByte + " " + lowByte;
    }
  }

  // loadROM(filePath) {
  //   const bin = fs.readFileSync(filePath);
  //   for (let address = 0; address < bin.length; address++) {
  //     this.memory.ROM[address] = bin[address];
  //   }
  // }

  writeMemory(address, data) {
    if (
      address >= Computer.START_ROM &&
      address < Computer.START_ROM + Computer.ROM_SIZE
    ) {
      throw Error("Cannot write to ROM");
    }

    if (
      address >= Computer.START_RAM &&
      address < Computer.START_RAM + Computer.RAM_SIZE
    ) {
      this.memory.RAM[address - Computer.START_RAM] = data;
      return;
    }

    if (
      address >= Computer.START_VRAM &&
      address < Computer.START_VRAM + Computer.VRAM_SIZE
    ) {
      this.memory.VRAM[address - Computer.START_VRAM] = data;
      return;
    }
    throw Error("Memory location does not exist");
  }

  readMemory(address) {
    if (
      address >= Computer.START_ROM &&
      address < Computer.START_ROM + Computer.ROM_SIZE
    ) {
      return this.memory.ROM[address - Computer.START_ROM];
    }

    if (
      address >= Computer.START_RAM &&
      address < Computer.START_RAM + Computer.RAM_SIZE
    ) {
      return this.memory.RAM[address - Computer.START_RAM];
    }

    if (
      address >= Computer.START_VRAM &&
      address < Computer.START_VRAM + Computer.VRAM_SIZE
    ) {
      return this.memory.VRAM[address - Computer.START_VRAM];
    }
    throw Error("Memory location does not exist");
  }

  nextInstruction() {
    const lowByte = this.readMemory(this.programCounter);
    this.programCounter++;
    const highByte = this.readMemory(this.programCounter);
    this.programCounter++;
    this.registers.IRHigh = highByte;
    this.registers.IRLow = lowByte;
  }

  processMoveInstruction(instruction) {
    const load = LOADS[instruction.slice(1, 4)];
    const enable = ENABLES[instruction.slice(4, 7)];
    this.move(load, enable);
  }

  move(load, enable) {
    if (!load || !enable) {
      return;
    }

    if (load === "RAM") {
      this.writeMemory(this.A, this.registers[enable]);
      return;
    }

    if (enable === "RAM") {
      this.registers[load] = this.readMemory(this.A);
      return;
    }
    this.registers[load] = this.registers[enable];
  }

  processComputationInstruction(instruction) {
    const load = LOADS[instruction.slice(1, 4)];
    const jumpCondition = JUMPS[instruction.slice(4, 8)];
    const ALUOperation = instruction.slice(8, 14);
    const ALUOut = ALUCircuit(
      this.registers.B,
      this.registers.C,
      parseInt(ALUOperation, 2)
    );

    // Jump logic here \/
    if (jumpCondition) {
      let shouldJump = false;
      Object.entries(jumpCondition).forEach(([flag, expectedValue]) => {
        if (flag === "zero" && ALUOut.zero === expectedValue) {
          shouldJump = true;
        }
        if (flag === "negative" && ALUOut.negative === expectedValue) {
          shouldJump = true;
        }
        if (flag === "carry" && ALUOut.carryOut === expectedValue) {
          shouldJump = true;
        }
      });
      if (Object.entries(jumpCondition).length === 0) {
        shouldJump = true;
      }
      if (shouldJump) {
        this.programCounter = this.A;
      }
    }

    if (!load) {
      return;
    }
    if (load === "RAM") {
      this.writeMemory(this.A, ALUOut.result);
      return;
    }
    this.registers[load] = ALUOut.result;
  }

  clock(n = 1) {
    while (n) {
      this.clock_once();
      n--;
    }
  }
  clock_once() {
    this.nextInstruction();
    const instruction =
      toBinary(this.registers.IRLow) + toBinary(this.registers.IRHigh);

    if (instruction[0] === "0") {
      return this.processMoveInstruction(instruction);
    } else {
      return this.processComputationInstruction(instruction);
    }
  }
}
module.exports = Computer;

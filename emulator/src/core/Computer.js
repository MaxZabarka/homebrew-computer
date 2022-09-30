const {
  ENABLES,
  LOADS,
  JUMPS,
  EXPRESSIONS,
  JUMP_NAMES,
} = require("./constants");
const ALUCircuit = require("./ALUCircuit");
const { toBinary } = require("../lib/toBinary");
const START_ROM = 0x0;
const ROM_SIZE = 0x400;

const START_VRAM = 0x1000;
const VRAM_SIZE = 0x1000;

const START_RAM = 0x8000;
const RAM_SIZE = 0x8000;


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
      ROM: Array(2 ** 10).fill(0),
      RAM: Array(2 ** 15).fill(0),
      VRAM: Array(2 ** 12).fill(0),
    };
  }

  get A() {
    return (this.registers.AHigh << 8) + this.registers.ALow;
  }

  loadROM(bin) {
    for (let address = 0; address < bin.length; address++) {
      this.memory.ROM[address] = bin[address];
    }
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
        return `(${computation}), ${jump}`
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
    if (address >= START_ROM && address < START_ROM + ROM_SIZE) {
      throw Error("Cannot write to ROM");
    }

    if (address >= START_RAM && address < START_RAM + RAM_SIZE) {
      this.memory.RAM[address - START_RAM] = data;
      return;
    }

    if (address >= START_VRAM && address < START_VRAM + VRAM_SIZE) {
      this.memory.VRAM[address - START_VRAM] = data;
      return;
    }
    throw Error("Memory location does not exist");
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
      let shouldJump = true;
      Object.entries(jumpCondition).forEach(([flag, expectedValue]) => {
        if (flag === "zero" && ALUOut.zero !== expectedValue) {
          shouldJump = false;
        }
        if (flag === "negative" && ALUOut.negative !== expectedValue) {
          shouldJump = false;
        }
        if (flag === "carry" && ALUOut.carryOut !== expectedValue) {
          shouldJump = false;
        }
      });
      if (shouldJump) {
        // console.log(this.A)
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

  clock() {
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

const removeWhiteSpace = require("./removeWhiteSpace");
const { ENABLES, LOADS } = require("./constants");
const Computer = require("./Computer");



const computer = new Computer();

const processMove = (computer, instruction) => {
  const data = parseInt(instruction.slice(-8), 2);
  const load = LOADS[instruction.slice(1, 4)];
  const enable = ENABLES[instruction.slice(4, 7)];
  computer.registers.IRHigh = data;
  computer.registers[load] = computer.registers[enable];
};

const processCompute = (state, instruction) => {
  throw new Error("not implemented");
};

const nextState = (computer, instruction) => {
  instruction = removeWhiteSpace(instruction);
  if (instruction.length !== 16) {
    throw new Error("Instructions must be 16 bits long");
  }

  if (instruction[0] === "0") {
    processMove(computer, instruction);
    return computer;
  } else {
  }
};

// console.log(nextState(computer, "0 001 110 0 10000000")); // AHigh = 0x8000
// console.log(nextState(computer, "0 010 110 0 00000001")); // ALow = 1

// console.log('computer.A', computer.A)
// computer.writeMemory(computer.A, 500)
computer.memory.ROM[0] = 0b00011100
computer.memory.ROM[1] = 85

computer.memory.ROM[2] = 0b00100010
computer.memory.ROM[3] = 0

computer.memory.ROM[4] = 0b00110100
computer.memory.ROM[5] = 0

computer.memory.ROM[6] = 0b01000110
computer.memory.ROM[7] = 0

computer.memory.ROM[8] = 0b00101100
computer.memory.ROM[9] = 0

computer.memory.ROM[10] = 0b00011100
computer.memory.ROM[11] = 16

computer.memory.ROM[12] = 0b01011100
computer.memory.ROM[13] = 170

computer.clock()
computer.clock()
computer.clock()
computer.clock()
computer.clock()
computer.clock()
computer.clock()

console.log('computer', computer)
// console.log('computer', computer)
// console.log(nextState(computer, "0 011 110 0 11111111")); // B = 255
// console.log(nextState(computer, "0 100 011 0 01010101")); // C = B

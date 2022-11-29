const Computer = require("../emulator_core/Computer");
const { execSync } = require("child_process");
const path = require("path");
const fs = require("fs");

const run = (fileName) => {
  const compiler = path.resolve(__dirname, "../compile.py");
  const input = path.resolve(__dirname, fileName);
  const output = path.resolve(__dirname, path.parse(fileName).name);

  try {
    const computer = new Computer(true);
    execSync(`${compiler} ${input} -o ${output}.bin`);
    const ROM = fs.readFileSync(output + ".bin");
    computer.loadROM(ROM);
    computer.clock(200000);
    return computer;
  } finally {
    deleteFile(output + ".zab");
    deleteFile(output + ".vm");
  }
};

const deleteFile = (fileName) => {
  try {
    fs.unlinkSync(fileName);
  } catch (e) {
    if (e.code !== "ENOENT") {
      throw e;
    }
  }
};

const testStack = (fileName, expectedStack) => {
  const computer = run(fileName);
  expect(computer.getStack().slice(-expectedStack.length)).toEqual(
    expectedStack
  );
};

test("constants", () => {
  testStack("constants.c", [1, 2, 3, 4, 5]);
});

test("if", () => {
  testStack("if.c", [1, 2]);
});

test("if else", () => {
  testStack("if_else.c", [1, 2, 3]);
});

test("if else if", () => {
  testStack("if_else_if.c", [1, 2, 3]);
});

test("if else if else", () => {
  testStack("if_else_if_else.c", [1, 2, 3, 4]);
});

test("while loop", () => {
  testStack("while.c", [5, 4, 3, 2, 1]);
});

test("recursive multiplication", () => {
  testStack("recursive_mult.c", [30]);
});

test("iterative multiplication", () => {
  testStack("iterative_mult.c", [30]);
});

test("fast multiplication", () => {
  testStack("fast_mult.c", [1]);
});

test("local variables", () => {
  testStack("local.c", [1, 2, 3, 4, 5, 6, 7]);
});

test("argument variables", () => {
  testStack("argument.c", [1, 2, 3]);
});

test("order of operations", () => {
  testStack("order_of_operations.c", [13]);
});

test("additive operations", () => {
  testStack("additive.c", [1, 2, 3]);
});

test("left shift", () => {
  testStack("left_shift.c", [0, 4, 8, 1, 2, 4, 32, 64, 128]);
});

test("relational operators (>, <)", () => {
  testStack("relational.c", [5, 0, 0, 5]);
});

test("relational operators 2 (=<, >=)", () => {
  testStack("relational_2.c", [1, 1, 0, 0, 1, 1]);
});

test("equality operators", () => {
  testStack("equality.c", [0, 1, 1, 0]);
});

test("function call", () => {
  testStack("function_call.c", [1, 2, 3]);
});

test("bitwise operators", () => {
  testStack("bitwise.c", [16, 127]);
});

// test("pointers", () => {
//   testStack("pointers.c", [1, 2, 3, 4, 5, 6]);
// })
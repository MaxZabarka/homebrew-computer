const Computer = require("./Computer");

const computer = new Computer();

computer.loadROM("../programs/fib.bin");

Array(20)
  .fill()
  .forEach(() => {
    console.log('computer', computer)
    computer.clock();
  });

// while(true) {
//   console.log('computer', computer)
//   computer.clock()
// }

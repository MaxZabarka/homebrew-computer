const Computer = require("../core/Computer");

let computer = new Computer();

postMessage(computer)

onmessage = (e) => {
  const data = e.data;
  const action = data.action;

  if (action === "run") {
    if (e.data.shouldRun[0] === 1) {
      return;
    }
    e.data.shouldRun[0] = 1;

    while (e.data.shouldRun[0]) {
      computer.clock();
    }
    postMessage(computer);
  }

  if (action === "clock") {
    computer.clock();
    postMessage(computer);
  }

  if (action === "loadROM") {
    computer = new Computer();
    computer.loadROM(data.ROM);
    postMessage(computer);
  }
  if (action === "reset") {
    const newComputer = new Computer();
    newComputer.memory.ROM = computer.memory.ROM;
    postMessage(newComputer);
  }

  if (action === "get") {
    postMessage(computer);

  }
};

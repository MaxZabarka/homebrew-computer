const Computer = require("../core/Computer");

let computer = new Computer();

postMessage(computer);

onmessage = (e) => {
  const data = e.data;
  const action = data.action;

  if (action === "run") {
    if (e.data.shouldRun[0] === 1) {
      return;
    }
    e.data.shouldRun[0] = 1;

    while (e.data.shouldRun[0]) {
      try {
        computer.clock();
      } catch (e) {
        console.log(e);
        break
      }
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
    const ROM = computer.memory.ROM
    computer = new Computer();
    computer.loadROM(ROM);
    postMessage(computer);
  }

  if (action === "get") {
    postMessage(computer);
  }
};

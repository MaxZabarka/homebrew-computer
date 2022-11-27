const Computer = require("../core/Computer");

let computer = new Computer();
let breakpoints = new Set();

postMessage({ computer });
onmessage = (e) => {
  const data = e.data;
  const action = data.action;
  if (action === "run") {
    if (e.data.shouldRun[0] === 1) {
      return;
    }
    e.data.shouldRun[0] = 1;
    let reachedBreakpoint = false;
    let error = null;

    while (e.data.shouldRun[0]) {
      try {
        computer.clock();
        if (breakpoints.has(computer.programCounter)) {
          e.data.shouldRun[0] = 0;
          reachedBreakpoint = true;
          break;
        }
      } catch (e) {
        error = e;
        data.shouldRun[0] = 0;
        reachedBreakpoint = true;
        break;
      }
    }
    console.log('error :>> ', error);
    postMessage({ computer, reachedBreakpoint, error });
  }

  if (action === "updateBreakpoints") {
    breakpoints = data.breakpoints;
  }

  if (action === "clock") {
    let error = null;
    try {
      computer.clock();
    } catch (e) {
      console.error(e)
      error = e;
    }
    console.log(computer)

    postMessage({ computer, error });
  }

  if (action === "loadROM") {
    computer = new Computer();
    computer.loadROM(data.ROM);
    postMessage({ computer });
  }

  if (action === "reset") {
    // e.data.shouldRun[0] = 1;
    // onmessage({ data: { action: "stop" } });
    onmessage({ data: { action: "loadROM", ROM: computer.memory.ROM } });
    // const ROM = computer.memory.ROM
    // computer = new Computer();
    // computer.loadROM(ROM);
    // postMessage(computer);
  }
};

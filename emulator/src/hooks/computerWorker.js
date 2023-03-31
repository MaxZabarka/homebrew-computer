const Computer = require("../core/Computer");

let computer = new Computer();
let breakpoints = new Set();

postMessage({ computer });
onmessage = (e) => {
  const data = e.data;
  const action = data.action;

  if (action === "run") {
    let reachedBreakpoint = false;
    let error = null;
    let throttle = e.data.shared[1];

    let clocks = 0;
    let lastClock = performance.now();
    const MILLI_TO_SEC = 1000;

    if (throttle > 0) {
      e.data.shared[0] = 1;

      const runThrottled = () => {
        let breakTimeoutLoop = false;
        if (e.data.shared[0] === 0) {
          breakTimeoutLoop = true;
        }
        try {
          computer.clock();
          const currentTime = performance.now();
          postMessage({
            speed: 1 / ((currentTime - lastClock) / MILLI_TO_SEC),
          });
          lastClock = currentTime;

          if (breakpoints.has(computer.programCounter)) {
            e.data.shared[0] = 0;
            reachedBreakpoint = true;
            breakTimeoutLoop = true;
          }
        } catch (e) {
          error = e;
          data.shared[0] = 0;
          reachedBreakpoint = true;
          breakTimeoutLoop = true;
        }
        postMessage({ computer, reachedBreakpoint: true, error });

        if (!breakTimeoutLoop) {
          throttle = e.data.shared[1];
          setTimeout(runThrottled, throttle);
          if (throttle === 0) {
            onmessage({ data: { action: "run" } });
          }
        }
      };

      setTimeout(() => {
        runThrottled();
      }, throttle);
      return;
    }

    if (e.data.shared[0] === 1) {
      return;
    }
    e.data.shared[0] = 1;

    const SAMPLE = 1000000;
    while (e.data.shared[0]) {
      if (clocks === SAMPLE) {
        const currentTime = performance.now();
        postMessage({
          speed: SAMPLE / ((currentTime - lastClock) / MILLI_TO_SEC),
        });
        clocks = 0;
        lastClock = currentTime;
      }
      clocks++;

      try {
        computer.clock();
        if (breakpoints.has(computer.programCounter)) {
          e.data.shared[0] = 0;
          reachedBreakpoint = true;
          break;
        }
      } catch (e) {
        error = e;
        data.shared[0] = 0;
        reachedBreakpoint = true;
        break;
      }
    }
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
      console.error(e);
      error = e;
    }
    console.log(computer);

    postMessage({ computer, error });
  }

  if (action === "loadROM") {
    try{
      computer = new Computer();
      computer.loadROM(data.ROM);
    } catch (e) {
      console.log(e);
      postMessage({ error: e });
      return;
    }

    postMessage({ computer });
  }

  if (action === "reset") {
    // e.data.shared[0] = 1;
    // onmessage({ data: { action: "stop" } });
    onmessage({ data: { action: "loadROM", ROM: computer.memory.ROM } });
    // const ROM = computer.memory.ROM
    // computer = new Computer();
    // computer.loadROM(ROM);
    // postMessage(computer);
  }
};

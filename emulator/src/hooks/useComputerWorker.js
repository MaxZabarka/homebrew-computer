import Computer from "../core/Computer";

const { useEffect, useRef, useCallback, useState } = require("react");

if (!window.crossOriginIsolated) {
  throw new Error(
    "Cross Origin Isolation must be enabled for useComputerWorker"
  );
}

export const useComputerWorker = ({ ROM, onChange, throttle }) => {
  const sharedRef = useRef(null);
  const workerRef = useRef(null);
  const [running, setRunning] = useState(false);
  const [speed, setSpeed] = useState(null);

  useEffect(() => {
    // eslint-disable-next-line no-undef
    sharedRef.current = new Int16Array(new SharedArrayBuffer(4));
    sharedRef.current[0] = 0; // 0 = stop, 1 = run

    workerRef.current = new Worker(
      new URL("./computerWorker.js", import.meta.url)
    );
  }, [])

  useEffect(() => {
    workerRef.current.onmessage = (e) => {
      if (e.data.error) {
        alert(e.data.error);
        console.error(e.data.error)
      }
      if (e.data.computer) {
        const newComputer = { ...e.data.computer };
        Object.setPrototypeOf(newComputer, Computer.prototype);
        onChange(newComputer, e.data.reachedBreakpoint, e.data.sharp);
      }
      if (e.data.speed) {
        setSpeed(e.data.speed)
        console.log('speed (Hz):>> ', (e.data.speed));

        console.log('speed (mHZ):>> ', (e.data.speed/1_000_000));
      }
      setRunning(sharedRef.current[0] === 1);
    };
  }, [onChange]);

  useEffect(() => {
    sharedRef.current[1] = throttle;
  }, [throttle]);

  useEffect(() => {
    setSpeed(null);
  }, [running]);

  const run = () => {
    workerRef.current.postMessage({
      action: "run",
      shared: sharedRef.current,
    });
    setRunning(true);
  };

  const stop = () => {
    sharedRef.current[0] = 0;
  };

  const clock = () => {
    workerRef.current.postMessage({
      action: "clock",
    });
  };

  const updateBreakpoints = (breakpoints) => {
    workerRef.current.postMessage({ action: "updateBreakpoints", breakpoints });
  };

  const reset = () => {
    stop();
    workerRef.current.postMessage({ action: "reset" });
  };

  const loadROM = useCallback((ROM) => {
    workerRef.current.postMessage({ action: "loadROM", ROM });
  }, []);

  return { run, stop, clock, reset, loadROM, updateBreakpoints, running, speed };
};

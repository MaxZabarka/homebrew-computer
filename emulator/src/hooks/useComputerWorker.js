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

  useEffect(() => {
    if (workerRef.current) {
      workerRef.current.postMessage({ action: "throttle" });
    }
  }, [throttle]);

  useEffect(() => {
    // eslint-disable-next-line no-undef
    sharedRef.current = new Int8Array(new SharedArrayBuffer(1));
    workerRef.current = new Worker(
      new URL("./computerWorker.js", import.meta.url)
    );

    workerRef.current.onmessage = (e) => {
      const newComputer = { ...e.data.computer };
      Object.setPrototypeOf(newComputer, Computer.prototype);
      if (e.data.error) {
        alert(e.data.error)
      }
      setRunning(sharedRef.current[0] === 1);
      onChange(newComputer, e.data.reachedBreakpoint);
    };
  }, [onChange, ROM]);

  const run = () => {
    workerRef.current.postMessage({
      action: "run",
      shouldRun: sharedRef.current,
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

  return { run, stop, clock, reset, loadROM, updateBreakpoints, running };
};

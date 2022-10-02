import Computer from "../core/Computer";

const { useEffect, useRef, useCallback } = require("react");

if (!window.crossOriginIsolated) {
  throw new Error(
    "Cross Origin Isolation must be enabled for useComputerWorker.js"
  );
}

export const useComputerWorker = ({ ROM, onChange }) => {
  const sharedRef = useRef(null);
  const workerRef = useRef(null);

  useEffect(() => {
    // eslint-disable-next-line no-undef
    sharedRef.current = new Int8Array(new SharedArrayBuffer(1));
    workerRef.current = new Worker(
      new URL("./computerWorker.js", import.meta.url)
    );

    workerRef.current.onmessage = (e) => {
      const newComputer = { ...e.data };
      Object.setPrototypeOf(newComputer, Computer.prototype);
      onChange(newComputer);
    };
  }, [onChange, ROM]);

  const run = () => {
    workerRef.current.postMessage({
      action: "run",
      shouldRun: sharedRef.current,
    });
  };

  const stop = () => {
    sharedRef.current[0] = 0;
  };

  const clock = () => {
    console.log("cloc");
    workerRef.current.postMessage({
      action: "clock",
    });
  };

  const reset = () => {
    workerRef.current.postMessage({ action: "reset" });
  };

  const loadROM = useCallback((ROM) => {
    workerRef.current.postMessage({ action: "loadROM", ROM });
  }, []);

  return { run, stop, clock, reset, loadROM };
};

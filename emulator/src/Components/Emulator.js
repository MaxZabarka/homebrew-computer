import React, {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import Computer from "../core/Computer";
import { useFilePicker } from "use-file-picker";
import ROM from "./ROM";
import { useComputerWorker } from "../hooks/useComputerWorker";
import VirtualMachine from "./VirtualMachine";
import Stack from "./Stack";
import Registers from "./Registers";
import "./Emulator.scss";
import Controls from "./Controls";
export const ComputerContext = React.createContext();

export const Emulator = () => {
  const [computer, setComputer] = useState(null);
  const [breakpoints, setBreakpoints] = useState(new Set());
  const lastLoadedFileRef = useRef(null);
  const romRef = useRef(null);

  const [openFileSelector, { filesContent }] = useFilePicker({
    accept: ".bin",
    multiple: false,
    readAs: "ArrayBuffer",
  });

  const onComputerChange = useCallback(
    (newComputer, reachedBreakpoint) => {
      setComputer(newComputer);
      if (reachedBreakpoint) {
        scrollActiveIntoView();
      }
    },
    [setComputer]
  );

  const scrollActiveIntoView = () => {
    setTimeout(() => {
      romRef.current.scrollActiveIntoView();
    }, 50);
  };

  const computerWorker = useComputerWorker({
    onChange: onComputerChange,
    throttle: 0,
  });

  const run = () => {
    computerWorker.run();
  };
  const stop = () => {
    computerWorker.stop();
    scrollActiveIntoView();
  };
  const clock = () => {
    try {
      computerWorker.clock();
    } catch (e) {
      alert(e);
    }
    scrollActiveIntoView();
  };
  const reset = () => {
    computerWorker.reset();
  };

  const clearBreakpoints = () => {
    setBreakpoints(new Set());
  };

  const { loadROM, updateBreakpoints, running } = computerWorker;
  useEffect(() => {
    if (!filesContent[0]) {
      return;
    }
    const file = filesContent[0];
    if (file.name !== lastLoadedFileRef.current?.name) {
      clearBreakpoints();
    }
    loadROM(new Uint8Array(file.content));
    lastLoadedFileRef.current = file;
  }, [filesContent, loadROM]);

  useEffect(() => {
    updateBreakpoints(breakpoints);
  }, [breakpoints, updateBreakpoints]);

  return (
    <div className="Emulator">
      <Controls
        running={running}
        openFileSelector={openFileSelector}
        run={run}
        stop={stop}
        clock={clock}
        reset={reset}
        clearBreakpoints={clearBreakpoints}
      />
      <main className={running ? "disabled" : ""}>
        {computer && (
          <ComputerContext.Provider value={[computer, setComputer]}>
            <ROM
              breakpoints={breakpoints}
              setBreakpoints={setBreakpoints}
              ref={romRef}
              onSelectROM={openFileSelector}
            />
            <Stack />
            <VirtualMachine />
            <Registers />
          </ComputerContext.Provider>
        )}
      </main>
    </div>
  );
};

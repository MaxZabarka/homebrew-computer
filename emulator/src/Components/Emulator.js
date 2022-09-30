import React, { useEffect, useMemo, useRef, useState } from "react";
import Computer from "../core/Computer";
import { useFilePicker } from "use-file-picker";
import ROM from "./ROM";
import { useComputerWorker } from "../hooks/useComputerWorker";
import VirtualMachine from "./VirtualMachine";
export const ComputerContext = React.createContext();

export const Emulator = () => {
  const [computer, setComputer] = useState(null);

  const [openFileSelector, { filesContent }] = useFilePicker({
    accept: ".bin",
    multiple: false,
    readAs: "ArrayBuffer",
  });

  const { run, stop, clock, loadROM, reset } = useComputerWorker({
    onChange: setComputer,
  });

  useEffect(() => {
    if (!filesContent[0]) {
      return;
    }
    loadROM(new Uint8Array(filesContent[0].content));
  }, [filesContent, loadROM]);

  return (
    <div>
      <button onClick={openFileSelector}>Select ROM</button>
      <button onClick={run}>Run</button>
      <button onClick={stop}>Stop</button>
      <button onClick={clock}>Clock</button>
      <button onClick={reset}>Reset</button>

      {computer && (
        <ComputerContext.Provider value={computer}>
          <ROM onSelectROM={openFileSelector} />
          <VirtualMachine/>
          <h1>B: {computer.registers.B}</h1>
          <h1>C: {computer.registers.C}</h1>
        </ComputerContext.Provider>
      )}
    </div>
  );
};

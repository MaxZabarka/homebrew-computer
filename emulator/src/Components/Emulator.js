import React, { useEffect, useMemo, useRef, useState } from "react";
import Computer from "../core/Computer";
import { useFilePicker } from "use-file-picker";
import ROM from "./ROM";
import { useComputerWorker } from "../hooks/useComputerWorker";
import VirtualMachine from "./VirtualMachine";
import Stack from "./Stack";
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
    <div style={{ display: "flex" }}>
      <div>
        <button onClick={openFileSelector}>Select ROM</button>
        <button onClick={run}>Run</button>
        <button onClick={stop}>Stop</button>
        <button onClick={clock}>Clock</button>
        <button onClick={reset}>Reset</button>
      </div>
      {computer && (
        <ComputerContext.Provider value={computer}>
          <ROM onSelectROM={openFileSelector} />
          <Stack />
          <VirtualMachine />
          <div>
          <h1>B: {computer.registers.B}</h1>
          <h1>C: {computer.registers.C}</h1>
          <h1>AHigh: {computer.registers.AHigh}</h1>
          <h1>ALow: {computer.registers.ALow}</h1>
          </div>
        </ComputerContext.Provider>
      )}
    </div>
  );
};

import React, { useContext } from "react";
import { combineBytes } from "../lib/combineBytes";
import { ComputerContext } from "./Emulator";
import Paper from "./Paper";
import Value from "./Value";

const VirtualMachine = () => {
  const computer = useContext(ComputerContext);

  const stack = combineBytes(computer.memory.RAM[1], computer.memory.RAM[0]);
  const argument = combineBytes(computer.memory.RAM[3], computer.memory.RAM[2]);
  const local = combineBytes(computer.memory.RAM[5], computer.memory.RAM[4]);

  return (
    <Paper title="Virtual Machine">
      <Value title="Stack Pointer" value={stack} />
      <Value title="Argument Pointer" value={argument} />
      <Value title="Local Pointer" value={local} />
    </Paper>
  );
};

export default VirtualMachine;

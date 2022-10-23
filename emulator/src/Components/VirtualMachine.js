import React, { useContext } from "react";
import { combineBytes } from "../lib/combineBytes";
import { ComputerContext } from "./Emulator";
import Paper from "./Paper";
import Value from "./Value";

const VirtualMachine = () => {
  const computer = useContext(ComputerContext);

  const stack = computer.memory.RAM[0]
  const local = computer.memory.RAM[1]
  const argument = computer.memory.RAM[2]

  return (
    <Paper title="Virtual Machine">
      <Value title="Stack Pointer" value={stack} />
      <Value title="Local Pointer" value={local} />
      <Value title="Argument Pointer" value={argument} />
    </Paper>
  );
};

export default VirtualMachine;

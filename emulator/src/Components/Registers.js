import React, { useContext } from "react";
import { combineBytes } from "../lib/combineBytes";
import { ComputerContext } from "./Emulator";
import Paper from "./Paper";
import Value from "./Value";

const Registers = () => {
  const [computer ] = useContext(ComputerContext);

  const B = computer.registers.B
  const C = computer.registers.C

  const AHigh = computer.registers.AHigh
  const ALow = computer.registers.ALow

  const A = combineBytes(AHigh, ALow)

  let data = null
  try {
    data = computer.readMemory(A)
  } catch (e) {
    data = null;
  }

  return (
    <Paper title="Values">
      <Value title="B" value={B} wide/>
      <Value title="C" value={C} wide/>
      <Value title="AHigh" value={AHigh} wide/>
      <Value title="ALow" value={ALow} wide/>
      <Value title="A" value={A} bit16 wide />
      <Value title="*A" value={data} wide />
    </Paper>
  );
};

export default Registers;

import React, { useContext } from "react";
import Computer from "../core/Computer";
import { ComputerContext } from "./Emulator";

const Stack = () => {
  const [computer] = useContext(ComputerContext);
  //   console.log('computer.memory.RAM[0],computer.memory.RAM[1]', computer.memory.RAM[0],computer.memory.RAM[1])
  //   return <></>
  const stackItems =
    computer.memory.RAM[0] -
    Computer.START_RAM -
    Computer.STACK_START;

  const displayedStack = computer.memory.RAM.slice(
    Math.max(
      Computer.STACK_START,
      stackItems + Computer.STACK_START - 10
    ),
    stackItems + Computer.STACK_START
  ).slice(-10)
  
  // const stackEnd = Computer.STACK_START + stackItems;
  return (
    <div>
      <ul>
        {displayedStack.map((val) => {
          return <li>{val}</li>;
        })}
      </ul>
    </div>
  );
};

export default Stack;

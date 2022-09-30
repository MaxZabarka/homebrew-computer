import React, { useContext } from "react";
import { ComputerContext } from "./Emulator";
import Paper from "./Paper";
import "./ROM.scss";

const ROM = (props) => {
  const computer = useContext(ComputerContext);
  console.log("computer", computer);
  return (
    <Paper title="ROM" className="ROM">
      <ol>
        {computer.memory.ROM.map((value, address) => {
          const focused =
            computer.programCounter === address ||
            computer.programCounter + 1 === address;
          return (
            <li className={focused && "active"}>
              <div className="address">{address}</div>
              <div className="value"></div>
              {address % 2 === 0 &&
                computer.disassemble(value, computer.memory.ROM[address + 1])}
            </li>
          );
        })}
      </ol>
    </Paper>
  );
};

export default ROM;

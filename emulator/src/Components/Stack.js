import React, { useContext, useEffect } from "react";
import Computer from "../core/Computer";
import { ComputerContext } from "./Emulator";
import Paper from "./Paper";
import "./Stack.scss";
import { useAutoAnimate } from "@formkit/auto-animate/react";
import { HiArrowLongLeft } from "react-icons/hi2";

const Stack = () => {
  const [computer] = useContext(ComputerContext);
  const [parent] = useAutoAnimate(/* optional config */);

  // const listRef = useRef(null)
  // const wrapperRef = useRef(null)
  // const fillerRef = useRef(null)
  const stackPointer = computer.memory.RAM[0];
  const localPointer = computer.memory.RAM[1];
  const argumentPointer = computer.memory.RAM[2];

  const stackItems = stackPointer - Computer.START_RAM - Computer.STACK_START;
  // const stackItems = 5;

  const displayedStack = computer.memory.RAM.slice(
    Computer.STACK_START,
    stackItems + Computer.STACK_START
  );

  useEffect(() => {}, [stackItems]);

  return (
    <Paper className="Stack" title="Stack">
      <div className="wrapper">
        {/* <div className="filler"></div> */}
        <ul ref={parent}>
        <div className="bottom"></div>

          {/* <div className="placeholder"></div> */}
          {displayedStack.map((val, i) => {
            let className = "";
            className +=
              localPointer === i + Computer.STACK_START ? " local " : "";
            className +=
              argumentPointer === i + Computer.STACK_START ? " argument " : "";
            console.log(
              "i+Computer.STACK_START :>> ",
              i + Computer.STACK_START
            );
            return (
              <li className={className} key={`${i}`}>
                {val}
                <div className="arg-arrow"><HiArrowLongLeft/> Argument</div>
                <div className="lcl-arrow">Local <HiArrowLongLeft/></div>
              </li>
            );
          })}

        </ul>
      </div>
    </Paper>
  );
};

export default Stack;

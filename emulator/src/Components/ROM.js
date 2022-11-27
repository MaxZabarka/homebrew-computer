import React, {
  forwardRef,
  useContext,
  useEffect,
  useImperativeHandle,
  useRef,
  useState,
} from "react";
import { ComputerContext } from "./Emulator";
import IconBar from "./IconBar";
import Paper from "./Paper";
import { MdSearch } from "react-icons/md";
import "./ROM.scss";
import IconButton from "./IconButton";

const toggleSetElement = (set, element) => {
  if (set.has(element)) {
    set.delete(element);
  } else {
    set.add(element);
  }
};

const ROM = forwardRef((props, ref) => {
  const [computer] = useContext(ComputerContext);
  // const [breakpoints, setBreakpoints] = useState(computer.breakpoints);

  const toggleBreakpoint = (address) => {
    props.setBreakpoints((oldBreakpoints) => {
      const newBreakpoints = new Set(oldBreakpoints);
      toggleSetElement(newBreakpoints, address);
      return newBreakpoints;
    });
  };

  const scrollActiveIntoView = (smooth = true) => {
    document.querySelector(".focused-bottom").scrollIntoView({
      behavior: smooth ? "smooth" : "auto",
      block: "center",
      inline: "center",
    });
  };
  useImperativeHandle(
    ref,
    () => {
      return {
        scrollActiveIntoView,
      };
    },
    []
  );

  return (
    <Paper title="ROM" className="ROM">
      <IconBar>
        <IconButton onClick={scrollActiveIntoView}>
          <MdSearch />
        </IconButton>
      </IconBar>
      <ol>
        {computer.memory.ROM.map((value, address) => {
          const focusedTop = computer.programCounter === address;
          const focusedBottom = computer.programCounter + 1 === address;
          let className = focusedTop
            ? "focused-top"
            : focusedBottom
            ? "focused-bottom"
            : "";
          if (props.breakpoints.has(address)) {
            className += " breakpoint";
          }

          return (
            <li
              key={address}
              onClick={() => {
                toggleBreakpoint(address);
              }}
              className={className}
            >
              {address % 2 === 0 && (
                <button className="breakpoint-button">
                  <div />
                </button>
              )}
              <div className="address">{address}</div>
              <div className="value">
                {address % 2 === 0 &&
                  computer.disassemble(value, computer.memory.ROM[address + 1])}
              </div>
            </li>
          );
        })}
      </ol>
    </Paper>
  );
});

export default ROM;

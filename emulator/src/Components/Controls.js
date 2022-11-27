import React from "react";
import "./Controls.scss";
import { AiOutlineFolderOpen } from "react-icons/ai";
import {
  VscDebugRestart,
  VscDebugStart,
  VscDebugStop,
  VscRunAll,
} from "react-icons/vsc";
import { GrClear } from "react-icons/gr";
const Controls = ({
  openFileSelector,
  run,
  stop,
  clock,
  reset,
  clearBreakpoints,
  running,
}) => {
  return (
    <div className="Controls">
      <div>
        <button disabled={running} onClick={openFileSelector}>
          Select ROM
          <AiOutlineFolderOpen className="icon" />
        </button>

        <button disabled={running} onClick={clearBreakpoints}>
          Clear breakpoints
          <GrClear />
        </button>
      </div>
      <div>
        <button disabled={running} onClick={clock}>
          Clock
          <VscDebugStart style={{ marginLeft: "-0.5rem" }} />
        </button>
        <button disabled={running} onClick={run}>
          Run
          <VscRunAll />
        </button>
        <button disabled={!running} onClick={stop}>
          Stop
          <VscDebugStop style={{ marginLeft: "-0.2rem" }} />
        </button>
        <button disabled={running} onClick={reset}>
          Reset
          <VscDebugRestart />
        </button>
      </div>
    </div>
  );
};

export default Controls;

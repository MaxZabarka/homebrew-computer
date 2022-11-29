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
  onSpeedChange,
  speed,
  fileName,
  actualSpeed,
}) => {
  let formattedActualSpeed = null;
  if (actualSpeed) {
    actualSpeed = actualSpeed * 3;

    if (actualSpeed > 100_000) {
      formattedActualSpeed = `${(actualSpeed / 1_000_000).toFixed(2)}MHz`;
    } else {
      formattedActualSpeed = `${actualSpeed.toFixed(2)}Hz`;
    }
  }
  console.log("actualSpeed :>> ", actualSpeed);
  console.log("formattedActualSpeed :>> ", formattedActualSpeed);

  return (
    <div className="Controls">
      <div>
        <button disabled={running} onClick={openFileSelector}>
          Select ROM
          <AiOutlineFolderOpen className="icon" />
        </button>
        <div className="filename">{fileName}</div>
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
        <div className="slider">
          <input
            disabled={running && parseFloat(speed) === 1}
            type="range"
            value={speed}
            step={0.2}
            min="0"
            max="1"
            onChange={(e) => {
              if (running && parseFloat(e.target.value) === 1) {
                return;
              }
              onSpeedChange(e.target.value);
            }}
          ></input>
          <div className="speed">
            <div>
              {parseFloat(speed) === 1
                ? " (no limit)"
                : (1 / (((1 - speed) * 500) / 1000)).toFixed(2) +
                  " instructions/s"}
              {/* 500 referenced in emulator.js too */}
            </div>
            <div className="light">
              {running && actualSpeed && formattedActualSpeed}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Controls;

import React from "react";
import { toBinary } from "../lib/toBinary";
import "./Value.scss";

const Value = (props) => {
  let binary = "N/A";
  let hex = "N/A";
  let decimal = "N/A";
  
  if (!(props.value === null || props.value === undefined)) {
    if (props.bit16) {
      binary = toBinary(props.value, 16);
    } else {
      binary = toBinary(props.value, 8);
    }
     hex = props.value.toString(16);
     decimal = props.value;
  }
  return (
    <div className="Value">
      <h2>{props.title}</h2>
      <div className={"row " + (props.wide && "wide")}>
        <div>
          <p className="label">Decimal</p>
          <p className="num">{decimal}</p>
        </div>
        <div className="binary">
          <p className="label">Binary</p>
          <p className="num">{binary}</p>
        </div>
        <div>
          <p className="label">Hex</p>
          <p className="num">{hex}</p>
        </div>
      </div>
    </div>
  );
};

export default Value;

import React from "react";
import { toBinary } from "../lib/toBinary";
import "./Value.scss";

const Value = (props) => {
  const binary = toBinary(props.value, 8);
  const hex = props.value.toString(16);

  return (
    <div className="Value">
      <h2>{props.title}</h2>
      <div className="row">
        <div>
          <p className="label">Decimal</p>
          <p className="num">{props.value}</p>
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

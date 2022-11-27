import React from "react";
import "./IconButton.scss";

const IconButton = (props) => {
  return (
    <button onClick={props.onClick} className="IconButton">
      {props.children}
    </button>
  );
};

export default IconButton;

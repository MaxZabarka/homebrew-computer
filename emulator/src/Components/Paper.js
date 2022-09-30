import React from "react";
import "./Paper.scss";

const Paper = (props) => {
  return (
    <div className={"Paper " + props.className}>
      <h1 className="title">{props.title}</h1>
      {props.children}
    </div>
  );
};

export default Paper;

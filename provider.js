import React from "react";

export default (props) => {
  return (
    <div>
      {props.children}
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          fontSize: 16,
          padding: "15px 30px",
          bottom: 0,
          color: "white"
        }}
      >
        Use ← → to navigate or swipe 
      </div>
    </div>
  );
};
import React from "react";
import { extend } from "react-three-fiber";
import CustomLine from "../CustomLine/CustomLine";
import { TextMesh } from "troika-3d-text/dist/textmesh-standalone.umd.js";

extend({ TextMesh });

const Hyperlane = ({ points, name, color }) => {
  return (
    <>
      <CustomLine
        points={points.map((point) => [...point, 0])}
        color={color}
      ></CustomLine>
    </>
  );
};

export default Hyperlane;

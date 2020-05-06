import Text from "../Text/Text";
import PropTypes from "prop-types";
import React, { useState, useRef } from "react";
import CustomLine from "../CustomLine/CustomLine";

const Hyperlane = ({ points, name, color }) => {
  const [hovered, setHover] = useState(false);
  const [textPosition, setTextPosition] = useState([]);

  const mesh = useRef();

  // const handleMouseOver = (e) => {
  //   setHover(true);
  //   setTextPosition(e.point)
  // }

  // const handleMouseLeave = (e) => {
  //   setHover(false)
  //   setTextPosition([])
  // }

  return (
    <group>
      <CustomLine
        points={points.map((point) => [...point, 0])}
        color={color}
      ></CustomLine>
      {hovered ? <Text text={name} position={textPosition} /> : null}
    </group>
  );
};

Hyperlane.propTypes = {
  points: PropTypes.arrayOf(PropTypes.array),
  color: PropTypes.string,
  name: PropTypes.string,
};

Hyperlane.defaultProps = {
  points: [[0, 0, 0]],
  color: "lightblue",
  name: "",
};

export default Hyperlane;

import React from "react";
import PropTypes from "prop-types";
import { useThree, extend } from "@react-three/fiber";
import { Text } from "troika-three-text";

extend({ Text });

const CustomText = ({ text, position, color }) => {
  const { camera } = useThree();

  return (
    <text
      rotation={camera.rotation}
      position={position}
      text={text}
      font="http://localhost:3000/fonts/STARWARS.ttf"
      fontSize={1.5}
      anchorX={0.5}
      anchorY={0.5}
    >
      <meshPhongMaterial attach="material" color={color}></meshPhongMaterial>
    </text>
  );
};

CustomText.propTypes = {
  position: PropTypes.arrayOf(PropTypes.number),
  text: PropTypes.string,
  color: PropTypes.string,
};

CustomText.defaultProps = {
  position: [0, 0, 0],
  text: "",
  color: "white",
};

export default CustomText;

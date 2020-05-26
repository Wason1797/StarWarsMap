import Text from "../Text/Text";
import PropTypes from "prop-types";
import React, { useRef, useState } from "react";

const Planet = (props) => {
  const mesh = useRef();

  const [hovered, setHover] = useState(false);

  const [x, y] = props.position;

  const handleClick = () => {
    props.handleExternalClick(props.name, [x, y, 100]);
  };

  return (
    <>
      <mesh
        position={props.position}
        ref={mesh}
        scale={[0.5, 0.5, 0.5]}
        onPointerOver={(e) => setHover(true)}
        onPointerOut={(e) => setHover(false)}
        onClick={(e) => handleClick()}
      >
        <sphereBufferGeometry
          attach="geometry"
          args={[1, 32, 32]}
        ></sphereBufferGeometry>

        <meshStandardMaterial
          attach="material"
          color={hovered ? props.specialColor : props.normalColor}
        ></meshStandardMaterial>
      </mesh>
      {hovered ? <Text text={props.name} position={[x, y, 3.5]} /> : null}
    </>
  );
};

Planet.propTypes = {
  position: PropTypes.arrayOf(PropTypes.number),
  handleClick: PropTypes.func,
  name: PropTypes.string,
  normalColor: PropTypes.string,
  specialColor: PropTypes.string,
};

Planet.defaultProps = {
  handleExternalClick: (e) => {},
  position: [0, 0, 0],
  normalColor: "orange",
  specialColor: "hotpink",
};

export default Planet;

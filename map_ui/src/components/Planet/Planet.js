import React, { useRef, useState } from "react";
import { useThree, extend } from "react-three-fiber";
import { TextMesh } from "troika-3d-text/dist/textmesh-standalone.umd.js";

import PropTypes from "prop-types";

extend({ TextMesh });

const Planet = (props) => {
  const mesh = useRef();

  const [hovered, setHover] = useState(false);

  const { camera } = useThree();

  const [x, y] = props.position;

  return (
    <>
      <mesh
        position={props.position}
        ref={mesh}
        scale={[0.65, 0.65, 0.65]}
        onPointerOver={(e) => setHover(true)}
        onPointerOut={(e) => setHover(false)}
        onClick={(e) => props.handleClick(props.name)}
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
      {hovered ? (
        <textMesh
          rotation={camera.rotation}
          position={[x, y, 3.5]}
          text={props.name}
          font="http://localhost:3000/fonts/STARWARS.ttf"
          fontSize={1.5}
          anchorX={0.5}
          anchorY={0.5}
        >
          <meshPhongMaterial
            attach="material"
            color="white"
          ></meshPhongMaterial>
        </textMesh>
      ) : null}
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
  handleClick: (e) => {},
  position: [0, 0, 0],
  normalColor: "orange",
  specialColor: "hotpink",
};

export default Planet;

import * as THREE from "three";
import PropTypes from "prop-types";
import { extend } from "react-three-fiber";
import * as meshline from "threejs-meshline";
import React, { useRef, useState } from "react";

extend(meshline);

const CustomLine = ({ points, color, maxSamples }) => {
  const material = useRef();
  const mesh = useRef();

  const [curvePoints] = useState(
    points.map((point) => new THREE.Vector3(...point))
  );

  return (
    <mesh
      ref={mesh}
      onPointerOver={(e) => {
        console.log(e, "hover");
      }}
    >
      <meshLine attach="geometry">
        <catmullRomCurve3
          args={[curvePoints]}
          onUpdate={(self) => {
            self.parent.vertices = self.getPoints(maxSamples);
          }}
        ></catmullRomCurve3>
      </meshLine>
      <meshLineMaterial
        attach="material"
        ref={material}
        transparent={false}
        dephTest={false}
        lineWidth={0.2}
        color={color}
      ></meshLineMaterial>
    </mesh>
  );
};

CustomLine.propTypes = {
  points: PropTypes.array,
  color: PropTypes.string,
  maxSamples: PropTypes.number,
};

CustomLine.defaultProps = {
  points: [[0, 0, 0]],
  color: "lightblue",
  maxSamples: 500,
};

export default CustomLine;

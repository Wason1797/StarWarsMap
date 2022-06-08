import React, { useRef, useState } from "react";
import PropTypes from "prop-types";
import { extend } from "@react-three/fiber";
import * as meshline from 'threejs-meshline'
import * as THREE from 'three';

extend(meshline);

const CustomLine = ({ points, color, maxSamples }) => {
  const material = useRef();


  const [curvePoints] = useState(
    points.map((point) => new THREE.Vector3(...point))
  );

  const [curve] = useState(() => {
    return new THREE.CatmullRomCurve3(curvePoints).getPoints(500);
  });

  return (
    <mesh>
      <meshLine attach="geometry" vertices={curve} />
      <meshLineMaterial
        attach="material"
        ref={material}
        transparent={false}
        depthTest={false}
        lineWidth={0.2}
        color={color}
      />
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
  color: "#A2CCB6",
  maxSamples: 500,
};

export default CustomLine;

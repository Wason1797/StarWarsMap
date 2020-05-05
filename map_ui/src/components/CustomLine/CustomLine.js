import * as THREE from "three";
import { extend } from "react-three-fiber";
import * as meshline from "threejs-meshline";
import React, { useRef, useState } from "react";

extend(meshline);

const CustomLine = ({ points, color, onMouseHover, onMouseOut }) => {
  const material = useRef();

  const [curvePoints] = useState(
    points.map((point) => new THREE.Vector3(...point))
  );

  return (
    <mesh
    onPointerOver={e => console.log("hover")}>
      <meshLine onUpdate={(self) => (self.parent.geometry = self.geometry)}>
        <geometry onUpdate={(self) => self.parent.setGeometry(self)}>
          <catmullRomCurve3
            args={[curvePoints]}
            onUpdate={(self) => {
              self.parent.vertices = self.getPoints(500);
            }}
          ></catmullRomCurve3>
        </geometry>
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

export default CustomLine;

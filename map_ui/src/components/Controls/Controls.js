import React, { useRef, useImperativeHandle, forwardRef } from "react";
import { extend, useThree, useFrame } from "@react-three/fiber";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";

extend({ OrbitControls });

const Controls = forwardRef(({}, ref) => {
  const controlsRef = useRef();
  const { camera, gl } = useThree();

  useImperativeHandle(ref, () => {
    return {
      updateCamera: (position) => {
        console.log(camera.position);
        // const rotation = camera.rotation
        // const [x, y, z] = position
        // camera.position.set(x, y-50, 100);
        // camera.setRotationFromEuler(rotation)
      },
    };
  });

  useFrame(() => controlsRef.current && controlsRef.current.update());

  return (
    <orbitControls
      ref={controlsRef}
      args={[camera, gl.domElement]}
      enableRotate
      enablePan
      enableDamping
      dampingFactor={0.1}
      maxDistance={250}
      minDistance={1}
      minPolarAngle={Math.PI / 6}
      maxPolarAngle={Math.PI / 2}
    ></orbitControls>
  );
});

export default Controls;

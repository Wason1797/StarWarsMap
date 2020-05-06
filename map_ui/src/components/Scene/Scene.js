import React, { useRef } from "react";
import { useThree } from "react-three-fiber";

import Controls from "../Controls/Controls";
import Space from "../Space/Space";

const Scene = () => {
  const { camera } = useThree();
  const controlsRef = useRef();

  camera.fov = 45;
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.near = 0.1;
  camera.far = 1000;
  camera.up.set(0, 0, 1);
  camera.position.set(0, 0, 100);

  return (
    <>
      <Space controls={controlsRef} />
      <Controls
        ref={(ref) => {
          controlsRef.current = ref;
        }}
      />
    </>
  );
};

export default Scene;

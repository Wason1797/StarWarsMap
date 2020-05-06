import Planet from "../Planet/Planet";
import Hyperlane from "../Hyperlane/Hyperlane";
import CustomLine from "../CustomLine/CustomLine";
import React, { useEffect, useState } from "react";
import { onPlanetClick } from "../../functions/eventHandler";

import { getPlanets, getHyperlanes } from "../../functions/apiHandler";

const Space = (props) => {
  const [planets, setPlanets] = useState([]);
  const [hyperlanes, setHyperlanes] = useState([]);
  const [path, setPath] = useState([]);
  const [startPlanet, setStartPlanet] = useState("");

  useEffect(() => {
    getPlanets()
      .then((response) => response.json())
      .then((data) => setPlanets(data))
      .catch((ex) => setPlanets([]));

    getHyperlanes()
      .then((response) => response.json())
      .then((data) => setHyperlanes(data))
      .catch((ex) => setHyperlanes([]));
  }, []);

  const handlePlanetClick = (planetName, planetPosition) => {
    onPlanetClick(planets, startPlanet, planetName, setStartPlanet, setPath);
    props.controls.current.updateCamera(planetPosition);
  };

  return (
    <>
      <ambientLight />
      <pointLight position={[window.innerWidth, window.innerHeight, 10]} />
      <group>
        {hyperlanes.map((lane) => (
          <Hyperlane
            key={lane.name}
            points={lane.points}
            name={lane.name}
            color="lightblue"
          ></Hyperlane>
        ))}
      </group>
      {path.length > 0 ? (
        <CustomLine points={path} color="red" maxSamples={250}></CustomLine>
      ) : null}
      <group>
        {planets.map((planet, index) => {
          const [x, y] = planet.location;
          return (
            <Planet
              key={index}
              position={[x, y, 0]}
              name={planet.name}
              handleExternalClick={handlePlanetClick}
            ></Planet>
          );
        })}
      </group>
    </>
  );
};

export default Space;

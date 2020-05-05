import React, { useEffect, useState } from "react";
import Planet from "../Planet/Planet";
import Hyperlane from "../Hyperlane/Hyperlane";
import CustomLine from "../CustomLine/CustomLine";

import {
  getPlanets,
  getHyperlanes,
  getPathBetweenPlanets,
} from "../../functions/apiHandler";

const Space = () => {
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

  const handlePlanetClick = (planetName) => {

    if (planets.length > 0) {
      if (startPlanet === "") {
        setStartPlanet(planetName);
      } else if (planetName !== startPlanet) {
        getPathBetweenPlanets(startPlanet, planetName)
          .then((response) => response.json())
          .then((path) => {
            setPath([]);
            setPath(path.map((point) => [...point, 0]));
            setStartPlanet("");
          })
          .catch((ex) => {
            setPath([]);
            setStartPlanet("");
          });
      }
    }
  };

  return (
    <>
      <ambientLight />
      <pointLight position={[window.innerWidth, window.innerHeight, 10]} />

      {hyperlanes.map((lane) => (
        <Hyperlane
          key={lane.name}
          points={lane.points}
          name={lane.name}
          color="lightblue"
        ></Hyperlane>
      ))}
      {path.length > 0 ? (
        <CustomLine points={path} color="red"></CustomLine>
      ) : null}

      {planets.map((planet, index) => {
        const [x, y] = planet.location;
        return (
          <Planet
            key={index}
            position={[x, y, 0]}
            name={planet.name}
            handleClick={handlePlanetClick}
          ></Planet>
        );
      })}
    </>
  );
};

export default Space;

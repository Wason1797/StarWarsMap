import { getPathBetweenPlanets } from "./apiHandler";

const onPlanetClick = (
  planets,
  startPlanet,
  planetName,
  setStartPlanetCallback,
  setPathCallback
) => {
  if (planets.length > 0) {
    if (startPlanet === "") {
      setStartPlanetCallback(planetName);
    } else if (planetName !== startPlanet) {
      getPathBetweenPlanets(startPlanet, planetName)
        .then((response) => response.json())
        .then((path) => {
          setPathCallback([]);
          setPathCallback(path.map((point) => [...point, 0]));
          setStartPlanetCallback("");
        })
        .catch((ex) => {
          setPathCallback([]);
          setStartPlanetCallback("");
        });
    }
  }
};

export { onPlanetClick };

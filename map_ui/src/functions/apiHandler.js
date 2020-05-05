const BASE_URL = "http://localhost:5000";

const getPlanets = () => {
  return fetch(`${BASE_URL}/planets`);
};

const getHyperlanes = () => {
  return fetch(`${BASE_URL}/hyperlanes/points`);
};

const getPathBetweenPlanets = (startPlanet, endPlanet) => {
  return fetch(
    `${BASE_URL}/hyperlanes/shortest-path/points/${startPlanet}/${endPlanet}`
  );
};

export { getPlanets, getHyperlanes, getPathBetweenPlanets };

import { Runtime, Inspector } from "https://cdn.jsdelivr.net/npm/@observablehq/runtime@4/dist/runtime.js";
import weatherNotebook from "https://api.observablehq.com/@kennsmithds/portland-maine-weather-with-legends.js?v=3";
const main = new Runtime().module(weatherNotebook, name => {
    if (name === "viewof weatherHeatMap") return new Inspector.into("#weatherHeatMap")();
    if (name === "viewof smellHeatMap") return new Inspector.into("#smellHeatMap")();
    if (name === "viewof weatherInput") return new Inspector.into("#weatherFeatures")();
    return true;
});
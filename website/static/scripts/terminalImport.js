import { Runtime, Inspector } from "https://cdn.jsdelivr.net/npm/@observablehq/runtime@4/dist/runtime.js";
import stinkyNotebook from "https://api.observablehq.com/d/c2397f201500cb0c.js?v=3";
const main = new Runtime().module(stinkyNotebook, name => {
    if (name === "viewof terminalsData") return Inspector.into("#terminalHistogram")();
    if (name === "viewof productTypeData") return Inspector.into("#cargoType")();
    return true;
});
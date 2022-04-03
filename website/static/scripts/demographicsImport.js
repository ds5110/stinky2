import { Runtime, Inspector } from "https://cdn.jsdelivr.net/npm/@observablehq/runtime@4/dist/runtime.js";
import demoNotebook from "https://api.observablehq.com/@kennsmithds/portland-maine-demographics-with-malodorous-time-series-h.js?v=3";
const main = new Runtime().module(demoNotebook, name => {
    if (name === "viewof smellDensityMap") return Inspector.into("#demoMap")();
    if (name === "viewof weatherDateSlider") return Inspector.into("#demoTimeBrush")();
    if (name === "viewof selectedFeature") return Inspector.into("#demoDropdown")();
    if (name === "demoLegend") return Inspector.into("#demoLegend")();
    return true;
});
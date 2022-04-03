import { Runtime, Inspector } from "https://cdn.jsdelivr.net/npm/@observablehq/runtime@4/dist/runtime.js";
import define from "https://api.observablehq.com/d/f6cce0018383da27.js?v=3";
new Runtime().module(define, name => {
    if (name === "viewof mymap") return new Inspector(document.querySelector("#observablehq-viewof-mymap-5263f343"));
    if (name === "viewof datesFilter") return new Inspector(document.querySelector("#observablehq-viewof-datesFilter-5263f343"));
    if (name === "viewof shipNameFilter") return new Inspector(document.querySelector("#observablehq-viewof-shipNameFilter-5263f343"));
    if (name === "viewof productTypeFilter") return new Inspector(document.querySelector("#observablehq-viewof-productTypeFilter-5263f343"));
    if (name === "viewof terminalFilter") return new Inspector(document.querySelector("#observablehq-viewof-terminalFilter-5263f343"));
    if (name === "viewof selectAllFilter") return new Inspector(document.querySelector("#observablehq-viewof-selectAllFilter-5263f343"));
    if (name === "viewof stinkyDateSlider") return new Inspector(document.querySelector("#observablehq-viewof-stinkyDateSlider-5263f343"));
    if (name === "viewof mapData") return new Inspector(document.querySelector("#observablehq-viewof-mapData-42f2f98d"));

    return ["filteredData", "stinkyDataGeo", "stinkyDataCollection", "inclusiveFilteredVesselsData", "viewof filteredVesselsProductType", "viewof filteredVesselsTerminal", "DatesFromFilteredVesselsData", "filteredTerminals", "terminalsDataGeo", "terminalsLocationDataCollection", "smellDensityMap", "exclusiveFilteredVesselsData", "vesselsVar", "selectedDatesVesselsData", "viewof mapData"].includes(name);
});

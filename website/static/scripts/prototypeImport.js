import { Runtime, Inspector } from "https://cdn.jsdelivr.net/npm/@observablehq/runtime@4/dist/runtime.js";
import define from "https://api.observablehq.com/@iellms/prototype-1-ian-ellmer.js?v=3";
const main = new Runtime().module(define, name => {
    if (name === "viewof mymapOldIan") return new Inspector.into("#originalMap")();
    return true;
});
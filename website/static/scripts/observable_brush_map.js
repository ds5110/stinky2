// import define1 from "/@pbogden/click-to-recenter-brush-iii.js?v=3";
// import define1 from "{{url_for('static', filename='scripts/recenter.js')}}";
import define1 from "./recenter.js";

function _1(md){return(
md`# My Zoomable Raster & Vector II

This version adds random points and a brush to filter them, in the spirit of [Brushable Earthquakes](https://observablehq.com/@pbogden/brushable-earthquakes?collection=@pbogden/earthquakes).`
)}

function _map(replay,d3,width,height,initialScale,initialCenter,url,features)
{
  replay
  
  const svg = d3.create("svg")
      .attr("viewBox", [0, 0, width, height]);

  const projection = d3.geoMercator()
      .scale(1 / (2 * Math.PI))
      .translate([0, 0]);

  const render = d3.geoPath(projection);

  const tile = d3.tile()
      .extent([[0, 0], [width, height]])
      .tileSize(512);

  const zoom = d3.zoom()
      .scaleExtent([1 << 15, 1 << 24])
      .extent([[0, 0], [width, height]])
      .on("zoom", ({transform}) => zoomed(transform));

  let image = svg.append("g")
      .attr("pointer-events", "none")
    .selectAll("image");

  const path = svg.append("path")
      .attr("pointer-events", "none")
      .attr("fill", "none")
      .attr("stroke", "red")
      .attr("stroke-linecap", "round")
      .attr("stroke-linejoin", "round");

  svg
      .call(zoom)
      .call(zoom.transform, d3.zoomIdentity
          .translate(width / 2, height / 2)
          .scale(-initialScale)
          .translate(...projection(initialCenter))
          .scale(-1));

  const m = 10, rng = d3.randomBates(1);
  const points = Array.from({ length: 50 }, () => [rng() * (width - 2 * m) + m, rng() * (height - 2 * m) + m]);
  const data = points.map(d => projection.invert(d))

  svg.selectAll("circle")
    .data(data)
    .join("circle")
      .attr("fill", "black")
      .attr("transform", d => ("translate(" + projection(d) + ")") )
      .attr("r", 5)

  function zoomed(transform) {
    const tiles = tile(transform);

    image = image.data(tiles, d => d).join("image")
        .attr("xlink:href", d => url(...d))
        .attr("x", ([x]) => (x + tiles.translate[0]) * tiles.scale)
        .attr("y", ([, y]) => (y + tiles.translate[1]) * tiles.scale)
        .attr("width", tiles.scale)
        .attr("height", tiles.scale);

    projection
        .scale(transform.k / (2 * Math.PI))
        .translate([transform.x, transform.y]);

    path.attr("d", render(features));

    svg.selectAll("circle")
        .attr("transform", d => ("translate(" + projection(d) + ")") )
  }

  // See: https://observablehq.com/@mbostock/shader
  Object.assign(svg.node(), {
      update(values = []) {
        values = values.length > 0 ? values : data;
        svg.selectAll("circle")
          .data(values)
          .join("circle")
            .attr("fill", "black")
            .attr("transform", d => ("translate(" + projection(d) + ")") )
            .attr("r", values.length > 1000 ? 1 : 5) 
      }
    });

  return svg.node();
}


function _brush($0){return(
$0
)}

function _brushed(d3,map,chart,md,data)
{
  d3.select(map).selectAll("circle")
      // .attr("r", (d,i) => i) 
      .attr("fill-opacity", 0.5)
      .attr("stroke", "#f00")
      .attr("visibility", d => (d[0] > chart[0][0] && d[0] < chart[1][0]
                             && d[1] < chart[0][1] && d[1] > chart[1][1]) 
                              ? "visible" : "hidden");
  
  // Count the visible earthquakes on the map
  const n = d3.select(map).selectAll("circle")
      .filter(function() { return d3.select(this).attr("visibility") == "visible" })
      .nodes().length;
  
  return md`${n} out of ${data.length} data points are visible on the map.`
}


function _replay(html){return(
html`<button>Replay`
)}

function _6(md){return(
md`## Data`
)}

function _title(){return(
"This stuff is wicked cool!"
)}

function _data(map,stinky,d3)
{
  map.update(stinky.length > 0 ? stinky : [])

  return d3.select(map).selectAll("circle").data();
}


async function _stinky(d3)
{
  // https://observablehq.com/@mbostock/fetch-error-handling
  // FIXME: use local csv
  // const url='https://raw.githubusercontent.com/ds5110/stinky2/main/output_data/smc_data.csv2';
  const url = "http://localhost:5000/merged_data";
  const response = await fetch(url);
  if (!response.ok) {
    console.log(`Not OK response from fetch: ${response}`);
    return [];
    // throw new Error("sorry about that...unable to fetch");
  }
  return d3.csvParse(await response.text()).map(d => [+d.longitude, +d.latitude]);
}


function _10(md){return(
md`## Appendix`
)}

function _styling(d3,brush)
{
  d3.select(brush).select(".x-axis").attr("font-size", 25);
  d3.select(brush).select(".y-axis").attr("font-size", 25);
}


function _url(){return(
(x, y, z) => `https://${"abc"[Math.abs(x + y) % 3]}.basemaps.cartocdn.com/rastertiles/voyager/${z}/${x}/${y}${devicePixelRatio > 1 ? "@2x" : ""}.png`
)}

function _x(d3,data,margin,width){return(
d3.scaleLinear(d3.extent(data, d => d[0]), [margin.left, width - margin.right])
)}

function _margin(){return(
{top: 10, right: 50, bottom: 30, left: 80}
)}

function _height(){return(
500
)}

function _initialCenter(){return(
[-70.2568, 43.649]
)}

function _initialScale(){return(
1 << 21
)}

function _features(d3,topojson){return(
d3.json("https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json").then(topology => topojson.feature(topology, topology.objects.states))
)}

function _topojson(require){return(
require("topojson-client@3")
)}

function _d3(require){return(
require("d3@6", "d3-tile@1")
)}

export default function define(runtime, observer) {
  const main = runtime.module();
  main.variable(observer()).define(["md"], _1);
  main.variable(observer("map")).define("map", ["replay","d3","width","height","initialScale","initialCenter","url","features"], _map);
  main.variable(observer("brush")).define("brush", ["viewof chart"], _brush);
  main.variable(observer("brushed")).define("brushed", ["d3","map","chart","md","data"], _brushed);
  main.variable(observer("viewof replay")).define("viewof replay", ["html"], _replay);
  main.variable(observer("replay")).define("replay", ["Generators", "viewof replay"], (G, _) => G.input(_));
  main.variable(observer()).define(["md"], _6);
  main.variable(observer("title")).define("title", _title);
  main.variable(observer("data")).define("data", ["map","stinky","d3"], _data);
  main.variable(observer("stinky")).define("stinky", ["d3"], _stinky);
  main.variable(observer()).define(["md"], _10);
  main.variable(observer("styling")).define("styling", ["d3","brush"], _styling);
  main.variable(observer("url")).define("url", _url);
  main.variable(observer("x")).define("x", ["d3","data","margin","width"], _x);
  main.variable(observer("margin")).define("margin", _margin);
  main.variable(observer("height")).define("height", _height);
  main.variable(observer("initialCenter")).define("initialCenter", _initialCenter);
  main.variable(observer("initialScale")).define("initialScale", _initialScale);
  main.variable(observer("features")).define("features", ["d3","topojson"], _features);
  main.variable(observer("topojson")).define("topojson", ["require"], _topojson);
  const child1 = runtime.module(define1).derive(["data","title","x","margin"], main);
  main.import("viewof chart", child1);
  main.import("chart", child1);
  main.variable(observer("d3")).define("d3", ["require"], _d3);
  return main;
}

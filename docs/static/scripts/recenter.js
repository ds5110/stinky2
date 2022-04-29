// https://observablehq.com/@pbogden/click-to-recenter-brush-iv@256
function _1(md){return(
md`# Click to Recenter Brush IV
This version is designed to work in Jupyter.`
)}

function _chart(d3,width,height,margin,data,x,y,yAxis,xAxis,title)
{
  const svg = d3.create("svg")
      .attr("viewBox", [0, 0, width, height]);

  const brush = d3.brush()
      .extent([[margin.left, margin.top], [width - margin.right, height - margin.bottom]])
      .on("start brush end", brushed);

  const circle = svg.append("g")
      .attr("fill-opacity", 0.2)
    .selectAll("circle")
    .data(data)
    .join("circle")
      .attr("transform", d => `translate(${x(d[0])},${y(d[1])})`)
      .attr("r", 3.5);

  svg.append("g")
      .call(yAxis);

  svg.append("g")
      .call(xAxis);

  svg.append("text")
    .attr("text-anchor", "start")
    .attr("font-family", "sans-serif")
    .attr("font-size", ".75em")
    .attr("x", margin.left)
    .attr("y", margin.top)
    .attr("dx", ".5em")
    .attr("dy", ".5em")
    .text(title)

  const dx = (x.range()[1] - x.range()[0]) / 10; // Fixed width for recentering
  const x0 = (d3.mean(x.range())); // Intialize brush on midpoint
  const [y0, y1] = y.range(); // Full height when recentering
  svg.append("g")
      .call(brush)
      .call(brush.move, [[x0 - dx / 2, y1], [x0 + dx / 2, y0]]) // Initialize brush
      .call(g => g.select(".overlay")
          .datum({type: "selection"})
          .on("mousedown touchstart", beforebrushstarted));

  function beforebrushstarted(event) {
    const [[cx, cy]] = d3.pointers(event);
    const [x0, x1] = [cx - dx / 2, cx + dx / 2];
    const [X0, X1] = x.range();
    d3.select(this.parentNode)
        .call(brush.move, x1 > X1 ? [[X1 - dx, y0], [X1, y1]] 
            : x0 < X0 ? [[X0, y0], [X0 + dx, y1]]
            : [[x0, y1], [x1, y0]]);
  }

  function brushed(event) {
    const selection = event.selection;
    if (selection === null) {
      circle.attr("stroke", null);
    } else {
      const [[a0, b0], [a1, b1]] = selection;
      const [x0, x1] = [a0, a1].map(x.invert);
      const [y0, y1] = [b0, b1].map(y.invert);
      circle.attr("stroke", d => x0 <= d[0] && d[0] <= x1 && d[1] <= y0 && y1 <= d[1] ? "red" : null);
      svg.node().value = [[x0, y0], [x1, y1]];
      svg.node().dispatchEvent(new CustomEvent("input"));
    }
  }

  return svg.node();
}


async function _source(html,d3)
{
  const textarea = html`<textarea rows=10>`;
  const url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.geojson";
  textarea.value = await d3.text(url);
  return textarea;
}


function _data(source){return(
JSON.parse(source).features.map(d => [d.properties.time, d.properties.mag, d])
)}

function _title(){return(
"magnitude"
)}

function _xAxis(height,margin,d3,x){return(
g => g
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x).ticks(6))
)}

function _yAxis(margin,d3,y){return(
g => g
    .attr("transform", `translate(${margin.left}, 0)`)
    .call(d3.axisLeft(y).ticks(3))
)}

function _x(d3,data,margin,width){return(
d3.scaleTime(d3.extent(data, d => d[0]), [margin.left, width - margin.right])
)}

function _y(d3,data,height,margin){return(
d3.scaleLinear(d3.extent(data, d => d[1]), [height - margin.bottom, margin.top])
)}

function _margin(){return(
{top: 10, right: 20, bottom: 20, left: 20}
)}

function _height(){return(
120
)}

function _d3(require){return(
require("d3@6")
)}

export default function define1(runtime, observer) {
  const main = runtime.module();
  main.variable(observer()).define(["md"], _1);
  main.variable(observer("viewof chart")).define("viewof chart", ["d3","width","height","margin","data","x","y","yAxis","xAxis","title"], _chart);
  main.variable(observer("chart")).define("chart", ["Generators", "viewof chart"], (G, _) => G.input(_));
  main.variable(observer("viewof source")).define("viewof source", ["html","d3"], _source);
  main.variable(observer("source")).define("source", ["Generators", "viewof source"], (G, _) => G.input(_));
  main.variable(observer("data")).define("data", ["source"], _data);
  main.variable(observer("title")).define("title", _title);
  main.variable(observer("xAxis")).define("xAxis", ["height","margin","d3","x"], _xAxis);
  main.variable(observer("yAxis")).define("yAxis", ["margin","d3","y"], _yAxis);
  main.variable(observer("x")).define("x", ["d3","data","margin","width"], _x);
  main.variable(observer("y")).define("y", ["d3","data","height","margin"], _y);
  main.variable(observer("margin")).define("margin", _margin);
  main.variable(observer("height")).define("height", _height);
  main.variable(observer("d3")).define("d3", ["require"], _d3);
  return main;
}

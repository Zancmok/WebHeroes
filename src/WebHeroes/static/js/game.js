// ─── Field Type Definitions ───────────────────────────────────────────────────
// Pure descriptors: name, display_name, color, resource only.
// No weight, minimum_amount, or number_tokens here.

const FIELD_TYPES = [
  { name: "outer-bound",  display_name: "Ocean",    color: "#1a4a7a", resource: null     },
  { name: "desert",       display_name: "Desert",   color: "#d4b878", resource: null     },
  { name: "hills",        display_name: "Hills",    color: "#c0522a", resource: "brick"  },
  { name: "forest",       display_name: "Forest",   color: "#2d6b3a", resource: "lumber" },
  { name: "mountains",    display_name: "Mountains",color: "#7a7a8a", resource: "ore"    },
  { name: "fields",       display_name: "Fields",   color: "#d4c43a", resource: "grain"  },
  { name: "pasture",      display_name: "Pasture",  color: "#7bbf50", resource: "wool"   },
];

// ─── Distribution Config ──────────────────────────────────────────────────────
// Weights and minimum tile counts live here, separate from type descriptors.
// number_tokens will be added in a later step.

const FIELD_DISTRIBUTION = {
  "desert":    { weight: 1, minimum_amount: 1 },
  "hills":     { weight: 3, minimum_amount: 3 },
  "forest":    { weight: 4, minimum_amount: 4 },
  "mountains": { weight: 3, minimum_amount: 3 },
  "fields":    { weight: 4, minimum_amount: 4 },
  "pasture":   { weight: 4, minimum_amount: 4 },
};

const SETTINGS = { map_size: 5 }; // Standard Catan = 5

// ─── Helpers ──────────────────────────────────────────────────────────────────

const OUTER = FIELD_TYPES.find(f => f.name === "outer-bound");

function weightedRandom(types, totalWeight) {
  const r = Math.random() * totalWeight;
  let acc = 0;
  for (const t of types) {
    acc += FIELD_DISTRIBUTION[t.name].weight;
    if (r < acc) return t;
  }
  return types[types.length - 1];
}

// ─── Map Logic (mirrors Python Map.__init__) ──────────────────────────────────

function generateTileDistribution(fieldTypes, count) {
  const fields = [];
  const eligibleTypes = fieldTypes.filter(f => f.name !== "outer-bound");

  // Place minimum amounts
  for (const ft of eligibleTypes) {
    const dist = FIELD_DISTRIBUTION[ft.name];
    for (let i = 0; i < dist.minimum_amount; i++) fields.push(ft);
  }

  const totalWeight = eligibleTypes.reduce((s, f) => s + FIELD_DISTRIBUTION[f.name].weight, 0);

  // Fill remaining slots via weighted random
  while (fields.length < count) {
    fields.push(weightedRandom(eligibleTypes, totalWeight));
  }

  // Shuffle (Fisher-Yates)
  for (let i = fields.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [fields[i], fields[j]] = [fields[j], fields[i]];
  }

  return fields;
}

function generateMap(fieldTypes, settings) {
  const mapSize = settings.map_size;
  // map_size ** 2 - 6 = map_size + 2 * sum(from i=3 to i=map_size-1 : i)
  const tileCount = mapSize ** 2 - 6;
  const mapTiles = generateTileDistribution(fieldTypes, tileCount);

  const innerWidth  = mapSize;
  const innerHeight = 1 + 2 * (mapSize - 3);
  const BORDER      = 4;
  const outerWidth  = innerWidth + BORDER;

  const grid = [];
  let tileIdx = 0;

  // Top border rows
  for (let b = 0; b < BORDER; b++) {
    const row = [];
    for (let c = 0; c < outerWidth; c++) row.push({ type: OUTER, number: null });
    grid.push(row);
  }

  // Middle rows
  for (let i = 0; i < innerHeight; i++) {
    const row = [];
    const seaTiles   = Math.abs(i - Math.floor(innerHeight / 2));
    const leftOuter  = Math.floor(BORDER / 2) + Math.floor(seaTiles / 2);
    const innerCount = innerWidth - seaTiles;
    const rightOuter = Math.floor(BORDER / 2) + Math.floor(seaTiles / 2) + (seaTiles % 2);

    for (let c = 0; c < leftOuter;  c++) row.push({ type: OUTER, number: null });
    for (let c = 0; c < innerCount; c++) row.push({ type: mapTiles[tileIdx++], number: null });
    for (let c = 0; c < rightOuter; c++) row.push({ type: OUTER, number: null });

    grid.push(row);
  }

  // Bottom border rows
  for (let b = 0; b < BORDER; b++) {
    const row = [];
    for (let c = 0; c < outerWidth; c++) row.push({ type: OUTER, number: null });
    grid.push(row);
  }

  // Note: number token assignment is not done here — to be added in a later step.

  return grid;
}

// ─── SVG Hex Renderer ─────────────────────────────────────────────────────────

const HEX_R = 42;
const HEX_W = Math.sqrt(3) * HEX_R;
const HEX_H = 2 * HEX_R;

function hexPoints(cx, cy, r) {
  const pts = [];
  for (let i = 0; i < 6; i++) {
    const angle = Math.PI / 180 * (60 * i - 30); // pointy-top
    pts.push([cx + r * Math.cos(angle), cy + r * Math.sin(angle)]);
  }
  return pts.map(p => p.join(",")).join(" ");
}

function hexCenter(row, col) {
  const x = col * HEX_W + (row % 2 === 1 ? HEX_W / 2 : 0);
  const y = row * HEX_H * 0.75;
  return { x, y };
}

let showNumbers = true;
let showOuter   = true;
let currentGrid = null;

function render(grid) {
  currentGrid = grid;
  const svg = document.getElementById("board-svg");
  svg.innerHTML = "";

  const ns = "http://www.w3.org/2000/svg";

  // Compute bounding box
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
  grid.forEach((row, ri) => {
    row.forEach((_, ci) => {
      const { x, y } = hexCenter(ri, ci);
      if (x - HEX_W / 2 < minX) minX = x - HEX_W / 2;
      if (y - HEX_R     < minY) minY = y - HEX_R;
      if (x + HEX_W / 2 > maxX) maxX = x + HEX_W / 2;
      if (y + HEX_R     > maxY) maxY = y + HEX_R;
    });
  });

  const pad = 12;
  const vw = maxX - minX + pad * 2;
  const vh = maxY - minY + pad * 2;
  svg.setAttribute("viewBox", `${minX - pad} ${minY - pad} ${vw} ${vh}`);
  svg.setAttribute("width",  vw);
  svg.setAttribute("height", vh);

  // Ocean background
  const bgRect = document.createElementNS(ns, "rect");
  bgRect.setAttribute("x",      minX - pad);
  bgRect.setAttribute("y",      minY - pad);
  bgRect.setAttribute("width",  vw);
  bgRect.setAttribute("height", vh);
  bgRect.setAttribute("fill",   "#0f2d4a");
  bgRect.setAttribute("rx",     "12");
  svg.appendChild(bgRect);

  grid.forEach((row, ri) => {
    row.forEach((cell, ci) => {
      const isOuter = cell.type.name === "outer-bound";
      if (isOuter && !showOuter) return;

      const { x, y } = hexCenter(ri, ci);
      const g = document.createElementNS(ns, "g");
      g.setAttribute("class", `hex-cell${isOuter ? " hex-outer" : ""}`);

      // Hex polygon
      const poly = document.createElementNS(ns, "polygon");
      poly.setAttribute("points",       hexPoints(x, y, HEX_R - 1.5));
      poly.setAttribute("fill",         cell.type.color);
      poly.setAttribute("stroke",       isOuter ? "rgba(255,255,255,0.08)" : "rgba(0,0,0,0.4)");
      poly.setAttribute("stroke-width", isOuter ? "0.5" : "1.5");
      g.appendChild(poly);

      if (!isOuter) {
        // Inner highlight
        const innerPoly = document.createElementNS(ns, "polygon");
        innerPoly.setAttribute("points", hexPoints(x, y - 2, HEX_R * 0.55));
        innerPoly.setAttribute("fill",   "rgba(255,255,255,0.07)");
        innerPoly.setAttribute("stroke", "none");
        g.appendChild(innerPoly);

        // Terrain label
        const label = document.createElementNS(ns, "text");
        label.setAttribute("x",                x);
        label.setAttribute("y",                y + (showNumbers && cell.number ? 2 : 5));
        label.setAttribute("text-anchor",      "middle");
        label.setAttribute("dominant-baseline","middle");
        label.setAttribute("font-family",      "Cinzel, serif");
        label.setAttribute("font-size",        cell.type.name === "desert" ? "7" : "6.5");
        label.setAttribute("fill",             cell.type.name === "fields" ? "#4a3800" : "#fff");
        label.setAttribute("opacity",          "0.85");
        label.setAttribute("filter",           "drop-shadow(0 1px 2px rgba(0,0,0,0.6))");
        label.textContent = cell.type.display_name;
        g.appendChild(label);

        // Number token (only if assigned — not yet in this build)
        if (showNumbers && cell.number) {
          const isRed = cell.number === 6 || cell.number === 8;
          const circle = document.createElementNS(ns, "circle");
          circle.setAttribute("cx",           x);
          circle.setAttribute("cy",           y + 14);
          circle.setAttribute("r",            "10");
          circle.setAttribute("fill",         "#f5ead0");
          circle.setAttribute("stroke",       isRed ? "#c0522a" : "#7a6040");
          circle.setAttribute("stroke-width", "1.5");
          g.appendChild(circle);

          const num = document.createElementNS(ns, "text");
          num.setAttribute("x",                x);
          num.setAttribute("y",                y + 14);
          num.setAttribute("text-anchor",      "middle");
          num.setAttribute("dominant-baseline","middle");
          num.setAttribute("font-family",      "Cinzel, serif");
          num.setAttribute("font-size",        "9");
          num.setAttribute("font-weight",      isRed ? "700" : "400");
          num.setAttribute("fill",             isRed ? "#c0522a" : "#1c1008");
          num.textContent = cell.number;
          g.appendChild(num);
        }
      }

      // Tooltip
      g.addEventListener("mousemove", (e) => {
        const tt = document.getElementById("tooltip");
        tt.textContent = isOuter
          ? "Ocean"
          : `${cell.type.display_name}${cell.type.resource ? " · " + cell.type.resource : ""}${cell.number ? " · Roll " + cell.number : ""}`;
        tt.style.left = (e.clientX + 14) + "px";
        tt.style.top  = (e.clientY - 28) + "px";
        tt.classList.add("visible");
      });
      g.addEventListener("mouseleave", () => {
        document.getElementById("tooltip").classList.remove("visible");
      });

      svg.appendChild(g);
    });
  });

  renderLegend();
}

function renderLegend() {
  const legend = document.getElementById("legend");
  legend.innerHTML = "";
  const seen = new Set();

  for (const ft of FIELD_TYPES) {
    if (ft.name === "outer-bound") continue;
    if (seen.has(ft.name)) continue;
    seen.add(ft.name);

    const item    = document.createElement("div");
    item.className = "legend-item";

    const swatch  = document.createElement("div");
    swatch.className = "legend-swatch";
    swatch.style.background = ft.color;

    const label   = document.createElement("span");
    label.textContent = ft.display_name + (ft.resource ? ` (${ft.resource})` : "");

    item.appendChild(swatch);
    item.appendChild(label);
    legend.appendChild(item);
  }
}

// ─── Boot & Controls ──────────────────────────────────────────────────────────

function newGame() {
  const grid = generateMap(FIELD_TYPES, SETTINGS);
  render(grid);
}

document.getElementById("btn-regenerate").addEventListener("click", newGame);

document.getElementById("btn-toggle-numbers").addEventListener("click", () => {
  showNumbers = !showNumbers;
  if (currentGrid) render(currentGrid);
});

document.getElementById("btn-toggle-outer").addEventListener("click", () => {
  showOuter = !showOuter;
  if (currentGrid) render(currentGrid);
});

newGame();
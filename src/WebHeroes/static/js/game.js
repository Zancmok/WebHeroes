(function () {
  //Colour & label config
  const FIELD_STYLES = {
    "forest":      { fill: "#2d5a1b", label: "Forest",    resource: "Lumber" },
    "hill":        { fill: "#8b3a0f", label: "Hills",     resource: "Brick"  },
    "pasture":     { fill: "#7ec850", label: "Pasture",   resource: "Wool"   },
    "field":       { fill: "#d4b84a", label: "Fields",    resource: "Grain"  },
    "mountain":    { fill: "#6b6b6b", label: "Mountains", resource: "Ore"    },
    "desert":      { fill: "#c9b07a", label: "Desert",    resource: null     },
    "outer-bound": { fill: "#1a3a5c", label: "Ocean",     resource: null     },
    "outer_bound": { fill: "#1a3a5c", label: "Ocean",     resource: null     },
  };

  const IMG_BASE = "/game-management/img/";

  const NUMBER_COLORS = { 6: "#e05c2e", 8: "#e05c2e" };
  const HEX_SIZE = 48;

  // Pointy-top hex math
  function hexToPixel(q, r) {
    const x = HEX_SIZE * (Math.sqrt(3) * q + Math.sqrt(3) / 2 * r);
    const y = HEX_SIZE * (3 / 2 * r);
    return { x, y };
  }

  function hexCornerPoints(cx, cy, size) {
    const pts = [];
    for (let i = 0; i < 6; i++) {
      const angle = (Math.PI / 180) * (60 * i + 30); // pointy-top
      pts.push([cx + size * Math.cos(angle), cy + size * Math.sin(angle)]);
    }
    return pts;
  }

  function pointsAttr(pts) {
    return pts.map(([x, y]) => `${x},${y}`).join(" ");
  }

  function svgEl(tag, attrs = {}) {
    const el = document.createElementNS("http://www.w3.org/2000/svg", tag);
    for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, v);
    return el;
  }

  function resolveSprite(field) {
    if (field.sprite) {
      return field.sprite
        .replace(/^__|__(?=\/)/g, "")
        .replace("graphics/", "images/");
    }
    return null;
  }
  const svg     = document.getElementById("board-svg");
  const tooltip = document.getElementById("tooltip");
  const legend  = document.getElementById("legend");

  let showNumbers = true;
  let showOuter   = true;
  let lastData    = null;

  function render(data) {
    console.log("[game.js] render() called with:", data);
    lastData = data;
    svg.innerHTML = "";

    if (!data || !data.map || !data.map.fields) {
      console.warn("[game.js] No map/fields in data:", data);
      svg.setAttribute("viewBox", "0 0 400 400");
      return;
    }

    const fields = data.map.fields;
    const keys   = Object.keys(fields);
    console.log(`[game.js] ${keys.length} fields. First 3:`, keys.slice(0, 3).map(k => JSON.stringify(k)));

    const parsed = [];
    for (const [key, field] of Object.entries(fields)) {
      const cleanKey = key.replace(/^"|"$/g, "");
      let parts = cleanKey.split("\u0000");
      if (parts.length !== 2) parts = cleanKey.split("\x00");
      if (parts.length !== 2) {
        console.warn("[game.js] Unexpected key format:", JSON.stringify(key));
        continue;
      }
      const q = Number(parts[0]);
      const r = Number(parts[1]);
      if (isNaN(q) || isNaN(r)) {
        console.warn("[game.js] NaN coords:", JSON.stringify(key));
        continue;
      }
      const { x, y } = hexToPixel(q, r);
      parsed.push({ q, r, x, y, field });
    }

    console.log(`[game.js] ${parsed.length} hexes parsed.`);
    if (parsed.length === 0) return;

    // Bounding box
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    for (const { x, y } of parsed) {
      minX = Math.min(minX, x - HEX_SIZE);
      minY = Math.min(minY, y - HEX_SIZE);
      maxX = Math.max(maxX, x + HEX_SIZE);
      maxY = Math.max(maxY, y + HEX_SIZE);
    }
    const pad = 12;
    const vb  = `${minX - pad} ${minY - pad} ${maxX - minX + pad * 2} ${maxY - minY + pad * 2}`;
    svg.setAttribute("viewBox", vb);
    svg.setAttribute("width",  maxX - minX + pad * 2);
    svg.setAttribute("height", maxY - minY + pad * 2);

    // Outer behind inner
    parsed.sort((a, b) =>
      (a.field.field_type === "outer-bound" || a.field.field_type === "outer_bound" ? 0 : 1) -
      (b.field.field_type === "outer-bound" || b.field.field_type === "outer_bound" ? 0 : 1)
    );

    //Defs
    const defs = svgEl("defs");

    // Drop shadow filter
    const filt = svgEl("filter", { id: "hex-shadow", x: "-20%", y: "-20%", width: "140%", height: "140%" });
    filt.appendChild(svgEl("feDropShadow", { dx: "0", dy: "3", stdDeviation: "4", "flood-color": "rgba(0,0,0,0.5)" }));
    defs.appendChild(filt);

    // One clipPath per hex so images are masked to the hex shape
    for (const { x, y, q, r } of parsed) {
      const cp = svgEl("clipPath", { id: `clip-${q}-${r}` });
      cp.appendChild(svgEl("polygon", {
        points: pointsAttr(hexCornerPoints(x, y, HEX_SIZE - 1.5)),
      }));
      defs.appendChild(cp);
    }

    svg.appendChild(defs);

    const seen = new Set();

    for (const { x, y, q, r, field } of parsed) {
      const normType = (field.field_type || "").replace("_", "-");
      const isOuter  = normType === "outer-bound";
      if (isOuter && !showOuter) continue;

      // Look up style using both hyphen and underscore variants
      const style  = FIELD_STYLES[field.field_type] || FIELD_STYLES[normType] || { fill: "#888", label: field.field_type };
      const pts    = hexCornerPoints(x, y, HEX_SIZE - 1.5);
      const pAttr  = pointsAttr(pts);
      const clipId = `clip-${q}-${r}`;
      const sprite = resolveSprite(field);
      const g      = svgEl("g", { class: isOuter ? "hex-cell hex-outer" : "hex-cell" });

      // Layer 1: solid colour base (visible while image loads or if img missing)
      g.appendChild(svgEl("polygon", { points: pAttr, fill: style.fill, stroke: "none" }));

      // Layer 2: image clipped to hex shape — driven by field.sprite from backend,
      // with a client-side fallback for sea tiles. Applies to ALL hexes incl. outer.
      if (sprite) {
        const imgSize = HEX_SIZE * 2.05;
        g.appendChild(svgEl("image", {
          href:                `${IMG_BASE}${sprite}`,
          x:                   x - imgSize / 2,
          y:                   y - imgSize / 2,
          width:               imgSize,
          height:              imgSize,
          preserveAspectRatio: "xMidYMid slice",
          "clip-path":         `url(#${clipId})`,
        }));
      }

      // Layer 3: border stroke (+ drop shadow on inner hexes)
      g.appendChild(svgEl("polygon", {
        points:         pAttr,
        fill:           "none",
        stroke:         isOuter ? "rgba(255,255,255,0.06)" : "rgba(0,0,0,0.45)",
        "stroke-width": isOuter ? "1" : "1.5",
        filter:         isOuter ? "" : "url(#hex-shadow)",
      }));

      if (!isOuter) {
        // Subtle inner ring
        g.appendChild(svgEl("polygon", {
          points: pointsAttr(hexCornerPoints(x, y, HEX_SIZE * 0.78)),
          fill: "none", stroke: "rgba(255,255,255,0.12)", "stroke-width": "1",
        }));

        // Layer 4: number token
        if (showNumbers && field.assigned_number != null) {
          const numColor = NUMBER_COLORS[field.assigned_number] || "#f5ead0";
          g.appendChild(svgEl("circle", {
            cx: x, cy: y, r: 16,
            fill: "rgba(245,234,208,0.93)",
            stroke: "rgba(0,0,0,0.35)", "stroke-width": "1.5",
          }));
          const txt = svgEl("text", {
            x, y, "text-anchor": "middle", "dominant-baseline": "central",
            fill: numColor, "font-size": "14",
            "font-family": "Cinzel, serif", "font-weight": "bold",
          });
          txt.textContent = field.assigned_number;
          g.appendChild(txt);
        } else if (!sprite) {
          // Fallback label when there's no image and no number
          const lbl = svgEl("text", {
            x, y, "text-anchor": "middle", "dominant-baseline": "central",
            fill: "rgba(255,255,255,0.55)", "font-size": "9",
            "font-family": "Crimson Pro, serif", "letter-spacing": "0.05em",
          });
          lbl.textContent = (style.label || field.field_type).toUpperCase();
          g.appendChild(lbl);
        }

        // Tooltip
        g.addEventListener("mousemove", (e) => {
          const lines = [`Type: ${style.label || field.field_type}`];
          if (style.resource)        lines.push(`Resource: ${style.resource}`);
          if (field.assigned_number) lines.push(`Number: ${field.assigned_number}`);
          tooltip.textContent = lines.join("  ·  ");
          tooltip.classList.add("visible");
          tooltip.style.left = (e.clientX + 14) + "px";
          tooltip.style.top  = (e.clientY - 28) + "px";
        });
        g.addEventListener("mouseleave", () => tooltip.classList.remove("visible"));
        if (!seen.has(field.field_type)) seen.add(field.field_type);
      }

      svg.appendChild(g);
    }

    // Legend — swatches show the actual image thumbnail
    legend.innerHTML = "";
    for (const ft of seen) {
      const style  = FIELD_STYLES[ft] || { fill: "#888", label: ft };
      const item   = document.createElement("div");
      item.className = "legend-item";
      const swatch = document.createElement("div");
      swatch.className = "legend-swatch";
      // Find a parsed hex of this type to get its sprite
      const sample = parsed.find(p => p.field.field_type === ft);
      const sampleSprite = sample ? resolveSprite(sample.field) : null;
      if (sampleSprite) {
        swatch.style.backgroundImage    = `url(${IMG_BASE}${sampleSprite})`;
        swatch.style.backgroundSize     = "cover";
        swatch.style.backgroundPosition = "center";
      } else {
        swatch.style.background = style.fill;
      }
      const lbl = document.createElement("span");
      lbl.textContent = style.label || ft;
      item.appendChild(swatch);
      item.appendChild(lbl);
      legend.appendChild(item);
    }

    console.log("[game.js] Render complete.");
  }

  //Socket.IO
  const socket = io();

  socket.on("connect", () => {
    console.log("[game.js] Socket connected, sid:", socket.id);
    const lobbyName = (sessionStorage.getItem("currentLobbyName") || "").trim();
    if (lobbyName) {
      console.log("[game.js] Re-joining lobby:", lobbyName);
      socket.emit("lobby-management:join-lobby", { lobby_name: lobbyName });
    } else {
      console.warn("[game.js] No lobbyName in sessionStorage.");
    }
    socket.emit("game-management:get-game-data");
    console.log("[game.js] Emitted game-management:get-game-data");
  });

  socket.on("connect_error", (err) => console.error("[game.js] Socket connect error:", err));

  socket.on("game-management:get-game-data", (data) => {
    console.log("[game.js] Received game data:", data);
    render(data);
  });

  const _onevent = socket.onevent.bind(socket);
  socket.onevent = function (packet) {
    console.log("[game.js] RAW socket event:", packet.data);
    _onevent(packet);
  };

  //Controls
  document.getElementById("btn-toggle-numbers").addEventListener("click", () => {
    showNumbers = !showNumbers;
    if (lastData) render(lastData);
  });
  document.getElementById("btn-toggle-outer").addEventListener("click", () => {
    showOuter = !showOuter;
    if (lastData) render(lastData);
  });
})();
(function () {
  // ─── Colour & label config ───────────────────────────────────────────────────
  const FIELD_STYLES = {
    "forest":     { fill: "#2d5a1b", label: "Forest",    resource: "Lumber" },
    "hill":       { fill: "#8b3a0f", label: "Hills",     resource: "Brick"  },
    "pasture":    { fill: "#7ec850", label: "Pasture",   resource: "Wool"   },
    "field":      { fill: "#d4b84a", label: "Fields",    resource: "Grain"  },
    "mountain":   { fill: "#6b6b6b", label: "Mountains", resource: "Ore"    },
    "desert":     { fill: "#c9b07a", label: "Desert",    resource: null     },
    "outer-bound":{ fill: "#1a3a5c", label: "Ocean",     resource: null     },
  };

  const NUMBER_COLORS = { 6: "#e05c2e", 8: "#e05c2e" };
  const HEX_SIZE = 48;

  // Pointy-top hex math — matches Python odd-r offset -> axial
  function hexToPixel(q, r) {
    const x = HEX_SIZE * (Math.sqrt(3) * q + Math.sqrt(3) / 2 * r);
    const y = HEX_SIZE * (3 / 2 * r);
    return { x, y };
  }

  function hexCorners(cx, cy, size) {
    const pts = [];
    for (let i = 0; i < 6; i++) {
      const angle = (Math.PI / 180) * (60 * i + 30); // +30 = pointy-top
      pts.push([cx + size * Math.cos(angle), cy + size * Math.sin(angle)]);
    }
    return pts.map(([x, y]) => `${x},${y}`).join(" ");
  }

  function svgEl(tag, attrs = {}) {
    const el = document.createElementNS("http://www.w3.org/2000/svg", tag);
    for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, v);
    return el;
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
    console.log(`[game.js] ${keys.length} fields. First 3 keys (JSON):`, keys.slice(0,3).map(k => JSON.stringify(k)));

    const parsed = [];
    for (const [key, field] of Object.entries(fields)) {
      // Keys arrive double-serialized with surrounding quotes: '"0\u00000"'
      // Strip the extra quotes first, then split on the null byte
      const cleanKey = key.replace(/^"|"$/g, "");
      let parts = cleanKey.split("\u0000");
      if (parts.length !== 2) parts = cleanKey.split("\x00");
      if (parts.length !== 2) {
        console.warn("[game.js] Unexpected key format:", JSON.stringify(key), "cleaned:", JSON.stringify(cleanKey));
        continue;
      }
      const q = Number(parts[0]);
      const r = Number(parts[1]);
      if (isNaN(q) || isNaN(r)) {
        console.warn("[game.js] NaN coords for key:", JSON.stringify(key), "->", parts);
        continue;
      }
      const { x, y } = hexToPixel(q, r);
      parsed.push({ q, r, x, y, field });
    }

    console.log(`[game.js] ${parsed.length} hexes parsed.`);
    if (parsed.length === 0) {
      console.error("[game.js] 0 hexes — nothing to render. Check key format above.");
      return;
    }

    // Bounding box
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    for (const { x, y } of parsed) {
      minX = Math.min(minX, x - HEX_SIZE);
      minY = Math.min(minY, y - HEX_SIZE);
      maxX = Math.max(maxX, x + HEX_SIZE);
      maxY = Math.max(maxY, y + HEX_SIZE);
    }
    const pad = 12;
    const vbW = maxX - minX + pad * 2;
    const vbH = maxY - minY + pad * 2;
    const vb  = `${minX - pad} ${minY - pad} ${vbW} ${vbH}`;
    console.log("[game.js] viewBox:", vb);
    svg.setAttribute("viewBox", vb);
    svg.setAttribute("width",  vbW);
    svg.setAttribute("height", vbH);

    // Outer behind inner
    parsed.sort((a, b) => (a.field.field_type === "outer-bound" ? 0 : 1) - (b.field.field_type === "outer-bound" ? 0 : 1));

    // Defs
    const defs = svgEl("defs");
    const filt = svgEl("filter", { id: "hex-shadow", x: "-20%", y: "-20%", width: "140%", height: "140%" });
    const drop = svgEl("feDropShadow", { dx: "0", dy: "3", stdDeviation: "4", "flood-color": "rgba(0,0,0,0.5)" });
    filt.appendChild(drop);
    defs.appendChild(filt);
    svg.appendChild(defs);

    const seen = new Set();

    for (const { x, y, field } of parsed) {
      const isOuter = field.field_type === "outer-bound";
      if (isOuter && !showOuter) continue;

      const style   = FIELD_STYLES[field.field_type] || { fill: "#888", label: field.field_type };
      const corners = hexCorners(x, y, HEX_SIZE - 1.5);
      const g       = svgEl("g", { class: isOuter ? "hex-cell hex-outer" : "hex-cell" });

      const poly = svgEl("polygon", {
        points: corners,
        fill:   style.fill,
        stroke: isOuter ? "rgba(255,255,255,0.06)" : "rgba(0,0,0,0.4)",
        "stroke-width": isOuter ? "1" : "1.5",
        filter: isOuter ? "" : "url(#hex-shadow)",
      });
      g.appendChild(poly);

      if (!isOuter) {
        const inner = svgEl("polygon", {
          points: hexCorners(x, y, HEX_SIZE * 0.78),
          fill: "none", stroke: "rgba(255,255,255,0.12)", "stroke-width": "1",
        });
        g.appendChild(inner);

        if (showNumbers && field.assigned_number != null) {
          const numColor = NUMBER_COLORS[field.assigned_number] || "#f5ead0";
          const circ = svgEl("circle", { cx: x, cy: y, r: 16, fill: "#f5ead0", stroke: "rgba(0,0,0,0.35)", "stroke-width": "1.5" });
          const txt  = svgEl("text", {
            x, y, "text-anchor": "middle", "dominant-baseline": "central",
            fill: numColor, "font-size": "14", "font-family": "Cinzel, serif", "font-weight": "bold",
          });
          txt.textContent = field.assigned_number;
          g.appendChild(circ);
          g.appendChild(txt);
        } else {
          const lbl = svgEl("text", {
            x, y, "text-anchor": "middle", "dominant-baseline": "central",
            fill: "rgba(255,255,255,0.55)", "font-size": "9",
            "font-family": "Crimson Pro, serif", "letter-spacing": "0.05em",
          });
          lbl.textContent = (style.label || field.field_type).toUpperCase();
          g.appendChild(lbl);
        }

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

    // Legend
    legend.innerHTML = "";
    for (const ft of seen) {
      const style  = FIELD_STYLES[ft] || { fill: "#888", label: ft };
      const item   = document.createElement("div");
      item.className = "legend-item";
      const swatch = document.createElement("div");
      swatch.className = "legend-swatch";
      swatch.style.background = style.fill;
      const lbl = document.createElement("span");
      lbl.textContent = style.label || ft;
      item.appendChild(swatch);
      item.appendChild(lbl);
      legend.appendChild(item);
    }
    console.log("[game.js] Render complete.");
  }

  // ─── Socket.IO ───────────────────────────────────────────────────────────────
  const socket = io();

  socket.on("connect", () => {
    console.log("[game.js] Socket connected, sid:", socket.id);

    // Re-join the lobby so the server session knows which game to serve
    const lobbyName = (sessionStorage.getItem("currentLobbyName") || "").trim();
    if (lobbyName) {
      console.log("[game.js] Re-joining lobby:", lobbyName);
      socket.emit("lobby-management:join-lobby", { lobby_name: lobbyName });
    } else {
      console.warn("[game.js] No lobbyName in sessionStorage — server may not find the game.");
    }

    socket.emit("game-management:get-game-data");
    console.log("[game.js] Emitted game-management:get-game-data");
  });

  socket.on("connect_error", (err) => {
    console.error("[game.js] Socket connect error:", err);
  });

  socket.on("game-management:get-game-data", (data) => {
    console.log("[game.js] Received game-management:get-game-data:", data);
    render(data);
  });

  // Log ALL socket events for debugging
  const _onevent = socket.onevent.bind(socket);
  socket.onevent = function(packet) {
    console.log("[game.js] RAW socket event:", packet.data);
    _onevent(packet);
  };

  // ─── Controls ────────────────────────────────────────────────────────────────

  document.getElementById("btn-toggle-numbers").addEventListener("click", () => {
    showNumbers = !showNumbers;
    if (lastData) render(lastData);
  });
  document.getElementById("btn-toggle-outer").addEventListener("click", () => {
    showOuter = !showOuter;
    if (lastData) render(lastData);
  });
})();
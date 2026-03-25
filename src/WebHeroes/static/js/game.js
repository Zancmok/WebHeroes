(function () {
  // ─── Field style config ────────────────────────────────────────────────────
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

  const IMG_BASE      = "/game-management/img/";
  const NUMBER_COLORS = { 6: "#e05c2e", 8: "#e05c2e" };
  const HEX_SIZE      = 48;

  // ─── Hex math ──────────────────────────────────────────────────────────────
  function hexToPixel(q, r) {
    return {
      x: HEX_SIZE * (Math.sqrt(3) * q + Math.sqrt(3) / 2 * r),
      y: HEX_SIZE * (3 / 2 * r),
    };
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
    return resolveRawSprite(field.field_type?.sprite);
  }

  function resolveRawSprite(sprite) {
    if (!sprite) return null;
    return sprite
      .replace(/^__|__(?=\/)/g, "")
      .replace("graphics/", "images/");
  }

  // ─── Geometry helpers ──────────────────────────────────────────────────────

  // Given two hex coords, return the midpoint between their pixel centres —
  // used as the visual midpoint of a road edge.
  function edgeMidpoint(q1, r1, q2, r2) {
    const a = hexToPixel(q1, r1);
    const b = hexToPixel(q2, r2);
    return { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 };
  }

  // The two pixel corners that are shared between hex A and hex B.
  // Each hex has 6 corners; two adjacent hexes share exactly 2 of them.
  function sharedEdgeCorners(q1, r1, q2, r2) {
    const ca = hexCornerPoints(...Object.values(hexToPixel(q1, r1)), HEX_SIZE - 1.5);
    const cb = hexCornerPoints(...Object.values(hexToPixel(q2, r2)), HEX_SIZE - 1.5);

    const EPS = 2; // pixel tolerance for "same point"
    const shared = [];
    for (const pa of ca) {
      for (const pb of cb) {
        const dx = pa[0] - pb[0], dy = pa[1] - pb[1];
        if (Math.sqrt(dx * dx + dy * dy) < EPS) {
          shared.push([(pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2]);
        }
      }
    }
    return shared; // usually 2 points
  }

  // The pixel point that is the shared corner of three hexes.
  // Average of their three centres' nearest matching corners.
  function intersectionPoint(q1, r1, q2, r2, q3, r3) {
    const centres = [[q1, r1], [q2, r2], [q3, r3]].map(([q, r]) => hexToPixel(q, r));
    return {
      x: (centres[0].x + centres[1].x + centres[2].x) / 3,
      y: (centres[0].y + centres[1].y + centres[2].y) / 3,
    };
  }

  // ─── Player colour helper ─────────────────────────────────────────────────
  function playerCSSColor(player) {
    const c = player?.color_type;
    if (!c) return "#ffffff";
    return `rgb(${c.r},${c.g},${c.b})`;
  }

  // ─── State ─────────────────────────────────────────────────────────────────
  const svg     = document.getElementById("board-svg");
  const tooltip = document.getElementById("tooltip");
  const legend  = document.getElementById("legend");

  let showNumbers   = true;
  let showOuter     = true;
  let lastData      = null;
  let hexPixelMap   = new Map(); // "q,r" → {x, y}

  // Placed buildings: stored client-side so we can redraw without a full
  // round-trip.  Each entry: { type: "road"|"settlement", location: [...ints],
  //                            building: {...}, player: {...} }
  const placedBuildings = [];

  // ─── Placement-mode state ──────────────────────────────────────────────────
  // When the player clicks a recipe button we enter placement mode.
  // placementMode: null | { recipeId, resultType: "road"|"settlement" }
  let placementMode = null;

  // ─── Render ────────────────────────────────────────────────────────────────
  function render(data) {
    console.log("[game.js] render() called");
    lastData = data;
    hexPixelMap.clear();
    svg.innerHTML = "";

    if (!data?.fields) {
      svg.setAttribute("viewBox", "0 0 400 400");
      return;
    }

    // Parse fields
    const parsed = [];
    for (const [key, field] of Object.entries(data.fields)) {
      const cleanKey = key.replace(/^"|"$/g, "");
      let parts = cleanKey.split("\u0000");
      if (parts.length !== 2) parts = cleanKey.split("\x00");
      if (parts.length !== 2) continue;
      const q = Number(parts[0]), r = Number(parts[1]);
      if (isNaN(q) || isNaN(r)) continue;
      const { x, y } = hexToPixel(q, r);
      parsed.push({ q, r, x, y, field });
      hexPixelMap.set(`${q},${r}`, { x, y });
    }

    if (parsed.length === 0) return;

    // View-box
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    for (const { x, y } of parsed) {
      minX = Math.min(minX, x - HEX_SIZE);
      minY = Math.min(minY, y - HEX_SIZE);
      maxX = Math.max(maxX, x + HEX_SIZE);
      maxY = Math.max(maxY, y + HEX_SIZE);
    }
    const pad = 12;
    svg.setAttribute("viewBox", `${minX - pad} ${minY - pad} ${maxX - minX + pad * 2} ${maxY - minY + pad * 2}`);
    svg.setAttribute("width",  maxX - minX + pad * 2);
    svg.setAttribute("height", maxY - minY + pad * 2);

    // Draw outer tiles first
    parsed.sort((a, b) => {
      const aO = a.field.field_type?.name?.includes("outer") ? 0 : 1;
      const bO = b.field.field_type?.name?.includes("outer") ? 0 : 1;
      return aO - bO;
    });

    // Defs
    const defs = svgEl("defs");
    const filt = svgEl("filter", { id: "hex-shadow", x: "-20%", y: "-20%", width: "140%", height: "140%" });
    filt.appendChild(svgEl("feDropShadow", { dx: "0", dy: "3", stdDeviation: "4", "flood-color": "rgba(0,0,0,0.5)" }));
    defs.appendChild(filt);
    for (const { x, y, q, r } of parsed) {
      const cp = svgEl("clipPath", { id: `clip-${q}-${r}` });
      cp.appendChild(svgEl("polygon", { points: pointsAttr(hexCornerPoints(x, y, HEX_SIZE - 1.5)) }));
      defs.appendChild(cp);
    }
    svg.appendChild(defs);

    // Hex tiles
    const seen = new Set();
    for (const { x, y, q, r, field } of parsed) {
      const typeName = field.field_type?.name || "";
      const normType = typeName.replace("_", "-");
      const isOuter  = normType === "outer-bound";
      if (isOuter && !showOuter) continue;

      const style  = FIELD_STYLES[typeName] || FIELD_STYLES[normType] || { fill: "#888", label: field.field_type?.display_name || typeName };
      const pts    = hexCornerPoints(x, y, HEX_SIZE - 1.5);
      const pAttr  = pointsAttr(pts);
      const sprite = resolveSprite(field);
      const g      = svgEl("g", { class: isOuter ? "hex-cell hex-outer" : "hex-cell" });

      g.appendChild(svgEl("polygon", { points: pAttr, fill: style.fill, stroke: "none" }));

      if (sprite) {
        const imgSize = HEX_SIZE * 2.05;
        g.appendChild(svgEl("image", {
          href: `${IMG_BASE}${sprite}`,
          x: x - imgSize / 2, y: y - imgSize / 2,
          width: imgSize, height: imgSize,
          preserveAspectRatio: "xMidYMid slice",
          "clip-path": `url(#clip-${q}-${r})`,
        }));
      }

      g.appendChild(svgEl("polygon", {
        points: pAttr, fill: "none",
        stroke: isOuter ? "rgba(255,255,255,0.06)" : "rgba(0,0,0,0.45)",
        "stroke-width": isOuter ? "1" : "1.5",
        filter: isOuter ? "" : "url(#hex-shadow)",
      }));

      if (!isOuter) {
        g.appendChild(svgEl("polygon", {
          points: pointsAttr(hexCornerPoints(x, y, HEX_SIZE * 0.78)),
          fill: "none", stroke: "rgba(255,255,255,0.12)", "stroke-width": "1",
        }));

        if (showNumbers && field.assigned_number != null) {
          const numColor = NUMBER_COLORS[field.assigned_number] || "#000000";
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
          const lbl = svgEl("text", {
            x, y, "text-anchor": "middle", "dominant-baseline": "central",
            fill: "rgba(255,255,255,0.55)", "font-size": "9",
            "font-family": "Crimson Pro, serif", "letter-spacing": "0.05em",
          });
          lbl.textContent = (style.label || field.field_type?.display_name || typeName).toUpperCase();
          g.appendChild(lbl);
        }

        g.addEventListener("mousemove", (e) => {
          const displayName = field.field_type?.display_name || style.label || typeName;
          const resource    = field.field_type?.resource?.display_name || style.resource;
          const lines = [`Type: ${displayName}`];
          if (resource)              lines.push(`Resource: ${resource}`);
          if (field.assigned_number) lines.push(`Number: ${field.assigned_number}`);
          tooltip.textContent = lines.join("  ·  ");
          tooltip.classList.add("visible");
          tooltip.style.left = (e.clientX + 14) + "px";
          tooltip.style.top  = (e.clientY - 28) + "px";
        });
        g.addEventListener("mouseleave", () => tooltip.classList.remove("visible"));
        if (!seen.has(typeName)) seen.add(typeName);
      }

      svg.appendChild(g);
    }

    // Draw all buildings placed so far
    for (const b of placedBuildings) {
      drawBuilding(b);
    }

    // Draw placement hit-targets if in placement mode
    if (placementMode) {
      drawPlacementTargets(parsed);
    }

    // Legend
    legend.innerHTML = "";
    for (const ft of seen) {
      const style  = FIELD_STYLES[ft] || { fill: "#888", label: ft };
      const item   = document.createElement("div");
      item.className = "legend-item";
      const swatch = document.createElement("div");
      swatch.className = "legend-swatch";
      const sample = parsed.find(p => p.field.field_type?.name === ft);
      const sampleSprite = sample ? resolveSprite(sample.field) : null;
      if (sampleSprite) {
        swatch.style.backgroundImage    = `url(${IMG_BASE}${sampleSprite})`;
        swatch.style.backgroundSize     = "cover";
        swatch.style.backgroundPosition = "center";
      } else {
        swatch.style.background = style.fill;
      }
      const lbl = document.createElement("span");
      lbl.textContent = sample?.field.field_type?.display_name || style.label || ft;
      item.appendChild(swatch);
      item.appendChild(lbl);
      legend.appendChild(item);
    }
  }

  // ─── Draw a single placed building / road ──────────────────────────────────
  function drawBuilding({ type, location, building, player }) {
    const color = playerCSSColor(player);

    if (type === "road") {
      // location = [q1,r1, q2,r2]
      const [q1, r1, q2, r2] = location;
      const corners = sharedEdgeCorners(q1, r1, q2, r2);

      if (corners.length < 2) {
        // Fallback: draw from centre to centre
        const a = hexToPixel(q1, r1), b = hexToPixel(q2, r2);
        corners.push([a.x, a.y], [b.x, b.y]);
      }

      const line = svgEl("line", {
        x1: corners[0][0], y1: corners[0][1],
        x2: corners[1][0], y2: corners[1][1],
        stroke: color,
        "stroke-width": "5",
        "stroke-linecap": "round",
        "pointer-events": "none",
      });
      // Thin dark outline for legibility
      const outline = svgEl("line", {
        x1: corners[0][0], y1: corners[0][1],
        x2: corners[1][0], y2: corners[1][1],
        stroke: "rgba(0,0,0,0.55)",
        "stroke-width": "7",
        "stroke-linecap": "round",
        "pointer-events": "none",
      });
      svg.appendChild(outline);
      svg.appendChild(line);

    } else if (type === "settlement") {
      // location = [q1,r1, q2,r2, q3,r3]
      const [q1, r1, q2, r2, q3, r3] = location;
      const { x, y } = intersectionPoint(q1, r1, q2, r2, q3, r3);

      const SIZE = building?.point_value > 1 ? 36 : 28; // city larger than village
      const sprite = resolveRawSprite(building?.sprite);

      if (sprite) {
        // Dark outline ring for contrast, then player colour ring on top
        svg.appendChild(svgEl("circle", {
          cx: x, cy: y, r: SIZE + 4,
          fill: "none",
          stroke: "rgba(0,0,0,0.7)", "stroke-width": "5",
          "pointer-events": "none",
        }));
        svg.appendChild(svgEl("circle", {
          cx: x, cy: y, r: SIZE + 4,
          fill: "none",
          stroke: color, "stroke-width": "3",
          "pointer-events": "none",
        }));
        svg.appendChild(svgEl("image", {
          href: `${IMG_BASE}${sprite}`,
          x: x - SIZE, y: y - SIZE,
          width: SIZE * 2, height: SIZE * 2,
          preserveAspectRatio: "xMidYMid meet",
          "pointer-events": "none",
        }));
      } else {
        // Fallback: plain coloured circle with letter
        const RADIUS = building?.point_value > 1 ? 10 : 7;
        svg.appendChild(svgEl("circle", {
          cx: x, cy: y + 2, r: RADIUS + 1,
          fill: "rgba(0,0,0,0.45)", "pointer-events": "none",
        }));
        svg.appendChild(svgEl("circle", {
          cx: x, cy: y, r: RADIUS,
          fill: color,
          stroke: "rgba(0,0,0,0.7)", "stroke-width": "1.5",
          "pointer-events": "none",
        }));
        const initial = svgEl("text", {
          x, y, "text-anchor": "middle", "dominant-baseline": "central",
          fill: "rgba(0,0,0,0.75)",
          "font-size": RADIUS > 8 ? "9" : "7",
          "font-family": "Cinzel, serif", "font-weight": "bold",
          "pointer-events": "none",
        });
        initial.textContent = building?.point_value > 1 ? "C" : "S";
        svg.appendChild(initial);
      }
    }
  }

  // ─── Placement-mode hit targets ────────────────────────────────────────────
  // We draw invisible clickable shapes over every valid edge (road) or corner
  // (settlement).  The backend enforces legality; we just need the player to
  // pick a spot.

  function drawPlacementTargets(parsed) {
    const { resultType } = placementMode;

    if (resultType === "road") {
      // Build a set of unique inner-hex edges
      const drawn = new Set();
      for (const { q, r, field } of parsed) {
        if (field.field_type?.name?.includes("outer")) continue;
        const neighbours = [
          [q+1, r], [q+1, r-1], [q, r-1],
          [q-1, r], [q-1, r+1], [q, r+1],
        ];
        for (const [nq, nr] of neighbours) {
          if (!hexPixelMap.has(`${nq},${nr}`)) continue;
          const nField = lastData?.fields[`${nq}\0${nr}`] || lastData?.fields[Object.keys(lastData.fields).find(k => {
            const parts = k.split("\u0000");
            return Number(parts[0]) === nq && Number(parts[1]) === nr;
          })];
          if (nField?.field_type?.name?.includes("outer")) continue;

          const edgeKey = [q, r, nq, nr].sort().join(",");
          if (drawn.has(edgeKey)) continue;
          drawn.add(edgeKey);

          const corners = sharedEdgeCorners(q, r, nq, nr);
          if (corners.length < 2) continue;

          const hit = svgEl("line", {
            x1: corners[0][0], y1: corners[0][1],
            x2: corners[1][0], y2: corners[1][1],
            stroke: "rgba(255,255,100,0.35)",
            "stroke-width": "10",
            "stroke-linecap": "round",
            cursor: "pointer",
            class: "placement-target",
          });
          hit.addEventListener("mouseenter", () => hit.setAttribute("stroke", "rgba(255,255,100,0.75)"));
          hit.addEventListener("mouseleave", () => hit.setAttribute("stroke", "rgba(255,255,100,0.35)"));
          hit.addEventListener("click", () => {
            emitBuild(placementMode.recipeId, [q, r, nq, nr]);
          });
          svg.appendChild(hit);
        }
      }

    } else if (resultType === "settlement") {
      // Build a set of unique inner-hex corners (each corner = 3 hexes)
      const drawn = new Set();
      const directions = [
        [+1, 0], [+1, -1], [0, -1],
        [-1, 0], [-1, +1], [0, +1],
      ];
      for (const { q, r, field } of parsed) {
        if (field.field_type?.name?.includes("outer")) continue;
        for (let i = 0; i < 6; i++) {
          const [dq1, dr1] = directions[i];
          const [dq2, dr2] = directions[(i + 1) % 6];
          const n1q = q + dq1, n1r = r + dr1;
          const n2q = q + dq2, n2r = r + dr2;
          if (!hexPixelMap.has(`${n1q},${n1r}`) || !hexPixelMap.has(`${n2q},${n2r}`)) continue;

          const coords = [[q, r], [n1q, n1r], [n2q, n2r]].sort((a, b) => a[0] - b[0] || a[1] - b[1]);
          const key = coords.map(c => c.join(",")).join("|");
          if (drawn.has(key)) continue;
          drawn.add(key);

          const [[a0, a1], [b0, b1], [c0, c1]] = coords;
          const { x, y } = intersectionPoint(a0, a1, b0, b1, c0, c1);

          const hit = svgEl("circle", {
            cx: x, cy: y, r: 9,
            fill: "rgba(255,255,100,0.35)",
            stroke: "rgba(255,255,100,0.7)", "stroke-width": "1.5",
            cursor: "pointer",
            class: "placement-target",
          });
          hit.addEventListener("mouseenter", () => hit.setAttribute("fill", "rgba(255,255,100,0.75)"));
          hit.addEventListener("mouseleave", () => hit.setAttribute("fill", "rgba(255,255,100,0.35)"));
          hit.addEventListener("click", () => {
            emitBuild(placementMode.recipeId, [a0, a1, b0, b1, c0, c1]);
          });
          svg.appendChild(hit);
        }
      }
    }
  }

  // ─── Emit build + leave placement mode ─────────────────────────────────────
  function emitBuild(recipeId, location) {
    console.log("[game.js] Emitting build:", recipeId, location);
    socket.emit("game-management:build", { recipe_id: recipeId, location });
    exitPlacementMode();
  }

  function enterPlacementMode(recipeId, resultType) {
    placementMode = { recipeId, resultType };
    console.log("[game.js] Entering placement mode:", placementMode);
    // Re-render to show targets
    if (lastData) render(lastData);

    // Update UI hint
    const hint = document.getElementById("placement-hint");
    if (hint) {
      hint.textContent = resultType === "road"
        ? "Click a highlighted edge to place your road.  [Esc to cancel]"
        : "Click a highlighted corner to place your settlement.  [Esc to cancel]";
      hint.style.display = "block";
    }
  }

  function exitPlacementMode() {
    placementMode = null;
    const hint = document.getElementById("placement-hint");
    if (hint) hint.style.display = "none";
    if (lastData) render(lastData);
  }

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && placementMode) exitPlacementMode();
  });

  // ─── Socket ────────────────────────────────────────────────────────────────
  const socket = io();
  window._gameSocket = socket; // expose so HTML layer can emit end-turn

  // Cached game-level state — populated fresh on every get-game-data.
  // myIndex is the authoritative identity; myColorName is a secondary check
  // used by the build handler to match players by colour across reconnects.
  let gameState = {
    players: [], currentUserIndex: 0, myIndex: -1,
    myColorName: null, myResources: {}, recipes: [],
  };

  socket.on("connect", () => {
    console.log("[game.js] Socket connected, sid:", socket.id);
    const lobbyName = (sessionStorage.getItem("currentLobbyName") || "").trim();
    if (lobbyName) {
      socket.emit("lobby-management:join-lobby", { lobby_name: lobbyName });
    }
    if (!lastData) {
    socket.emit("game-management:get-game-data");
  }
  });

  socket.on("connect_error", (err) => console.error("[game.js] Socket connect error:", err));

  socket.on("game-management:get-game-data", (data) => {
    console.log("[game.js] Received game data");
    console.log(data);
    render(data);

    // Always trust my_index from the server — set per-socket, never stale.
    const myIndex    = data.my_index ?? -1;
    const myColorName = data.players?.[myIndex]?.color_type?.name ?? null;

    gameState = {
      players:          data.players ?? [],
      currentUserIndex: data.current_user_index ?? 0,
      myIndex,
      myColorName,
      recipes:          data.prototypes?.filter(p => p.object_type === "recipe-s_prototype") ?? [],
      myResources:      data.players?.[myIndex]?.resources ?? {},
    };

    console.log("[game.js] myIndex:", myIndex, "color:", myColorName);
    window.dispatchEvent(new CustomEvent("game:data", { detail: { ...gameState } }));
  });

  // ── End-turn event from server ─────────────────────────────────────────────
  socket.on("game-management:end-turn", (data) => {
    console.log("[game.js] Received end-turn:", data);
    // data: { rolled_number, next_user_index, players }

    // Snapshot old resource totals before we overwrite state
    const oldResources = gameState.players.map(p =>
      p?.resources ? { ...p.resources } : {}
    );

    gameState.currentUserIndex = data.next_user_index;
    gameState.players          = data.players ?? gameState.players;
    // myIndex is stable for the socket lifetime — server assigns it from
    // the immutable lobby member list.
    gameState.myResources = gameState.players[gameState.myIndex]?.resources
                            ?? gameState.myResources;

    // Diff new vs old to derive gains per player
    const gains = {};
    gameState.players.forEach((player, i) => {
      if (!player?.resources) return;
      const old = oldResources[i] ?? {};
      const playerGains = {};
      for (const [res, amt] of Object.entries(player.resources)) {
        const delta = amt - (old[res] ?? 0);
        if (delta > 0) playerGains[res] = delta;
      }
      if (Object.keys(playerGains).length) gains[i] = playerGains;
    });

    flashMatchingTiles(data.rolled_number);

    for (const [playerIndexStr, playerGains] of Object.entries(gains)) {
      spawnGainPopups(Number(playerIndexStr), playerGains, gameState.players);
    }

    const endTurnDetail = {
      rolledNumber:  data.rolled_number,
      nextUserIndex: data.next_user_index,
      myIndex:       gameState.myIndex,
      players:       gameState.players,
      myResources:   gameState.myResources,
      recipes:       gameState.recipes,
      gains,
    };
    console.log("[game.js] end-turn detail myResources:", endTurnDetail.myResources);
    window.dispatchEvent(new CustomEvent("game:end-turn", { detail: endTurnDetail }));
  });

  // ── Flash tiles matching the rolled number ─────────────────────────────────
  function flashMatchingTiles(rolledNumber) {
    if (!lastData?.fields) return;
    for (const [key, field] of Object.entries(lastData.fields)) {
      if (field.assigned_number !== rolledNumber) continue;

      // Find the pixel coords for this field
      const cleanKey = key.replace(/^"|"$/g, "");
      let parts = cleanKey.split("\u0000");
      if (parts.length !== 2) parts = cleanKey.split("\x00");
      if (parts.length !== 2) continue;
      const q = Number(parts[0]), r = Number(parts[1]);
      if (isNaN(q) || isNaN(r)) continue;

      const { x, y } = hexToPixel(q, r);
      const pts = hexCornerPoints(x, y, HEX_SIZE - 1.5);

      // Bright overlay polygon that fades out
      const flash = svgEl("polygon", {
        points: pointsAttr(pts),
        fill: "rgba(255, 230, 80, 0.55)",
        stroke: "rgba(255, 200, 0, 0.9)",
        "stroke-width": "2.5",
        style: "pointer-events:none; animation: hexFlash 1.1s ease-out forwards",
      });
      svg.appendChild(flash);
      setTimeout(() => flash.remove(), 1200);
    }
  }

  // ── Floating "+N Resource" popups ──────────────────────────────────────────
  function spawnGainPopups(playerIndex, gains, players) {
    // Anchor to the board container so they float above the SVG
    const container = document.getElementById("board-area") || document.body;

    const player = players?.[playerIndex];
    const color  = player ? playerCSSColor(player) : "#fff";

    // Stack multiple resources vertically with a small delay each
    const entries = Object.entries(gains);
    entries.forEach(([resource, amount], i) => {
      const el = document.createElement("div");
      el.className = "gain-popup";
      el.textContent = `+${amount} ${resource}`;
      el.style.cssText = `
        position: absolute;
        left: 50%; top: 50%;
        transform: translate(-50%, -50%);
        font-family: 'Cinzel', serif;
        font-size: 1.05rem;
        font-weight: 700;
        color: ${color};
        text-shadow: 0 0 8px rgba(0,0,0,0.9), 0 2px 4px rgba(0,0,0,0.8);
        pointer-events: none;
        z-index: 50;
        white-space: nowrap;
        animation: floatUp 1.6s ease-out ${i * 0.18}s forwards;
        opacity: 0;
      `;
      container.appendChild(el);
      setTimeout(() => el.remove(), 1600 + i * 180 + 200);
    });
  }

  // ── Build event from server ────────────────────────────────────────────────
  socket.on("game-management:build", (data) => {
    console.log("[game.js] Received build event:", data);

    const { building, location, player } = data;
    const resultType = location.length === 4 ? "road" : "settlement";

    placedBuildings.push({ type: resultType, location, building, player });
    drawBuilding({ type: resultType, location, building, player });

    // Update the players array so everyone's state stays current.
    // Identify which slot this player occupies by colour name — that is
    // stable regardless of socket reconnects or index drift.
    if (data.player?.color_type?.name) {
      const idx = gameState.players.findIndex(
        p => p?.color_type?.name === data.player.color_type.name
      );
      if (idx !== -1) {
        gameState.players[idx] = data.player;
        // If it was our build, refresh resources + panels
        if (idx === gameState.myIndex) {
          gameState.myResources = data.player.resources ?? gameState.myResources;
          console.log("[game.js] build: updating myResources to", gameState.myResources);
          // Spread after setting myResources so the detail has the new value
          window.dispatchEvent(new CustomEvent("game:data", {
            detail: {
              ...gameState,
              myResources: gameState.myResources,
            }
          }));
        }
      }
    }

    window.dispatchEvent(new CustomEvent("game:build-placed", { detail: data }));
  });

  const _onevent = socket.onevent.bind(socket);
  socket.onevent = function (packet) {
    console.log("[game.js] RAW socket event:", packet.data?.[0]);
    _onevent(packet);
  };

  // ─── Controls ──────────────────────────────────────────────────────────────
  document.getElementById("btn-toggle-numbers")?.addEventListener("click", () => {
    showNumbers = !showNumbers;
    if (lastData) render(lastData);
  });

  document.getElementById("btn-toggle-outer")?.addEventListener("click", () => {
    showOuter = !showOuter;
    if (lastData) render(lastData);
  });

  // ─── Recipe buttons ────────────────────────────────────────────────────────
  // Call this from your UI layer when a player clicks "Build Road" / 
  // "Build Settlement" / "Build City".  Pass the recipe name (e.g. "road")
  // and the result prototype type ("road" or "settlement").
  //
  // Example (wire up after get-game-data):
  //   window.GameUI.startBuild("road",       "road");
  //   window.GameUI.startBuild("settlement", "settlement");
  //   window.GameUI.startBuild("city",       "settlement");
  window.GameUI = {
    startBuild(recipeId, resultType) {
      if (placementMode) exitPlacementMode();
      enterPlacementMode(recipeId, resultType);
    },
    cancelBuild() {
      exitPlacementMode();
    },
  };

})();
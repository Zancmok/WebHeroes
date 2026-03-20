(function () {
  // ─── Field styles — keyed by actual Lua field names ──────────────────────────
  const FIELD_STYLES = {
    "forest":      { fill: "#2d5a1b", label: "Forest"     },
    "grass-field": { fill: "#7ec850", label: "Grass Field" },
    "mountain":    { fill: "#6b6b6b", label: "Mountain"   },
    "mine":        { fill: "#8b3a0f", label: "Mine"       },
    "field":       { fill: "#d4b84a", label: "Field"      },
    "desert":      { fill: "#c9b07a", label: "Desert"     },
    "outer-bound": { fill: "#1a3a5c", label: "Deep Sea"   },
    "outer_bound": { fill: "#1a3a5c", label: "Deep Sea"   },
  };

  const IMG_BASE      = "/game-management/img/";
  const NUMBER_COLORS = { 6: "#e05c2e", 8: "#e05c2e" };
  const HEX_SIZE      = 48;

  // ─── Hex math ────────────────────────────────────────────────────────────────
  function hexToPixel(q, r) {
    return {
      x: HEX_SIZE * (Math.sqrt(3) * q + Math.sqrt(3) / 2 * r),
      y: HEX_SIZE * (3 / 2 * r),
    };
  }

  function hexCornerPoints(cx, cy, size) {
    const pts = [];
    for (let i = 0; i < 6; i++) {
      const angle = (Math.PI / 180) * (60 * i + 30);
      pts.push([cx + size * Math.cos(angle), cy + size * Math.sin(angle)]);
    }
    return pts;
  }

  function pointsAttr(pts) { return pts.map(([x, y]) => `${x},${y}`).join(" "); }

  function svgEl(tag, attrs = {}) {
    const el = document.createElementNS("http://www.w3.org/2000/svg", tag);
    for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, v);
    return el;
  }

  function resolveSprite(field) {
    const sprite = field.field_type?.sprite;
    if (sprite) return sprite.replace(/^__|__(?=\/)/g, "").replace("graphics/", "images/");
    return null;
  }

  // ─── State ───────────────────────────────────────────────────────────────────
  const svg     = document.getElementById("board-svg");
  const tooltip = document.getElementById("tooltip");
  const legend  = document.getElementById("legend");

  let showNumbers  = true;
  let showOuter    = true;
  let lastData     = null;
  let lastNonOuter = [];     // cached non-outer hex list, reused by overlay refreshes
  let myUserIndex  = null;
  let currentIndex = 0;
  let playersData  = [];
  let recipesData  = [];
  let pendingBuild = null;   // { recipe, isUpgrade, isRoad }

  // DOM refs injected by buildHUD()
  let endTurnBtn, buildMenuEl, buildListEl, resourcesEl,
      currentPlayerEl, rollResultEl, buildInstrEl;

  // ─── CSS ─────────────────────────────────────────────────────────────────────
  function buildCSS() {
    const s = document.createElement("style");
    s.textContent = `
      #game-hud {
        position: fixed; bottom: 0; left: 0; right: 0;
        background: linear-gradient(to top, rgba(8,18,32,0.98) 70%, transparent);
        padding: 12px 20px 16px;
        display: flex; flex-direction: column; gap: 8px;
        font-family: 'Cinzel', serif; z-index: 100; pointer-events: none;
      }
      #hud-players { display: flex; gap: 10px; pointer-events: none; }
      .player-chip {
        display: flex; align-items: center; gap: 6px;
        background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12);
        border-radius: 6px; padding: 4px 10px; font-size: 11px; color: rgba(255,255,255,0.6);
        transition: all 0.3s;
      }
      .player-chip.active  { background: rgba(255,255,255,0.14); border-color: rgba(255,255,255,0.4); color:#fff; box-shadow:0 0 10px rgba(255,255,255,0.1); }
      .player-chip.me      { border-color: rgba(255,220,100,0.4); }
      .player-chip.active.me { border-color: rgba(255,220,100,0.9); box-shadow:0 0 14px rgba(255,220,100,0.25); }
      .player-color-dot { width:10px; height:10px; border-radius:50%; flex-shrink:0; }
      #hud-bottom { display:flex; align-items:center; justify-content:space-between; gap:16px; pointer-events:all; }
      #hud-resources { display:flex; gap:8px; flex-wrap:wrap; }
      .resource-badge {
        background: rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15);
        border-radius:4px; padding:3px 9px; font-size:12px; color:rgba(255,255,255,0.75);
        display:flex; align-items:center; gap:5px; transition: background 0.2s;
      }
      .resource-badge .res-count { font-weight:bold; color:#fff; font-size:14px; }
      .resource-badge.zero { opacity: 0.4; }
      #hud-actions { display:flex; align-items:center; gap:10px; flex-shrink:0; }
      #hud-turn-info { text-align:right; color:rgba(255,255,255,0.5); font-size:11px; line-height:1.5; }
      #hud-current-player { display:block; color:rgba(255,255,255,0.85); }
      #hud-roll-result { font-size:14px; font-weight:bold; color:#e0c96e; display:block; min-height:18px; opacity:0; }
      #hud-roll-result.roll-fade { animation: roll-show 3.5s ease forwards; }
      @keyframes roll-show { 0%{opacity:1} 70%{opacity:1} 100%{opacity:0} }
      #game-hud button {
        background: rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.22);
        color:#fff; font-family:'Cinzel',serif; font-size:12px; padding:7px 16px;
        border-radius:5px; cursor:pointer; transition:background 0.2s, border-color 0.2s; letter-spacing:0.05em;
      }
      #game-hud button:hover:not(:disabled) { background:rgba(255,255,255,0.16); border-color:rgba(255,255,255,0.5); }
      #game-hud button:disabled { opacity:0.35; cursor:default; }
      #btn-end-turn:not(:disabled) { border-color:rgba(224,201,110,0.6); color:#e0c96e; }
      #build-menu {
        position:fixed; bottom:90px; right:20px;
        background:rgba(8,18,32,0.97); border:1px solid rgba(255,255,255,0.18);
        border-radius:8px; padding:14px 16px; min-width:240px; z-index:200;
        pointer-events:all; box-shadow:0 -4px 30px rgba(0,0,0,0.6);
      }
      #build-menu.hidden { display:none; }
      #build-menu-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; font-size:13px; color:rgba(255,255,255,0.8); letter-spacing:0.08em; }
      #btn-cancel-build { background:none!important; border:none!important; color:rgba(255,255,255,0.45)!important; padding:0!important; font-size:14px!important; cursor:pointer; }
      #build-overlay-instruction {
        position:fixed; top:20px; left:50%; transform:translateX(-50%);
        background:rgba(8,18,32,0.95); border:1px solid rgba(224,201,110,0.5);
        border-radius:6px; padding:8px 18px; font-size:12px; color:#e0c96e;
        font-family:'Crimson Pro',serif; z-index:300; pointer-events:none;
        display:none;
      }
      #build-overlay-instruction.visible { display:block; }
      #build-list { list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:6px; }
      .build-item {
        background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1);
        border-radius:5px; padding:8px 10px; cursor:pointer;
        transition:background 0.15s, border-color 0.15s;
      }
      .build-item:hover:not(.disabled) { background:rgba(255,255,255,0.12); border-color:rgba(255,255,255,0.3); }
      .build-item.disabled { opacity:0.35; cursor:default; }
      .build-item-name { font-size:12px; color:#fff; letter-spacing:0.05em; }
      .build-item-cost { font-size:10px; color:rgba(255,255,255,0.45); margin-top:3px; font-family:'Crimson Pro',serif; }
      .build-item-reason { font-size:10px; color:#e05c2e; margin-top:2px; font-family:'Crimson Pro',serif; }
      .intersection-dot { cursor:pointer; }
      .intersection-dot.build-target { fill:rgba(224,201,110,0.85); stroke:#fff; stroke-width:1.5; animation:pulse-dot 1s ease-in-out infinite alternate; }
      .connection-line { cursor:pointer; stroke-linecap:round; }
      .connection-line.build-target { stroke:rgba(224,201,110,0.85)!important; stroke-width:6!important; animation:pulse-dot 1s ease-in-out infinite alternate; }
      @keyframes pulse-dot { from{opacity:0.5} to{opacity:1} }
      .placed-village { pointer-events:none; }
      .placed-city    { pointer-events:none; }
      .placed-road    { pointer-events:none; }
    `;
    document.head.appendChild(s);
  }

  // ─── HUD DOM ──────────────────────────────────────────────────────────────────
  function buildHUD() {
    // Overlay instruction (outside the build menu so it shows during placement mode)
    buildInstrEl = document.createElement("div");
    buildInstrEl.id = "build-overlay-instruction";
    document.body.appendChild(buildInstrEl);

    const hud = document.createElement("div");
    hud.id = "game-hud";
    hud.innerHTML = `
      <div id="hud-players"></div>
      <div id="hud-bottom">
        <div id="hud-resources"></div>
        <div id="hud-actions">
          <div id="hud-turn-info">
            <span id="hud-current-player">—</span>
            <span id="hud-roll-result"></span>
          </div>
          <button id="btn-end-turn" disabled>Roll &amp; End Turn</button>
          <button id="btn-open-build" disabled>Build</button>
        </div>
      </div>
      <div id="build-menu" class="hidden">
        <div id="build-menu-header">
          <span>Build</span>
          <button id="btn-cancel-build">✕</button>
        </div>
        <ul id="build-list"></ul>
      </div>
    `;
    document.body.appendChild(hud);

    resourcesEl     = hud.querySelector("#hud-resources");
    currentPlayerEl = hud.querySelector("#hud-current-player");
    rollResultEl    = hud.querySelector("#hud-roll-result");
    endTurnBtn      = hud.querySelector("#btn-end-turn");
    buildMenuEl     = hud.querySelector("#build-menu");
    buildListEl     = hud.querySelector("#build-list");

    endTurnBtn.addEventListener("click", () => {
      if (!isMyTurn()) return;
      socket.emit("game-management:end-turn");
      endTurnBtn.disabled = true;
      hud.querySelector("#btn-open-build").disabled = true;
    });

    hud.querySelector("#btn-open-build").addEventListener("click", () => {
      if (!isMyTurn()) return;
      populateBuildMenu();
      buildMenuEl.classList.toggle("hidden");
    });

    hud.querySelector("#btn-cancel-build").addEventListener("click", cancelBuild);
  }

  // ─── HUD updates ─────────────────────────────────────────────────────────────
  function isMyTurn() {
    return myUserIndex !== null && currentIndex === myUserIndex;
  }

  function playerColor(p) {
    return p?.color_type ? `rgb(${p.color_type.r},${p.color_type.g},${p.color_type.b})` : "#888";
  }

  function updateHUD() {
    if (!playersData.length) return;

    const chipsEl = document.getElementById("hud-players");
    if (chipsEl) {
      chipsEl.innerHTML = "";
      playersData.forEach((p, i) => {
        const chip = document.createElement("div");
        chip.className = "player-chip" +
          (i === currentIndex ? " active" : "") +
          (i === myUserIndex  ? " me"     : "");
        chip.innerHTML = `
          <div class="player-color-dot" style="background:${playerColor(p)}"></div>
          <span>${p.color_type?.display_name || "Player " + (i + 1)}${i === myUserIndex ? " (you)" : ""}</span>
        `;
        chipsEl.appendChild(chip);
      });
    }

    const me = playersData[myUserIndex ?? 0];
    if (resourcesEl && me) {
      resourcesEl.innerHTML = "";
      for (const [res, count] of Object.entries(me.resources)) {
        const badge = document.createElement("div");
        badge.className = "resource-badge" + (count === 0 ? " zero" : "");
        badge.innerHTML = `<span class="res-count">${count}</span><span>${res}</span>`;
        resourcesEl.appendChild(badge);
      }
    }

    if (currentPlayerEl) {
      const ap = playersData[currentIndex];
      currentPlayerEl.textContent = ap
        ? (ap.color_type?.display_name || "Player " + (currentIndex + 1)) + "'s turn"
        : "—";
    }

    const myTurn = isMyTurn();
    if (endTurnBtn) endTurnBtn.disabled = !myTurn;
    const buildBtn = document.querySelector("#btn-open-build");
    if (buildBtn) buildBtn.disabled = !myTurn;
  }

  function flashRoll(n) {
    if (!rollResultEl) return;
    rollResultEl.textContent = `🎲  ${n}`;
    rollResultEl.classList.remove("roll-fade");
    // force reflow so removing the class takes effect before re-adding
    void rollResultEl.offsetWidth;
    rollResultEl.classList.add("roll-fade");
  }

  // ─── Build menu ───────────────────────────────────────────────────────────────
  function canBuildRecipe(recipe, me) {
    for (const ing of recipe.ingredients) {
      if ((me.resources[ing.resource] ?? 0) < ing.amount)
        return { ok: false, reason: "Not enough resources" };
    }
    // prerequisite_building is on the result prototype (SettlementPrototype)
    const prereq = recipe.result?.prerequisite_building;
    if (prereq) {
      const hasTarget = Object.values(placedSettlements).some(
        s => s.settlementType === prereq && s.ownerIndex === myUserIndex
      );
      if (!hasTarget)
        return { ok: false, reason: `Requires an existing ${prereq}` };
    }
    return { ok: true };
  }

  function populateBuildMenu() {
    buildListEl.innerHTML = "";
    const me = playersData[myUserIndex ?? 0];
    if (!me || !recipesData.length) {
      buildListEl.innerHTML = `<li style="font-size:11px;color:rgba(255,255,255,0.4);font-family:'Crimson Pro',serif">No recipes available</li>`;
      return;
    }
    recipesData.forEach(recipe => {
      const check = canBuildRecipe(recipe, me);
      const li    = document.createElement("li");
      li.className = "build-item" + (check.ok ? "" : " disabled");
      const costStr = recipe.ingredients.map(ing => `${ing.amount} ${ing.resource}`).join(", ");
      li.innerHTML = `
        <div class="build-item-name">${recipe.result?.display_name || recipe.display_name}</div>
        <div class="build-item-cost">${costStr || "Free"}</div>
        ${!check.ok ? `<div class="build-item-reason">${check.reason}</div>` : ""}
      `;
      if (check.ok) li.addEventListener("click", () => startBuild(recipe));
      buildListEl.appendChild(li);
    });
  }

  function isRoadRecipe(recipe) {
    // object_type on the result prototype tells us what it is
    return recipe.result?.object_type === "road-prototype";
  }

  function startBuild(recipe) {
    const isRoad    = isRoadRecipe(recipe);
    const isUpgrade = !isRoad && !!recipe.result?.prerequisite_building;
    pendingBuild = { recipe, isUpgrade, isRoad };

    // Close the build list, show placement instruction overlay
    buildMenuEl.classList.add("hidden");
    buildInstrEl.textContent = isRoad
      ? "Click an edge between two hexes to place your Road."
      : isUpgrade
        ? "Click one of your existing villages to upgrade it to a City."
        : "Click an intersection (where hexes meet) to place your Village.";
    buildInstrEl.classList.add("visible");

    highlightBuildTargets();
  }

  function cancelBuild() {
    pendingBuild = null;
    clearBuildHighlights();
    buildInstrEl.classList.remove("visible");
    buildMenuEl.classList.add("hidden");
  }

  // ─── Intersection & connection geometry ──────────────────────────────────────
  let parsedHexMap      = {};
  let overlayGroup      = null;
  // Persistent across re-renders (toggle numbers, toggle outer, etc.)
  // pixelKey -> { x, y, color, settlementType, ownerIndex }
  let placedSettlements = {};
  // edgeKey -> { color, ownerIndex }
  let placedRoads       = {};

  /**
   * Build an intersection map: rounded pixel key -> { x, y, hexArr (sorted), pixelKey }
   * Only intersections touched by 3 non-outer hexes are valid build sites.
   * Edge intersections (only 2 hexes) are excluded so we never pad with zeros.
   */
  function computeIntersections(nonOuterHexes) {
    const cornerMap = {};
    for (const { q, r, x, y } of nonOuterHexes) {
      for (const [cx, cy] of hexCornerPoints(x, y, HEX_SIZE - 1.5)) {
        const key = `${Math.round(cx * 2)},${Math.round(cy * 2)}`;
        if (!cornerMap[key]) cornerMap[key] = { x: cx, y: cy, hexes: [] };
        cornerMap[key].hexes.push([q, r]);
      }
    }
    const out = {};
    for (const [key, val] of Object.entries(cornerMap)) {
      const hexArr = val.hexes.sort((a, b) => a[0] - b[0] || a[1] - b[1]);
      out[key] = { x: val.x, y: val.y, hexArr, pixelKey: key };
    }
    return out;
  }

  /**
   * Build a connection (edge) map: edgeKey -> { x1, y1, x2, y2, hexPair (sorted), edgeKey }
   * Only edges shared by exactly 2 non-outer hexes.
   */
  function computeConnections(nonOuterHexes) {
    const edgeMap = {};
    for (const { q, r, x, y } of nonOuterHexes) {
      const corners = hexCornerPoints(x, y, HEX_SIZE - 1.5);
      for (let i = 0; i < 6; i++) {
        const [ax, ay] = corners[i];
        const [bx, by] = corners[(i + 1) % 6];
        const key = [
          Math.round(ax * 2), Math.round(ay * 2),
          Math.round(bx * 2), Math.round(by * 2),
        ].sort((a, b) => a - b).join(",");
        if (!edgeMap[key]) edgeMap[key] = { ax, ay, bx, by, hexes: [], edgeKey: key };
        edgeMap[key].hexes.push([q, r]);
      }
    }
    const out = {};
    for (const [key, val] of Object.entries(edgeMap)) {
      if (val.hexes.length !== 2) continue;
      const hexPair = val.hexes.sort((a, b) => a[0] - b[0] || a[1] - b[1]);
      out[key] = { ax: val.ax, ay: val.ay, bx: val.bx, by: val.by, hexPair, edgeKey: key };
    }
    return out;
  }

  function intersectionToLocation(hexArr) {
    const loc = hexArr.flat();
    while (loc.length < 6) loc.push(0);
    return loc;
  }

  /** Convert 2-hex edge to the flat [q1,r1,q2,r2] location array the server expects. */
  function connectionToLocation(hexPair) {
    return hexPair.flat();
  }

  function renderOverlay(nonOuterHexes) {
    if (overlayGroup) overlayGroup.remove();
    overlayGroup = svgEl("g", { id: "overlay-group" });
    svg.appendChild(overlayGroup);

    const intersections = computeIntersections(nonOuterHexes);
    const connections   = computeConnections(nonOuterHexes);

    // ── Placed roads ──
    for (const [edgeKey, road] of Object.entries(placedRoads)) {
      const conn = connections[edgeKey];
      if (!conn) continue;
      overlayGroup.appendChild(svgEl("line", {
        class: "placed-road",
        x1: conn.ax, y1: conn.ay, x2: conn.bx, y2: conn.by,
        stroke: road.color, "stroke-width": "5", "stroke-linecap": "round",
      }));
    }

    // ── Placed settlements ──
    for (const s of Object.values(placedSettlements)) {
      if (s.settlementType === "village") {
        overlayGroup.appendChild(svgEl("rect", {
          class: "placed-village",
          x: s.x - 7, y: s.y - 7, width: 14, height: 14,
          fill: s.color, stroke: "#fff", "stroke-width": "1.5", rx: 2,
        }));
      } else {
        const d = 10;
        overlayGroup.appendChild(svgEl("polygon", {
          class: "placed-city",
          points: `${s.x},${s.y-d} ${s.x+d},${s.y} ${s.x},${s.y+d} ${s.x-d},${s.y}`,
          fill: s.color, stroke: "#fff", "stroke-width": "1.5",
        }));
      }
    }

    // ── Connection (road) hit lines ──
    for (const [, conn] of Object.entries(connections)) {
      const mx = (conn.ax + conn.bx) / 2;
      const my = (conn.ay + conn.by) / 2;
      const line = svgEl("line", {
        class: "connection-line",
        x1: conn.ax, y1: conn.ay, x2: conn.bx, y2: conn.by,
        stroke: "rgba(255,255,255,0.0)", "stroke-width": "8",
        "data-edge-key": conn.edgeKey,
      });
      line._conn = conn;
      line.addEventListener("click", () => onConnectionClick(conn));
      overlayGroup.appendChild(line);
    }

    // ── Intersection dots ──
    for (const [key, inter] of Object.entries(intersections)) {
      const hasBuilding = !!placedSettlements[key];
      const circle = svgEl("circle", {
        class: "intersection-dot",
        cx: inter.x, cy: inter.y, r: hasBuilding ? 0 : 4,
        fill: "rgba(255,255,255,0.15)",
        stroke: "rgba(255,255,255,0.3)", "stroke-width": "1",
        "data-key": key,
      });
      circle._inter = inter;
      circle.addEventListener("click", () => onIntersectionClick(inter));
      overlayGroup.appendChild(circle);
    }

    overlayGroup._intersections = intersections;
    overlayGroup._connections   = connections;
  }

  function onIntersectionClick(inter) {
    if (!pendingBuild || !isMyTurn() || pendingBuild.isRoad) return;
    const existing = placedSettlements[inter.pixelKey];

    if (pendingBuild.isUpgrade) {
      // Must click an owned village
      const prereq = pendingBuild.recipe.result?.prerequisite_building;
      if (!existing || existing.settlementType !== prereq || existing.ownerIndex !== myUserIndex) return;
    } else {
      if (existing) return;
    }

    const loc = intersectionToLocation(inter.hexArr);
    socket.emit("game-management:build", { recipe_id: pendingBuild.recipe.name, location: loc });
    cancelBuild();
  }

  function onConnectionClick(conn) {
    if (!pendingBuild || !isMyTurn() || !pendingBuild.isRoad) return;
    if (placedRoads[conn.edgeKey]) return; // already a road here

    const loc = connectionToLocation(conn.hexPair);
    socket.emit("game-management:build", { recipe_id: pendingBuild.recipe.name, location: loc });
    cancelBuild();
  }

  function highlightBuildTargets() {
    if (!overlayGroup) return;

    if (pendingBuild?.isRoad) {
      // Highlight connection lines that are empty
      overlayGroup.querySelectorAll(".connection-line").forEach(el => {
        const key = el.getAttribute("data-edge-key");
        if (!placedRoads[key]) el.classList.add("build-target");
      });
    } else {
      overlayGroup.querySelectorAll(".intersection-dot").forEach(el => {
        const key      = el.getAttribute("data-key");
        const existing = placedSettlements[key];
        if (pendingBuild?.isUpgrade) {
          const prereq = pendingBuild.recipe.result?.prerequisite_building;
          if (existing?.settlementType === prereq && existing?.ownerIndex === myUserIndex)
            el.classList.add("build-target");
        } else {
          if (!existing) el.classList.add("build-target");
        }
      });
    }
  }

  function clearBuildHighlights() {
    if (!overlayGroup) return;
    overlayGroup.querySelectorAll(".intersection-dot, .connection-line")
      .forEach(el => el.classList.remove("build-target"));
  }

  // ─── Snap helpers ────────────────────────────────────────────────────────────
  function locationToIntersectionKey(loc) {
    if (!overlayGroup?._intersections) return null;
    const pairs = [];
    for (let i = 0; i < loc.length - 1; i += 2) {
      if (loc[i] === 0 && loc[i + 1] === 0) continue; // skip padding
      pairs.push([loc[i], loc[i + 1]]);
    }
    const hexArr = pairs.sort((a, b) => a[0] - b[0] || a[1] - b[1]);

    for (const [key, inter] of Object.entries(overlayGroup._intersections)) {
      const iArr = inter.hexArr;
      if (iArr.length !== hexArr.length) continue;
      if (iArr.every((h, i) => h[0] === hexArr[i][0] && h[1] === hexArr[i][1])) return key;
    }
    return null;
  }

  /**
   * Given a flat location array [q1,r1,q2,r2] from the server,
   * find the matching connection edgeKey in the current overlay.
   */
  function locationToEdgeKey(loc) {
    if (!overlayGroup?._connections) return null;
    const hexPair = [[loc[0], loc[1]], [loc[2], loc[3]]]
      .sort((a, b) => a[0] - b[0] || a[1] - b[1]);

    for (const [key, conn] of Object.entries(overlayGroup._connections)) {
      const cp = conn.hexPair;
      if (
        cp[0][0] === hexPair[0][0] && cp[0][1] === hexPair[0][1] &&
        cp[1][0] === hexPair[1][0] && cp[1][1] === hexPair[1][1]
      ) return key;
    }
    return null;
  }

  // ─── Main render ──────────────────────────────────────────────────────────────
  function isOuterField(fieldData) {
    return fieldData?.field_type?.name?.includes("outer") ?? false;
  }

  function render(data) {
    console.log("[game.js] render()");
    lastData      = data;
    svg.innerHTML = "";
    overlayGroup  = null;

    if (!data?.fields) { svg.setAttribute("viewBox", "0 0 400 400"); return; }

    if (data.prototypes) {
      recipesData = data.prototypes.filter(p => p.object_type === "recipe-s_prototype");
      console.log("[game.js] recipes:", recipesData.map(r => r.name));
    }
    if (data.players)                    playersData  = data.players;
    // Default to 0 if server doesn't send my_index
    myUserIndex = data.my_index ?? 0;
    if (data.current_user_index != null) currentIndex = data.current_user_index;

    const parsed = [];
    parsedHexMap = {};

    for (const [key, field] of Object.entries(data.fields)) {
      const clean = key.replace(/^"|"$/g, "");
      let parts   = clean.split("\u0000");
      if (parts.length !== 2) parts = clean.split("\x00");
      if (parts.length !== 2) continue;
      const q = Number(parts[0]), r = Number(parts[1]);
      if (isNaN(q) || isNaN(r)) continue;
      const { x, y } = hexToPixel(q, r);
      parsed.push({ q, r, x, y, field });
      parsedHexMap[`${q},${r}`] = { q, r, x, y };
    }
    if (!parsed.length) return;

    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    for (const { x, y } of parsed) {
      minX = Math.min(minX, x - HEX_SIZE); minY = Math.min(minY, y - HEX_SIZE);
      maxX = Math.max(maxX, x + HEX_SIZE); maxY = Math.max(maxY, y + HEX_SIZE);
    }
    const pad = 12;
    svg.setAttribute("viewBox", `${minX-pad} ${minY-pad} ${maxX-minX+pad*2} ${maxY-minY+pad*2}`);
    svg.setAttribute("width",  maxX - minX + pad * 2);
    svg.setAttribute("height", maxY - minY + pad * 2);

    parsed.sort((a, b) => (isOuterField(a.field)?0:1) - (isOuterField(b.field)?0:1));

    const defs = svgEl("defs");
    const filt = svgEl("filter", { id:"hex-shadow", x:"-20%", y:"-20%", width:"140%", height:"140%" });
    filt.appendChild(svgEl("feDropShadow", { dx:"0", dy:"3", stdDeviation:"4", "flood-color":"rgba(0,0,0,0.5)" }));
    defs.appendChild(filt);
    for (const { x, y, q, r } of parsed) {
      const cp = svgEl("clipPath", { id:`clip-${q}-${r}` });
      cp.appendChild(svgEl("polygon", { points: pointsAttr(hexCornerPoints(x, y, HEX_SIZE-1.5)) }));
      defs.appendChild(cp);
    }
    svg.appendChild(defs);

    const seen = new Set();
    for (const { x, y, q, r, field } of parsed) {
      const typeName = field.field_type?.name || "";
      const isOuter  = isOuterField(field);
      if (isOuter && !showOuter) continue;

      const style  = FIELD_STYLES[typeName] || { fill: "#888", label: field.field_type?.display_name || typeName };
      const pts    = hexCornerPoints(x, y, HEX_SIZE - 1.5);
      const pAttr  = pointsAttr(pts);
      const sprite = resolveSprite(field);
      const g      = svgEl("g", { class: isOuter ? "hex-cell hex-outer" : "hex-cell" });

      g.appendChild(svgEl("polygon", { points: pAttr, fill: style.fill, stroke: "none" }));
      if (sprite) {
        const imgSize = HEX_SIZE * 2.05;
        g.appendChild(svgEl("image", {
          href: `${IMG_BASE}${sprite}`,
          x: x - imgSize/2, y: y - imgSize/2, width: imgSize, height: imgSize,
          preserveAspectRatio: "xMidYMid slice", "clip-path": `url(#clip-${q}-${r})`,
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
          const numColor = NUMBER_COLORS[field.assigned_number] || "#1a1a1a";
          g.appendChild(svgEl("circle", { cx:x, cy:y, r:16, fill:"rgba(245,234,208,0.93)", stroke:"rgba(0,0,0,0.35)", "stroke-width":"1.5" }));
          const txt = svgEl("text", { x, y, "text-anchor":"middle", "dominant-baseline":"central", fill:numColor, "font-size":"14", "font-family":"Cinzel, serif", "font-weight":"bold" });
          txt.textContent = field.assigned_number;
          g.appendChild(txt);
        } else if (!sprite) {
          const lbl = svgEl("text", { x, y, "text-anchor":"middle", "dominant-baseline":"central", fill:"rgba(255,255,255,0.55)", "font-size":"9", "font-family":"Crimson Pro, serif", "letter-spacing":"0.05em" });
          lbl.textContent = (style.label || typeName).toUpperCase();
          g.appendChild(lbl);
        }
        g.addEventListener("mousemove", (e) => {
          const lines = [`Type: ${field.field_type?.display_name || style.label || typeName}`];
          if (field.field_type?.resource) lines.push(`Resource: ${field.field_type.resource}`);
          if (field.assigned_number)      lines.push(`Number: ${field.assigned_number}`);
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

    // Legend
    legend.innerHTML = "";
    for (const ft of seen) {
      const style  = FIELD_STYLES[ft] || { fill: "#888", label: ft };
      const item   = document.createElement("div");
      item.className = "legend-item";
      const swatch = document.createElement("div");
      swatch.className = "legend-swatch";
      const sample = parsed.find(p => p.field.field_type?.name === ft);
      const sp     = sample ? resolveSprite(sample.field) : null;
      if (sp) { swatch.style.backgroundImage = `url(${IMG_BASE}${sp})`; swatch.style.backgroundSize = "cover"; swatch.style.backgroundPosition = "center"; }
      else      { swatch.style.background = style.fill; }
      const lbl = document.createElement("span");
      lbl.textContent = sample?.field.field_type?.display_name || style.label || ft;
      item.appendChild(swatch); item.appendChild(lbl);
      legend.appendChild(item);
    }

    const nonOuter = parsed.filter(p => !isOuterField(p.field));
    lastNonOuter = nonOuter;   // cache for overlay refreshes
    renderOverlay(nonOuter);
    updateHUD();
    console.log("[game.js] render complete");
  }

  // ─── Socket ──────────────────────────────────────────────────────────────────
  const socket = io();

  socket.on("connect", () => {
    console.log("[game.js] connected:", socket.id);
    const lobbyName = (sessionStorage.getItem("currentLobbyName") || "").trim();
    if (lobbyName) socket.emit("lobby-management:join-lobby", { lobby_name: lobbyName });
    socket.emit("game-management:get-game-data");
  });

  socket.on("connect_error", err => console.error("[game.js] connect error:", err));

  socket.on("game-management:get-game-data", (data) => {
    console.log("[game.js] game data received");
    myUserIndex  = data.my_index ?? 0;
    if (data.current_user_index != null) currentIndex = data.current_user_index;
    render(data);
  });

  socket.on("game-management:end-turn", (data) => {
    console.log("[game.js] end-turn:", data);
    if (data.rolled_number   != null) flashRoll(data.rolled_number);
    if (data.next_user_index != null) currentIndex = data.next_user_index;
    if (data.players)                 playersData  = data.players;
    updateHUD(); // re-evaluates isMyTurn() and re-enables buttons accordingly
  });

  socket.on("game-management:build", (data) => {
    console.log("[game.js] build received:", data);
    if (!data.location || !data.player || !data.building) return;

    const loc        = data.location;
    const color      = playerColor(data.player);
    const ownerIndex = playersData.findIndex(p => p.color_type?.name === data.player.color_type?.name);

    if (data.building.object_type === "road-prototype" && loc.length === 4) {
      // ── Road ──
      const edgeKey = locationToEdgeKey(loc);
      if (edgeKey) placedRoads[edgeKey] = { color, ownerIndex };

    } else if (loc.length === 6) {
      // ── Settlement / City ──
      const settlementType = data.building.name; // e.g. "village" or "city"
      const interKey = locationToIntersectionKey(loc);
      if (interKey && overlayGroup?._intersections?.[interKey]) {
        const inter = overlayGroup._intersections[interKey];
        placedSettlements[interKey] = {
          x: inter.x, y: inter.y,
          color, settlementType, ownerIndex,
        };
      }
    }

    if (data.players) playersData = data.players;

    renderOverlay(lastNonOuter);
    updateHUD();
  });

  // ─── Controls ─────────────────────────────────────────────────────────────────
  document.getElementById("btn-toggle-numbers").addEventListener("click", () => {
    showNumbers = !showNumbers;
    if (lastData) render(lastData);
  });
  document.getElementById("btn-toggle-outer").addEventListener("click", () => {
    showOuter = !showOuter;
    if (lastData) render(lastData);
  });

  // ─── Init ─────────────────────────────────────────────────────────────────────
  buildCSS();
  buildHUD();
})();
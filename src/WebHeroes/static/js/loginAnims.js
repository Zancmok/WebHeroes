/* ============================================================
   1. HEX GRID CANVAS — animated Catan-style board in background
   ============================================================ */
(function () {
  const canvas = document.getElementById('hexCanvas');
  const ctx = canvas.getContext('2d');
  let W, H, hexes = [];

  const TILE_COLORS = [
    { fill: '#1a4a14', stroke: '#2d7a22' },
    { fill: '#7a5c0a', stroke: '#b8860b' },
    { fill: '#4a4040', stroke: '#6b6b6b' },
    { fill: '#2d5c25', stroke: '#4a8a3a' },
    { fill: '#6b2e0e', stroke: '#8b4513' },
    { fill: '#8a7010', stroke: '#c8a850' },
    { fill: '#0e3460', stroke: '#1e5080' },
  ];

  const NUM_DICE = ['②', '③', '④', '⑤', '⑥', '⑧', '⑨', '⑩', '⑪', '⑫'];

  function resize() {
    W = canvas.width  = window.innerWidth;
    H = canvas.height = window.innerHeight;
    buildGrid();
  }

  function buildGrid() {
    hexes = [];
    const SIZE = 70;
    const HW   = SIZE * Math.sqrt(3);
    const HH   = SIZE * 2;
    const cols = Math.ceil(W / HW) + 3;
    const rows = Math.ceil(H / (HH * 0.75)) + 3;

    for (let r = -1; r < rows; r++) {
      for (let c = -1; c < cols; c++) {
        const xOff = (r % 2 === 0 ? 0 : HW / 2);
        const x    = c * HW + xOff + HW * 0.5;
        const y    = r * HH * 0.75 + HH * 0.5;
        const tile = TILE_COLORS[Math.floor(Math.random() * TILE_COLORS.length)];
        hexes.push({
          x, y, size: SIZE,
          fill: tile.fill, stroke: tile.stroke,
          label: Math.random() > 0.4 ? NUM_DICE[Math.floor(Math.random() * NUM_DICE.length)] : '',
          phase: Math.random() * Math.PI * 2,
          speed: 0.3 + Math.random() * 0.7,
          baseAlpha: 0.15 + Math.random() * 0.35,
        });
      }
    }
  }

  function drawHex(x, y, size, fillColor, strokeColor, alpha) {
    ctx.save();
    ctx.globalAlpha = alpha;
    ctx.translate(x, y);
    ctx.beginPath();
    for (let i = 0; i < 6; i++) {
      const angle = (Math.PI / 180) * (60 * i - 30);
      i === 0
        ? ctx.moveTo(size * Math.cos(angle), size * Math.sin(angle))
        : ctx.lineTo(size * Math.cos(angle), size * Math.sin(angle));
    }
    ctx.closePath();
    ctx.fillStyle = fillColor;
    ctx.fill();
    ctx.strokeStyle = strokeColor;
    ctx.lineWidth = 1.5;
    ctx.stroke();
    ctx.restore();
  }

  let t = 0;
  function animate() {
    ctx.clearRect(0, 0, W, H);
    t += 0.008;
    hexes.forEach(h => {
      const a = h.baseAlpha + (Math.sin(t * h.speed + h.phase) * 0.5 + 0.5) * 0.12;
      drawHex(h.x, h.y, h.size, h.fill, h.stroke, a);
      if (h.label) {
        ctx.save();
        ctx.globalAlpha = a * 0.9;
        ctx.beginPath();
        ctx.arc(h.x, h.y, 14, 0, Math.PI * 2);
        ctx.fillStyle = '#e8d5a0';
        ctx.fill();
        ctx.strokeStyle = '#8b7355';
        ctx.lineWidth = 1;
        ctx.stroke();
        ctx.font = '12px Georgia';
        ctx.fillStyle = '#3d2b1a';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(h.label, h.x, h.y);
        ctx.restore();
      }
    });
    requestAnimationFrame(animate);
  }

  window.addEventListener('resize', resize);
  resize();
  animate();
})();

/* ============================================================
   2. FLOATING RESOURCE ICONS
   ============================================================ */
(function () {
  const resources = ['🌲', '🌾', '🐑', '🧱', '⛰️', '🌊', '⚓', '⚒'];
  function spawnResource() {
    const el = document.createElement('div');
    el.className = 'resource-float';
    el.textContent = resources[Math.floor(Math.random() * resources.length)];
    el.style.left   = (Math.random() * 100) + 'vw';
    el.style.bottom = '-2rem';
    const dur = 8 + Math.random() * 10;
    el.style.animationDuration = dur + 's';
    el.style.animationDelay    = (Math.random() * 4) + 's';
    el.style.fontSize          = (0.9 + Math.random() * 0.8) + 'rem';
    document.body.appendChild(el);
    setTimeout(() => el.remove(), (dur + 4) * 1000);
  }
  setInterval(spawnResource, 1200);
  for (let i = 0; i < 6; i++) setTimeout(spawnResource, i * 300);
})();

/* ============================================================
   3. MOUSE TRAIL — golden road dots
   ============================================================ */
(function () {
  let last = 0;
  document.addEventListener('mousemove', e => {
    const now = Date.now();
    if (now - last < 60) return;
    last = now;
    const dot = document.createElement('div');
    dot.className = 'trail-dot';
    dot.style.left = e.clientX + 'px';
    dot.style.top  = e.clientY + 'px';
    document.body.appendChild(dot);
    setTimeout(() => dot.remove(), 900);
  });
})();

/* ============================================================
   4. TAB ANIMATION — staggered form items appear
   ============================================================ */
function revealFormItems(paneId) {
  const pane  = document.getElementById(paneId);
  const items = pane.querySelectorAll('.form-item');
  items.forEach(item => {
    item.classList.remove('visible');
    item.style.transitionDelay = '0s';
  });
  requestAnimationFrame(() => {
    items.forEach((item, i) => {
      item.style.transitionDelay = (i * 0.1 + 0.1) + 's';
      setTimeout(() => item.classList.add('visible'), 20);
    });
  });
}

/* ============================================================
   5. DICE ROLL — exposed globally so login.js can call it
   ============================================================ */
const DICE_FACES = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅'];

function rollDice(callback) {
  const overlay = document.getElementById('diceOverlay');
  const d1 = document.getElementById('die1');
  const d2 = document.getElementById('die2');
  overlay.classList.add('active');
  let cycles = 0;
  const interval = setInterval(() => {
    d1.textContent = DICE_FACES[Math.floor(Math.random() * 6)];
    d2.textContent = DICE_FACES[Math.floor(Math.random() * 6)];
    void d1.offsetWidth;
    void d2.offsetWidth;
    if (++cycles >= 10) {
      clearInterval(interval);
      setTimeout(() => {
        overlay.classList.remove('active');
        if (callback) callback();
      }, 600);
    }
  }, 120);
}

/* ============================================================
   6. CARD TILT ON HOVER
   ============================================================ */
function initCardTilt() {
  const card = document.querySelector('.card');
  card.addEventListener('mousemove', function (e) {
    const rect = this.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width  - 0.5;
    const y = (e.clientY - rect.top)  / rect.height - 0.5;
    this.style.transform = `perspective(800px) rotateY(${x * 5}deg) rotateX(${-y * 5}deg)`;
  });
  card.addEventListener('mouseleave', function () {
    this.style.transition = 'transform 0.5s ease';
    this.style.transform  = 'perspective(800px) rotateY(0deg) rotateX(0deg)';
  });
}

/* ============================================================
   7. INIT ON DOM READY
   ============================================================ */
document.addEventListener('DOMContentLoaded', () => {
  revealFormItems('signup');
  initCardTilt();

  document.querySelectorAll('.nav-link').forEach(tab => {
    tab.addEventListener('shown.bs.tab', function (e) {
      const target = e.target.getAttribute('href').replace('#', '');
      revealFormItems(target);
    });
  });
});
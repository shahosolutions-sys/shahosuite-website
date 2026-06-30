/** Soft connected-square hero background (homepage-style, lighter on inner pages). */
(function () {
  var canvas = document.getElementById('hero-canvas');
  if (!canvas) return;

  var variant = canvas.getAttribute('data-variant') || 'wholesale';
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var small = window.matchMedia('(max-width: 560px)').matches;
  var ctx = canvas.getContext('2d');
  var palettes = {
    wholesale: ['#93c5fd', '#60a5fa', '#6ee7b7', '#67e8f9', '#a5b4fc'],
    landlord: ['#6ee7b7', '#34d399', '#a7f3d0', '#67e8f9', '#86efac'],
    neutral: ['#cbd5e1', '#94a3b8', '#bae6fd', '#bbf7d0', '#c4b5fd']
  };
  var COLORS = palettes[variant] || palettes.neutral;
  var MAX_DIST = 118;
  var W, H, nodes = [];
  var total = reduced ? 28 : (small ? 36 : 52);

  function resize() {
    W = canvas.width = canvas.offsetWidth;
    H = canvas.height = canvas.offsetHeight;
    nodes = [];
    for (var i = 0; i < total; i++) {
      nodes.push({
        x: Math.random() * W,
        y: Math.random() * H,
        vx: (Math.random() - 0.5) * (reduced ? 0.05 : 0.11),
        vy: (Math.random() - 0.5) * (reduced ? 0.05 : 0.11),
        s: 3 + Math.random() * 3.5,
        c: COLORS[Math.floor(Math.random() * COLORS.length)],
        p: Math.random() * Math.PI * 2
      });
    }
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);
    var t = performance.now() * 0.001;
    var i, j, n, a, b, dx, dy, dist, alpha, pulse, size, radius;

    for (i = 0; i < nodes.length; i++) {
      n = nodes[i];
      n.x += n.vx;
      n.y += n.vy;
      if (n.x < -12) n.x = W + 12;
      if (n.x > W + 12) n.x = -12;
      if (n.y < -12) n.y = H + 12;
      if (n.y > H + 12) n.y = -12;
    }

    for (i = 0; i < nodes.length; i++) {
      for (j = i + 1; j < nodes.length; j++) {
        a = nodes[i];
        b = nodes[j];
        dx = a.x - b.x;
        dy = a.y - b.y;
        dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < MAX_DIST) {
          alpha = (1 - dist / MAX_DIST) * 0.16;
          ctx.strokeStyle = 'rgba(71,85,105,' + alpha + ')';
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.stroke();
        }
      }
    }

    for (i = 0; i < nodes.length; i++) {
      n = nodes[i];
      pulse = 0.7 + Math.sin(t * 0.85 + n.p) * 0.22;
      size = n.s * pulse;
      radius = 2;
      ctx.globalAlpha = 0.5;
      ctx.fillStyle = n.c;
      ctx.beginPath();
      ctx.moveTo(n.x - size / 2 + radius, n.y - size / 2);
      ctx.lineTo(n.x + size / 2 - radius, n.y - size / 2);
      ctx.quadraticCurveTo(n.x + size / 2, n.y - size / 2, n.x + size / 2, n.y - size / 2 + radius);
      ctx.lineTo(n.x + size / 2, n.y + size / 2 - radius);
      ctx.quadraticCurveTo(n.x + size / 2, n.y + size / 2, n.x + size / 2 - radius, n.y + size / 2);
      ctx.lineTo(n.x - size / 2 + radius, n.y + size / 2);
      ctx.quadraticCurveTo(n.x - size / 2, n.y + size / 2, n.x - size / 2, n.y + size / 2 - radius);
      ctx.lineTo(n.x - size / 2, n.y - size / 2 + radius);
      ctx.quadraticCurveTo(n.x - size / 2, n.y - size / 2, n.x - size / 2 + radius, n.y - size / 2);
      ctx.closePath();
      ctx.fill();
    }
    ctx.globalAlpha = 1;
    if (!reduced) requestAnimationFrame(draw);
  }

  resize();
  window.addEventListener('resize', resize);
  if (reduced) draw();
  else requestAnimationFrame(draw);
})();

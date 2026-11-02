// Vídeo longo "Cinco pães" · palco 16:9 com partículas (lado direito da tela).
// As formações usam o mesmo sistema de coordenadas do Short (centro 540,1110) e são convertidas para o palco 16:9.
// A linha do tempo vem pronta do roteiro: R.cenas16 = [{t, form, o, D}], R.ov = [{a, b, html, css}], R.cnt = [{a, b, de, para, dur, pre, leg}].
window.EXTRA = (() => {
  const NP = 300, NB = 200, N = NP + NB, CX = 540, CY = 1110;
  const SX = 1380, SY = 600, S = .8; // centro e escala do palco 16:9
  let cv, ctx, cols, TL, OV = [], CNT;
  let sd = 7; const rnd = () => (sd = (sd * 16807) % 2147483647) / 2147483647;
  const P = Array.from({ length: N }, () => ({ ph: rnd() * 6.28, w: .6 + rnd() * .9, d: rnd(), sx: 110 + rnd() * 860, sy: 780 + rnd() * 660, v: .5 + rnd(), dir: rnd() * 2 - 1 }));
  const smooth = x => { x = clamp(x); return x * x * (3 - 2 * x); };
  const sun = (k, n, R) => { const r = R * Math.sqrt((k + .5) / n), a = k * 2.39996; return [Math.cos(a) * r, Math.sin(a) * r]; };
  const hex = h => [1, 3, 5].map(i => parseInt(h.trim().slice(i, i + 2), 16));
  const mix = (a, b, k) => a.map((v, i) => v + (b[i] - v) * k);
  const H = (i, x = CX, y = CY) => ({ x, y, r: 3, a: 0, c: cols.ink, sq: 0 });
  const D = (x, y, r, a, c, sq = 0) => ({ x, y, r, a, c, sq });
  // posições dos cestos (no sistema do Short)
  const K12 = c => [CX + ((c % 6) - 2.5) * 150, c < 6 ? CY - 60 : CY + 200];
  const K7 = c => [CX + (c - 3) * 125, CY + 180];

  const F = {
    poeira: (i, t) => D(P[i].sx + Math.sin(t * .4 * P[i].w + P[i].ph) * 30, P[i].sy + Math.cos(t * .3 * P[i].w + P[i].ph) * 30, 3, i < NP ? .35 : 0, cols.ink),
    calendario: (i, t, dt, o) => {
      if (i < NP) return H(i, P[i].sx, P[i].sy);
      const k = i - NP, cx = k % 20, cy = (k / 20) | 0, lit = o.acende ? clamp((dt - o.acende[0] - k * o.acende[1] / NB) / .25) : 1;
      return D(CX - 390 + cx * 41, CY - 190 + cy * 41, 15, .25 + .75 * lit, mix(cols.muted, cols.acc, lit), 1);
    },
    colunas4: (i, t, dt, o) => {
      if (i >= NP) return H(i);
      const c = (i / 75) | 0, j = i % 75, lit = clamp((dt - .3 - c * (o.passo || .7)) / .4);
      return D(CX + (c - 1.5) * 210 + ((j % 5) - 2) * 26, CY + 230 - ((j / 5) | 0) * 30, 9, .2 + .8 * lit, mix(cols.muted, c === 3 ? cols.acc : cols.ink, lit), .6);
    },
    multidao: (i, t, dt, o) => {
      if (i >= NP) return H(i);
      const n = o.n, on = i < n, [x, y] = sun(i, on ? n : NP, o.R);
      return D(CX + x + Math.sin(t * .8 * P[i].w + P[i].ph) * 3, CY + y + Math.cos(t * .7 * P[i].w + P[i].ph) * 3, 7, on ? (o.a || .9) : 0, i < 100 ? cols.ink : mix(cols.ink, cols.acc, .35));
    },
    ponto: (i, t, dt, o) => { const [x, y] = sun(i % 40, 40, (o.R || 14) + Math.sin(t * 3) * 3), f = o.apaga ? clamp(1 - (dt - 1) / 2.5) * .9 + .1 : 1;
      return D(CX + x, CY - 40 + y, 3.5, (i < 40 ? 1 : 0) * f, o.apaga ? mix(cols.acc, cols.muted, 1 - f) : cols.acc); },
    lago: (i, t, dt, o) => {
      if (i >= NP) { const a = (i - NP) / NB * 6.2832; return D(CX + Math.sin(a) * 230 * (1 + .12 * Math.cos(a)), CY + 20 - Math.cos(a) * 300, 4, .55, cols.muted); }
      if (i < 6) { const p = smooth((dt - .5) / (o.barco || 6)), [x, y] = sun(i, 6, 12);
        return D(CX - 120 + 250 * p + x, CY + 60 - 230 * p + y, 6, 1, cols.acc); }
      if (!o.margem) return H(i, CX - 300, CY + 120);
      const lag = P[i].d * 1.5, p = smooth((dt - .3 - lag) / 4.5), a = -2.2 + 2.6 * p; // anda pela margem norte de oeste para nordeste
      return D(CX + Math.sin(a) * 270 + Math.sin(i) * 10, CY + 20 - Math.cos(a) * 340 + Math.cos(i * 1.7) * 10, 5, p > 0 ? .85 : 0, cols.ink);
    },
    campo: (i, t) => {
      if (i < NP) { const cx = i % 20, cy = (i / 20) | 0; return D(CX - 400 + cx * 42 + Math.sin(t * 1.2 + cy * .5 + cx * .2) * 6, CY + 30 + cy * 20, 3.5 + cy * .15, .35 + cy * .03, cols.muted); }
      const k = i - NP; if (k >= 64) return H(i, CX, CY - 100);
      const row = k >> 1, s = k % 2 ? 1 : -1; // espiga: grãos em zigue-zague subindo a haste
      return D(CX + s * (16 - row * .2) + Math.sin(t * 1.2) * 5, CY - 30 - row * 13, 8 - row * .1, 1, cols.acc);
    },
    cidade: (i, t, dt, o) => {
      if (i >= NP) return H(i);
      const k = (i / 30) | 0, j = i % 30, [x, y] = sun(j, 30, 42), n = Math.min(10, 1 + Math.floor(clamp((dt - (o.cresce?.[0] ?? 99)) / (o.cresce?.[1] ?? 1)) * 9.99));
      const gx = k % 5, gy = (k / 5) | 0, on = k < n;
      return D(CX + (gx - 2) * 165 + x, CY - 60 + gy * 230 + y, 5.5, on ? .9 : 0, k ? cols.ink : cols.acc);
    },
    lanche: (i) => {
      if (i < NP) { const [x, y] = sun(i, NP, 300); return D(CX + x, CY + y, 4, 0, cols.ink); }
      const k = i - NP;
      if (k < 150) { const p = (k / 30) | 0, j = k % 30, [x, y] = sun(j, 30, 1);
        return D(CX + (p - 2) * 168 + x * 70, CY - 120 + Math.abs(p - 2) * 26 + y * 40, 7.5, 1, cols.acc); }
      const j = k - 150, f = (j / 25) | 0, m = j % 25, fx = CX + (f ? 175 : -175), fy = CY + 150, s = f ? 1 : -1;
      if (m < 18) { const [x, y] = sun(m, 18, 1); return D(fx + x * 85 * s, fy + y * 32, 6.5, .95, cols.ink); }
      const q = m - 18; return D(fx - s * (95 + (q % 2 ? 22 : 14) * (1 + (q >> 1) * .45)), fy + (q % 2 ? 1 : -1) * (8 + (q >> 1) * 11), 6, .95, cols.ink);
    },
    encolhe: (i, t, dt) => {
      const k = clamp((dt - .5) / 2.5);
      if (i < NP) { const [x, y] = sun(i, NP, 330); return D(CX + x, CY + y, 6, .45 * k, cols.ink); }
      const l = F.lanche(i), s = 1 - .75 * k; return D(CX + (l.x - CX) * s, CY + (l.y - CY) * s, l.r * (1 - .5 * k), 1, l.c);
    },
    mapa_peixe: (i, t) => { // lago pequeno com Magdala marcada
      if (i >= NP) { const a = (i - NP) / NB * 6.2832; return D(CX + Math.sin(a) * 200 * (1 + .12 * Math.cos(a)), CY - Math.cos(a) * 260, 4, .5, cols.muted); }
      if (i < 20) { const [x, y] = sun(i, 20, 16); return D(CX - 205 + x, CY - 70 + y, 5, 1, cols.acc); }
      return H(i);
    },
    grupos: (i, t, dt, o) => {
      if (i >= NP) { const k = i - NP, p = (k / 30) | 0; return D(CX + (p - 2) * 40, CY, 3, 0, cols.acc); }
      const b = i < 200 ? (i / 100) | 0 : 2 + (((i - 200) / 50) | 0), j = i < 200 ? i % 100 : (i - 200) % 50;
      const bx = CX + (b % 2 ? 175 : -175), by = b < 2 ? CY - 110 : CY + 175, cx = j % 10, cy = (j / 10) | 0;
      let c = cols.ink, r = 7;
      if (o.cor) c = mix(cols.ink, cols.acc, [0, .7, .35, 1][b] * clamp((dt - .5 - b * .4) / .6));
      if (o.comem) { const dd = Math.hypot(bx - CX, by - CY) / 400 + cx * .02 + cy * .02, k = clamp((dt - .8 - dd * 1.6) / .4); c = mix(cols.ink, cols.acc, k); r = 7 + Math.sin(k * Math.PI) * 4; }
      const x = bx + (cx - 4.5) * 25, y = by + (cy - (b < 2 ? 4.5 : 2)) * 25;
      if (o.apaga) return D(x, y, 6, .12, cols.acc);
      return D(x, y, r, .95, c);
    },
    partir: (i, t, dt) => {
      if (i < NP) return F.grupos(i, t, dt, { comem: 1 });
      const k = i - NP, alvo = F.grupos((k * 3) % NP, t, dt, {}), ok = clamp((dt - .6 - k * .012) / .7);
      return D(CX + (alvo.x + 9 - CX) * smooth(ok), CY + (alvo.y - 9 - CY) * smooth(ok), 4, ok > 0 ? 1 - .6 * ok : 0, cols.acc);
    },
    cestos: (i, t, dt) => {
      if (i < NP) return F.grupos(i, t, dt, { apaga: 1 });
      const k = i - NP, c = k % 12, j = (k / 12) | 0, [bx, by] = K12(c);
      return D(bx + ((j % 4) - 1.5) * 21, by + 30 - ((j / 4) | 0) * 20 - (j >= 16 ? 18 : 0), 8, 1, cols.acc);
    },
    eliseu: (i, t, dt, o) => {
      if (i < 100) { const cx = i % 10, cy = (i / 10) | 0; return D(CX - 230 + (cx - 4.5) * 20, CY + 120 + (cy - 4.5) * 20, 5.5, .9, cols.ink); }
      if (i < NP) { const [x, y] = sun(i - 100, 200, 170); return D(CX + 230 + x, CY + 120 + y, 4.5, clamp((dt - (o.t2 ?? 3)) / 1), cols.ink); }
      const k = i - NP;
      if (k < 20) { const [x, y] = sun(k, 20, 38); return D(CX - 230 + x, CY - 170 + y, 8, 1, cols.acc); }
      if (k < 170) { const p = ((k - 20) / 30) | 0, j = (k - 20) % 30, [x, y] = sun(j, 30, 1); return D(CX + 230 + (p - 2) * 52 + x * 22, CY - 170 + y * 14, 4.5, clamp((dt - (o.t2 ?? 3)) / 1), cols.acc); }
      return H(i);
    },
    sete: (i, t, dt) => { // 4 mil (80 pontos) e 7 cestos grandes
      if (i < 80) { const [x, y] = sun(i, 80, 150); return D(CX + x, CY - 150 + y, 7, .9, cols.ink); }
      if (i < NP) return H(i);
      const k = i - NP; if (k >= 175) return H(i);
      const c = k % 7, j = (k / 7) | 0, [bx, by] = K7(c);
      return D(bx + ((j % 5) - 2) * 17, by + 50 - ((j / 5) | 0) * 18, 7, clamp((dt - 1.5 - c * .25) / .5), cols.acc);
    },
    compara: (i, t, dt, o) => { // kófinos (pequeno, esquerda) e spyrís (grande, direita)
      if (i < NP) {
        if (o.pessoa && i < 26) { // bonequinho dentro do cesto grande
          const pts = [[0, -170], [0, -150], ...[...Array(7)].map((_, k) => [0, -130 + k * 14]), ...[...Array(5)].map((_, k) => [-14 - k * 9, -110 + k * 9]), ...[...Array(5)].map((_, k) => [14 + k * 9, -110 + k * 9]), ...[...Array(4)].map((_, k) => [-6 - k * 4, -30 + k * 12]), ...[...Array(4)].map((_, k) => [6 + k * 4, -30 + k * 12])];
          const [x, y] = pts[i] || [0, 0]; return D(CX + 190 + x, CY + 60 + y + (o.desce ? Math.min(140, (dt - 1) * 30) : 0), i < 2 ? 9 : 5.5, clamp((dt - .8) / .5), cols.ink);
        }
        return H(i);
      }
      const k = i - NP;
      if (k < 16) return D(CX - 230 + ((k % 4) - 1.5) * 18, CY + 120 - ((k / 4) | 0) * 17, 7, 1, cols.acc);
      if (k < 100) { const j = k - 16; return D(CX + 190 + ((j % 12) - 5.5) * 20, CY + 150 - ((j / 12) | 0) * 19, 7, o.pessoa ? .35 : 1, cols.acc); }
      return H(i);
    },
    regioes: (i, t, dt) => {
      if (i < 150) { const [x, y] = sun(i, 150, 150); return D(CX - 220 + x, CY + 60 + y, 5, .8, cols.ink); }
      if (i < NP) { const [x, y] = sun(i - 150, 150, 150); return D(CX + 220 + x, CY + 60 + y, 5, .8, mix(cols.ink, cols.acc, .4)); }
      const k = i - NP;
      if (k < 12) return D(CX - 220 + ((k % 6) - 2.5) * 34, CY - 170 + ((k / 6) | 0) * 34, 10, clamp((dt - 3) / .5), cols.acc);
      if (k < 19) return D(CX + 220 + ((k - 12) - 3) * 34, CY - 155, 10, clamp((dt - 5) / .5), cols.acc);
      return H(i);
    },
    rei: (i, t, dt) => {
      if (i >= NP) { if (i > NP) return H(i); const u = smooth((dt - 3) / 3); return D(CX, CY - 40 - 380 * u, 13, 1, cols.acc); }
      const [x, y] = sun(i, NP, 300), u = smooth((dt - .5) / 2.5) * .45, f = smooth((dt - 3) / 3);
      return D(CX + x * (1 - u), CY + y * (1 - u) - 60 * f * (1 - Math.hypot(x, y) / 300), 6, .85, cols.ink);
    },
    mana: (i, t) => {
      if (i < NP) { const cx = i % 30, cy = (i / 30) | 0; return D(CX - 435 + cx * 30, CY + 230 + cy * 9, 4, .5, cols.ink); }
      const Hh = 620, y = CY - 380 + ((t * 120 * P[i].v + P[i].d * Hh) % Hh);
      return D(CX - 430 + P[i].d * 860 + Math.sin(t + P[i].ph) * 8, y, 4.5, .85 * Math.sin(Math.PI * (y - CY + 380) / Hh), cols.acc);
    },
    luz: (i, t, dt, o) => { const [x, y] = sun(i % 60, 60, (o.R || 30) + Math.sin(t * 2) * 4); return D(CX + x, CY - 40 + y, 4, i < 60 ? 1 : 0, cols.acc); },
    afasta: (i, t, dt, o) => {
      if (i >= NP) return H(i, CX, CY - 40);
      if (i < 12) { const a = i / 12 * 6.2832; return D(CX + Math.cos(a) * 70, CY - 40 + Math.sin(a) * 70, 9, 1, cols.acc); }
      const [x, y] = sun(i, NP, 300), u = o.ja ? 1 : smooth((dt - .8 - P[i].d * 2) / 3), R = 1 + 1.4 * u;
      return D(CX + x * R, CY - 40 + y * R, 6, .85 * (1 - u), cols.ink);
    },
    sobe: (i, t, dt, o) => {
      const v = o.forte ? 260 : 70, Hh = 900, y = 1560 - ((t * v * P[i].v + P[i].d * Hh) % Hh);
      const sub = (1560 - y) / Hh, x = o.forte ? CX + P[i].dir * (60 + 420 * sub) + Math.sin(t + P[i].ph) * 12 : P[i].sx + Math.sin(t * .5 + P[i].ph) * 20;
      return D(x, y, o.forte ? 5 + P[i].d * 4 : 4, (o.forte ? .9 : .45) * Math.sin(Math.PI * sub), i % 3 ? cols.acc : cols.ink);
    },
    explode: (i, t, dt) => { const a = i * 2.39996, R = 40 + 900 * (1 - Math.exp(-dt * 1.4)) * (.4 + P[i].d * .6);
      return D(CX + Math.cos(a) * R, CY - 40 + Math.sin(a) * R * 1.2, 4 + P[i].d * 5, clamp(1 - dt / 3.2) * .95, i % 2 ? cols.acc : cols.ink); },
  };
  // preco: versão limpa
  F.preco = (i) => {
    if (i < NP) return H(i);
    const k = i - NP; if (k >= 160) return H(i);
    const g = (k / 40) | 0, j = k % 40, [x, y] = sun(j, 40, 62), gx = g === 0 ? CX + 20 : CX + 20 + (g - 1) * 160, gy = g === 0 ? CY - 150 : CY + 150;
    return D(gx + x, gy + y, 7, 1, g === 0 ? cols.ink : cols.acc);
  };

  const estado = (k, i, t) => { const c = TL[k]; return F[c.form](i, t, t - c.t, c.o || {}); };
  const cesto = (bx, by, w, h) => { ctx.beginPath(); ctx.moveTo(bx - w, by - h); ctx.lineTo(bx - w * .8, by + h * .8); ctx.quadraticCurveTo(bx, by + h, bx + w * .8, by + h * .8); ctx.lineTo(bx + w, by - h); ctx.stroke(); };
  const fmt = n => Math.round(n).toLocaleString('pt-BR');

  return {
    init(cena, R) {
      TL = R.cenas16; CNT = R.cnt || [];
      const cs = getComputedStyle(document.body), g = v => hex(cs.getPropertyValue(v));
      cols = { ink: g('--ink'), acc: R.acento ? hex(R.acento) : g('--acc'), muted: g('--ring') };
      cv = document.createElement('canvas'); cv.width = 1920; cv.height = 1080; cv.style.cssText = 'position:absolute;left:0;top:0'; cena.appendChild(cv); ctx = cv.getContext('2d');
      for (const o of R.ov || []) { const d = document.createElement('div'); d.style.cssText = 'position:absolute;text-align:center;' + o.css; d.innerHTML = o.html; cena.appendChild(d); OV.push({ ...o, d }); }
      this.cnt = document.createElement('div'); this.cnt.style.cssText = 'position:absolute;left:930px;width:900px;top:150px;text-align:center;font:900 110px M;color:var(--acc);line-height:1'; cena.appendChild(this.cnt);
      this.leg = document.createElement('div'); this.leg.style.cssText = 'position:absolute;left:930px;width:900px;top:270px;text-align:center;font:700 22px J,monospace;letter-spacing:4px;color:var(--sub)'; cena.appendChild(this.leg);
    },
    render(t) {
      ctx.clearRect(0, 0, 1920, 1080);
      const vis = window.__visivel ?? 1; cv.style.opacity = vis;
      let k = 0; for (let j = 0; j < TL.length; j++) if (t >= TL[j].t - .25) k = j;
      const t0 = TL[k].t - .25, Dd = TL[k].D ?? 1.2, sem = TL[k].D === 0;
      ctx.save(); ctx.translate(SX, SY); ctx.scale(S, S); ctx.translate(-CX, -CY);
      // contornos de cestos
      for (const c of TL) if (c.cesto) {
        const a = io(t, c.t, c.fim, .6, .5); if (a <= 0) continue;
        ctx.globalAlpha = a; ctx.strokeStyle = `rgb(${cols.ink})`; ctx.lineWidth = 5; ctx.lineCap = 'round';
        if (c.cesto === 'k12') for (let q = 0; q < 12; q++) { const [bx, by] = K12(q); cesto(bx, by, 58, 60); }
        if (c.cesto === 's7') for (let q = 0; q < 7; q++) { const [bx, by] = K7(q); cesto(bx, by + 10, 52, 75); }
        if (c.cesto === 'cmp') { cesto(CX - 230, CY + 80, 50, 55); cesto(CX + 190, CY + 70, 135, 120); }
      }
      ctx.globalAlpha = 1;
      // brilho
      const gl = TL.find(c => c.o?.glow && t >= c.t - .3 && t < c.fim);
      if (gl) { const kp = io(t, gl.t, gl.fim, 1, .4), R0 = gl.o.glow; const g = ctx.createRadialGradient(CX, CY - 40, 0, CX, CY - 40, R0);
        g.addColorStop(0, `rgba(${cols.acc},${.45 * kp})`); g.addColorStop(1, `rgba(${cols.acc},0)`); ctx.fillStyle = g; ctx.fillRect(CX - R0, CY - 40 - R0, 2 * R0, 2 * R0); }
      for (let i = 0; i < N; i++) {
        const b = estado(k, i, t), p = k && !sem ? smooth((t - t0 - P[i].d * .5) / Dd) : 1;
        let s = b; if (p < 1) { const a = estado(k - 1, i, t); s = { x: a.x + (b.x - a.x) * p, y: a.y + (b.y - a.y) * p, r: a.r + (b.r - a.r) * p, a: a.a + (b.a - a.a) * p, c: mix(a.c, b.c, p), sq: a.sq + (b.sq - a.sq) * p }; }
        if (s.a <= .01) continue;
        ctx.globalAlpha = clamp(s.a); ctx.fillStyle = `rgb(${s.c.map(Math.round)})`; ctx.beginPath();
        if (s.sq > .02) ctx.roundRect(s.x - s.r, s.y - s.r, s.r * 2, s.r * 2, s.r * (1 - .75 * s.sq)); else ctx.arc(s.x, s.y, s.r, 0, 6.2832);
        ctx.fill();
      }
      ctx.restore(); ctx.globalAlpha = 1;
      OV.forEach(o => { const v = Math.min(io(t, o.a, o.b, .35, .25), vis); o.d.style.display = v > 0 ? 'block' : 'none'; if (v > 0) blur(o.d, v, 10); });
      let c = null; for (const x of CNT) if (t >= x.a && t < x.b) c = x;
      if (c) { const v = c.de + (c.para - c.de) * (1 - Math.pow(1 - clamp((t - c.a) / c.dur), 3)); this.cnt.textContent = (c.pre || '') + fmt(v); this.leg.textContent = c.leg;
        const k2 = Math.min(io(t, c.a, c.b, .3, .25), vis); blur(this.cnt, k2, 14); blur(this.leg, k2, 8); }
      else { this.cnt.style.opacity = 0; this.leg.style.opacity = 0; }
    }
  };
})();

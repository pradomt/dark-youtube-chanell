// Short "Cinco pães" · visual de partículas no palco aberto (sem cartão).
// Cada ponto muda de formação no tempo da frase: multidão, calendário de 200 dias, pães e peixes, grupos, cestos, chuva de abundância.
// Determinístico: mesmo t = mesmo quadro (o render tira print quadro a quadro).
window.EXTRA = (() => {
  const NP = 300, NB = 200, N = NP + NB, CX = 540, CY = 1110;
  let cv, ctx, F, cols, ov = [];
  // gerador pseudoaleatório com semente fixa
  let sd = 7; const rnd = () => (sd = (sd * 16807) % 2147483647) / 2147483647;
  const P = Array.from({ length: N }, () => ({ ph: rnd() * 6.28, w: .6 + rnd() * .9, d: rnd(), sx: 90 + rnd() * 900, sy: 720 + rnd() * 760, v: .5 + rnd(), dir: rnd() * 2 - 1 }));
  const smooth = x => { x = clamp(x); return x * x * (3 - 2 * x); };
  const sun = (k, n, R) => { const r = R * Math.sqrt((k + .5) / n), a = k * 2.39996; return [Math.cos(a) * r, Math.sin(a) * r]; };
  const hex = h => [1, 3, 5].map(i => parseInt(h.trim().slice(i, i + 2), 16));
  const mix = (a, b, k) => a.map((v, i) => v + (b[i] - v) * k);
  const hid = (i) => ({ x: P[i].sx, y: P[i].sy, r: 3, a: 0, c: cols.ink, sq: 0 });

  // ---------- formações: f(i, t, dt) devolve {x, y, r, a, c, sq} ----------
  const pessoaOuOculto = (i, fn) => i < NP ? fn(i) : null;
  const FORM = {
    poeira: (i, t) => ({ x: P[i].sx + Math.sin(t * .4 * P[i].w + P[i].ph) * 30, y: P[i].sy + Math.cos(t * .3 * P[i].w + P[i].ph) * 30, r: 3, a: i < NP ? .35 : 0, c: cols.ink, sq: 0 }),
    calendario: (i, t, dt, o = {}) => {
      if (i < NP) return { ...hid(i), x: P[i].sx, y: P[i].sy };
      const k = i - NP, cx = k % 20, cy = (k / 20) | 0, lit = o.acende ? clamp((dt - o.acende[0] - k * o.acende[1] / NB) / .25) : 1;
      return { x: CX - 390 + cx * 41, y: CY - 190 + cy * 41, r: 15, a: .25 + .75 * lit, c: mix(cols.muted, cols.acc, lit), sq: 1 };
    },
    multidao: (i, t, dt, o) => {
      if (i >= NP) return { ...hid(i), x: CX, y: CY };
      const n = o.n, on = i < n, [x, y] = sun(i, on ? n : NP, o.R);
      return { x: CX + x + Math.sin(t * .8 * P[i].w + P[i].ph) * 3, y: CY + y + Math.cos(t * .7 * P[i].w + P[i].ph) * 3, r: 7, a: on ? .9 : 0, c: i < 100 ? cols.ink : mix(cols.ink, cols.acc, .35), sq: 0 };
    },
    divide: (i, t, dt) => {
      const [x, y] = sun(i < NP ? i : i - NP, NP, 300);
      if (i < NP) return { x: CX + x, y: CY + y, r: 7, a: i < NB ? .9 : .3, c: cols.ink, sq: 0 };
      return { x: CX + x + 8, y: CY + y - 8, r: 3.5, a: 1, c: cols.acc, sq: 0 };
    },
    lanche: (i) => {
      if (i < NP) { const [x, y] = sun(i, NP, 300); return { x: CX + x, y: CY + y, r: 4, a: 0, c: cols.ink, sq: 0 }; }
      const k = i - NP;
      if (k < 150) { const p = (k / 30) | 0, j = k % 30, [x, y] = sun(j, 30, 1); // 5 pães em arco
        const px = CX + (p - 2) * 168, py = CY - 120 + Math.abs(p - 2) * 26;
        return { x: px + x * 70, y: py + y * 40, r: 7.5, a: 1, c: cols.acc, sq: 0 }; }
      const j = k - 150, f = (j / 25) | 0, m = j % 25, fx = CX + (f ? 175 : -175), fy = CY + 150, s = f ? 1 : -1;
      if (m < 18) { const [x, y] = sun(m, 18, 1); return { x: fx + x * 85 * s, y: fy + y * 32, r: 6.5, a: .95, c: cols.ink, sq: 0 }; }
      const q = m - 18; return { x: fx - s * (95 + (q % 2 ? 22 : 14) * (1 + (q >> 1) * .45)), y: fy + (q % 2 ? 1 : -1) * (8 + (q >> 1) * 11), r: 6, a: .95, c: cols.ink, sq: 0 };
    },
    preco: (i) => {
      if (i < NP) return { x: CX, y: CY, r: 3, a: 0, c: cols.ink, sq: 0 };
      const k = i - NP; if (k >= 160) return { x: CX, y: CY, r: 3, a: 0, c: cols.acc, sq: 0 };
      const g = (k / 40) | 0, j = k % 40, [x, y] = sun(j, 40, 62);
      const gx = g === 0 ? CX + 20 : CX + 20 + (g - 1) * 160, gy = g === 0 ? CY - 150 : CY + 150;
      return { x: gx + x, y: gy + y, r: 7, a: 1, c: g === 0 ? cols.ink : cols.acc, sq: 0 };
    },
    grupos: (i, t, dt, o = {}) => {
      if (i >= NP) { const k = i - NP, p = (k / 30) | 0; return { x: CX + (p - 2) * 40, y: CY, r: 3, a: 0, c: cols.acc, sq: 0 }; }
      const b = i < 200 ? (i / 100) | 0 : 2 + (((i - 200) / 50) | 0), j = i < 200 ? i % 100 : (i - 200) % 50;
      const bx = CX + (b % 2 ? 175 : -175), by = b < 2 ? CY - 110 : CY + 175, cx = j % 10, cy = (j / 10) | 0;
      let c = cols.ink, r = 7;
      if (o.comem) { const dd = Math.hypot(bx - CX, by - CY) / 400 + cx * .02 + cy * .02, k = clamp((dt - .8 - dd * 1.6) / .4); c = mix(cols.ink, cols.acc, k); r = 7 + Math.sin(k * Math.PI) * 4; }
      if (o.apaga) return { x: bx + (cx - 4.5) * 25, y: by + (cy - (b < 2 ? 4.5 : 2)) * 25, r: 6, a: .12, c: cols.acc, sq: 0 };
      return { x: bx + (cx - 4.5) * 25, y: by + (cy - (b < 2 ? 4.5 : 2)) * 25, r, a: .95, c, sq: 0 };
    },
    partir: (i, t, dt) => { // o pão sai do centro e chega a cada grupo
      if (i < NP) return FORM.grupos(i, t, dt, { comem: 1 });
      const k = i - NP, alvo = FORM.grupos((k * 3) % NP, t, dt), ok = clamp((dt - .6 - k * .012) / .7);
      return { x: CX + (alvo.x + 9 - CX) * smooth(ok), y: CY + (alvo.y - 9 - CY) * smooth(ok), r: 4, a: ok > 0 ? 1 - .6 * ok : 0, c: cols.acc, sq: 0 };
    },
    cestos: (i, t, dt) => {
      if (i < NP) return FORM.grupos(i, t, dt, { apaga: 1 });
      const k = i - NP, c = k % 12, j = (k / 12) | 0, bx = CX + ((c % 6) - 2.5) * 150, by = c < 6 ? CY - 60 : CY + 200;
      return { x: bx + ((j % 4) - 1.5) * 21 + (j >= 16 ? 0 : 0), y: by + 30 - ((j / 4) | 0) * 20 - (j >= 16 ? 18 : 0), r: 8, a: 1, c: cols.acc, sq: 0 };
    },
    sobe: (i, t, dt, o) => { // partículas subindo devagar (grego) ou em fonte (abundância)
      const v = o.forte ? 260 : 70, H = 900, y = 1560 - ((t * v * P[i].v + P[i].d * H) % H);
      const sub = (1560 - y) / H, x = o.forte ? CX + P[i].dir * (60 + 420 * sub) + Math.sin(t + P[i].ph) * 12 : P[i].sx + Math.sin(t * .5 + P[i].ph) * 20;
      return { x, y, r: o.forte ? 5 + P[i].d * 4 : 4, a: (o.forte ? .9 : .45) * Math.sin(Math.PI * sub), c: i % 3 ? cols.acc : cols.ink, sq: 0 };
    },
    ponto: (i, t) => { const [x, y] = sun(i % 40, 40, 14 + Math.sin(t * 3) * 3); return { x: CX + x, y: CY - 40 + y, r: 3.5, a: i < 40 ? 1 : .25, c: cols.acc, sq: 0 }; },
    explode: (i, t, dt) => { const a = i * 2.39996, R = 40 + 900 * (1 - Math.exp(-dt * 1.4)) * (.4 + P[i].d * .6);
      return { x: CX + Math.cos(a) * R, y: CY - 40 + Math.sin(a) * R * 1.2, r: 4 + P[i].d * 5, a: clamp(1 - dt / 3.2) * .95, c: i % 2 ? cols.acc : cols.ink, sq: 0 }; },
  };

  // linha do tempo: [frase, formação, opções, duração da transição]
  const TL = () => [
    [-1, 'poeira'], [0, 'calendario', {}, 1.6], [1, 'multidao', { n: 100, R: 170 }], [2, 'multidao', { n: 300, R: 300 }],
    [3, 'calendario', { acende: [.3, 6.0] }], [5, 'divide'], [6, 'lanche'], [7, 'preco'], [8, 'grupos', {}, 1.0], [9, 'partir'],
    [10, 'cestos', {}, 1.6], [12, 'sobe', {}], [13, 'sobe', { forte: 1 }], [14, 'ponto', {}, 1.4], [16, 'explode', {}, .01]];

  function estado(k, i, t) { const [f, nome, o] = TL_[k]; return FORM[nome](i, t, t - (f < 0 ? 0 : F[f]), o || {}); }
  let TL_;

  // ---------- textos sobre o palco (referência bíblica, contador, nota) ----------
  const el = (css, html = '') => { const d = document.createElement('div'); d.style.cssText = 'position:absolute;left:0;right:0;text-align:center;' + css; d.innerHTML = html; cv.parentNode.appendChild(d); return d; };
  const fmt = n => Math.round(n).toLocaleString('pt-BR');

  return {
    init(cena, R) {
      F = R.frases; TL_ = TL();
      const cs = getComputedStyle(document.body), g = v => hex(cs.getPropertyValue(v));
      cols = { ink: g('--ink'), acc: R.acento ? hex(R.acento) : g('--acc'), muted: g('--ring') };
      cv = document.createElement('canvas'); cv.width = 1080; cv.height = 1920; cv.style.cssText = 'position:absolute;left:0;top:0'; cena.appendChild(cv); ctx = cv.getContext('2d');
      const refs = [[0, 'JOÃO 6:7 · MATEUS 20:2'], [1, 'MATEUS 14:21'], [2, 'ESTIMATIVA'], [3, 'JOÃO 6:7'], [4, 'MATEUS 20:2'], [5, 'JOÃO 6:7'], [6, 'JOÃO 6:9'],
        [7, 'APOCALIPSE 6:6'], [8, 'MARCOS 6:39-40'], [9, 'MARCOS 6:41-42'], [10, 'JOÃO 6:12 · PARÁFRASE'], [11, 'JOÃO 6:13'], [12, 'JOÃO 6:12 · JOÃO 10:10'], [13, 'JOÃO 10:10 · PARÁFRASE']];
      refs.forEach(([f, s], j) => ov.push({ d: el('top:690px;font:700 30px J,monospace;letter-spacing:5px;color:var(--acc)', s), a: F[f] - .2, b: (refs[j + 1] ? F[refs[j + 1][0]] : F[14]) - .15 }));
      const notas = [[0, 1, 'CADA QUADRADO: 1 DIA DE TRABALHO'], [1, 3, 'CADA PONTO: 50 PESSOAS'], [3, 5, 'CADA QUADRADO: 1 DENÁRIO = 1 DIA DE TRABALHO'],
        [5, 6, '200 DENÁRIOS DE PÃO · 15 MIL BOCAS'], [6, 7, 'O LANCHE DE UM MENINO'], [8, 10, 'CADA PONTO: 1 PESSOA'], [10, 12, 'O QUE SOBROU']];
      notas.forEach(([a, b, s]) => ov.push({ d: el('top:1650px;font:500 24px J,monospace;letter-spacing:3px;color:var(--muted)', s), a: F[a] + .3, b: F[b] - .15 }));
      // rótulos do preço e dos grupos
      ov.push({ d: el('top:850px;font:700 26px J,monospace;letter-spacing:4px;color:var(--sub)', '1 DENÁRIO COMPRAVA'), a: F[7] + .4, b: F[8] - .15 });
      ov.push({ d: el(`top:${CY - 172}px;left:90px;right:auto;font:800 36px M;color:var(--ink)`, '1 de trigo'), a: F[7] + .7, b: F[8] - .15 });
      ov.push({ d: el(`top:${CY + 128}px;left:90px;right:auto;font:800 36px M;color:var(--acc)`, '3 de cevada'), a: F[7] + 1.4, b: F[8] - .15 });
      [['100', -175, -110 + 140], ['100', 175, -110 + 140], ['50', -175, 175 + 80], ['50', 175, 175 + 80]].forEach(([s, dx, dy], j) =>
        ov.push({ d: el(`top:${CY + dy - 18}px;left:${CX + dx - 100}px;right:auto;width:200px;font:700 26px J,monospace;color:var(--muted)`, s), a: F[8] + 1 + j * .25, b: F[9] + .5 }));
      // cestos (contorno desenhado no canvas) e grego
      ov.push({ d: el('top:900px;font:800 120px "DejaVu Sans",sans-serif;color:var(--ink);letter-spacing:2px', '<span style="color:var(--acc)">περισσ</span>εύω'), a: F[12] + .4, b: F[14] - .15 });
      ov.push({ d: el('top:1050px;font:700 30px J,monospace;letter-spacing:4px;color:var(--sub)', 'SOBRAR · JOÃO 6:12'), a: F[12] + .6, b: F[14] - .15 });
      ov.push({ d: el('top:1160px;font:800 120px "DejaVu Sans",sans-serif;color:var(--ink);letter-spacing:2px', '<span style="color:var(--acc)">περισσ</span>όν'), a: F[12] + 2.0, b: F[14] - .15 });
      ov.push({ d: el('top:1310px;font:700 30px J,monospace;letter-spacing:4px;color:var(--sub)', 'ABUNDÂNCIA · JOÃO 10:10'), a: F[12] + 2.2, b: F[14] - .15 });
      ov.push({ d: el('top:1130px;left:140px;right:140px;font:500 24px/1.6 J,monospace;color:var(--muted)', 'Mateus 14:13-21 · Marcos 6:30-44 · João 6:1-13<br>João 10:10 · Mateus 20:2 · Apocalipse 6:6<br>Citações em paráfrase. 15 mil pessoas é estimativa:<br>o texto conta 5 mil homens, sem mulheres e crianças.'), a: R.chamada.a + .8, b: 999 });
      // contador grande
      this.cnt = el('top:1440px;font:900 150px M;color:var(--acc);line-height:1'); this.leg = el('top:1600px;font:700 26px J,monospace;letter-spacing:4px;color:var(--sub)');
      this.C = [[F[1] + .2, F[2] - .1, 0, 5000, 1.6, '', 'HOMENS'], [F[2] - .1, F[3] - .15, 5000, 15000, 1.8, '~', 'PESSOAS · ESTIMATIVA'],
        [F[3] + .3, F[5] - .15, 0, 200, 6.0, '', 'DIAS DE TRABALHO'], [F[11] - .1, F[12] - .15, 0, 12, .8, '', 'CESTOS CHEIOS']];
    },
    render(t) {
      ctx.clearRect(0, 0, 1080, 1920);
      // formação atual e anterior, com atraso por partícula (fluxo orgânico)
      let k = 0; for (let j = 0; j < TL_.length; j++) if (TL_[j][0] < 0 || t >= F[TL_[j][0]] - .25) k = j;
      const t0 = TL_[k][0] < 0 ? -99 : F[TL_[k][0]] - .25, D = TL_[k][3] ?? 1.2;
      // cestos: contorno
      const kc = Math.min(io(t, F[10] + .2, F[12] - .2, .6, .5), 1);
      if (kc > 0) { ctx.save(); ctx.globalAlpha = kc; ctx.strokeStyle = `rgb(${cols.ink})`; ctx.lineWidth = 5; ctx.lineCap = 'round';
        for (let c = 0; c < 12; c++) { const bx = CX + ((c % 6) - 2.5) * 150, by = c < 6 ? CY - 60 : CY + 200;
          ctx.beginPath(); ctx.moveTo(bx - 58, by - 60); ctx.lineTo(bx - 46, by + 48); ctx.quadraticCurveTo(bx, by + 60, bx + 46, by + 48); ctx.lineTo(bx + 58, by - 60); ctx.stroke(); }
        ctx.restore(); }
      for (let i = 0; i < N; i++) {
        const b = estado(k, i, t), dl = (TL_[k][0] === 16 ? 0 : P[i].d * .5), p = k ? smooth((t - t0 - dl) / D) : 1;
        let s = b; if (p < 1) { const a = estado(k - 1, i, t); s = { x: a.x + (b.x - a.x) * p, y: a.y + (b.y - a.y) * p, r: a.r + (b.r - a.r) * p, a: a.a + (b.a - a.a) * p, c: mix(a.c, b.c, p), sq: a.sq + (b.sq - a.sq) * p }; }
        if (s.a <= .01) continue;
        ctx.globalAlpha = clamp(s.a); ctx.fillStyle = `rgb(${s.c.map(Math.round)})`; ctx.beginPath();
        if (s.sq > .02) ctx.roundRect(s.x - s.r, s.y - s.r, s.r * 2, s.r * 2, s.r * (1 - .75 * s.sq)); else ctx.arc(s.x, s.y, s.r, 0, 6.2832);
        ctx.fill();
      }
      ctx.globalAlpha = 1;
      // brilho do ponto final
      const kp = io(t, F[14], F[16] + .2, 1, .3);
      if (kp > 0) { const g = ctx.createRadialGradient(CX, CY - 40, 0, CX, CY - 40, 220); g.addColorStop(0, `rgba(${cols.acc},${.45 * kp})`); g.addColorStop(1, `rgba(${cols.acc},0)`); ctx.fillStyle = g; ctx.fillRect(CX - 220, CY - 260, 440, 440); }
      ov.forEach(o => { const v = io(t, o.a, o.b, .35, .25); o.d.style.display = v > 0 ? 'block' : 'none'; if (v > 0) blur(o.d, v, 10); });
      let cv_ = null; for (const c of this.C) if (t >= c[0] && t < c[1]) cv_ = c;
      if (cv_) { const [a, b, de, para, dur, pre, leg] = cv_, v = de + (para - de) * (1 - Math.pow(1 - clamp((t - a) / dur), 3));
        this.cnt.textContent = pre + fmt(v); this.leg.textContent = leg; const k2 = io(t, a, b, .3, .25); blur(this.cnt, k2, 14); blur(this.leg, k2, 8); }
      else { this.cnt.style.opacity = 0; this.leg.style.opacity = 0; }
    }
  };
})();

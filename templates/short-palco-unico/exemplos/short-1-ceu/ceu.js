// Painel "extra" do Short 1: carta celeste desenhada a partir de ceu.json (dados do ceu.py).
// Estrelas acendem por brilho, céu clareia com o Sol subindo a 44°, estrelas somem, depois o mapa se espelha.
window.EXTRA = (() => {
  const D = window.__DADOS, ST = D.stars, NAMES = Object.keys(ST), SC = 330, $ = id => document.getElementById(id);
  const CONST = ['Cruzeiro do Sul', 'Escorpião', 'Cão Maior'];
  const Rr = m => Math.max(4, 10.5 - 1.6 * m);
  const RANK = {}; NAMES.map((n, i) => i).sort((a, b) => ST[NAMES[a]].m - ST[NAMES[b]].m).forEach((i, k) => RANK[i] = k);
  const VB = 'viewBox="-460 -260 920 520"';
  function init(el) {
    let s = '<g>';
    D.lines.forEach((l, i) => s += `<line id="l${i}" stroke="var(--cline)" stroke-width="3" stroke-linecap="round"/>`);
    NAMES.forEach((n, i) => s += `<circle id="s${i}" r="${Rr(ST[n].m)}" fill="var(--star)"/>`);
    CONST.forEach((c, i) => s += `<text id="c${i}" text-anchor="middle" font-family="J" font-weight="700" font-size="22" letter-spacing="2" fill="${i ? 'var(--muted)' : 'var(--acc)'}">${c.toUpperCase()}</text>`);
    el.innerHTML = `<svg style="position:absolute;inset:0" ${VB}>${s}</g></svg>
      <div id="dia" style="position:absolute;inset:0;opacity:0;background:linear-gradient(180deg,var(--day),#f7e9c9)"></div>
      <svg style="position:absolute;inset:0" ${VB}><g id="sol"><circle r="34" fill="#ffcf4a"/><circle r="56" fill="#ffcf4a" opacity=".25"/>
        <text id="solt" x="70" y="12" font-family="J" font-weight="800" font-size="34" fill="#141414"></text></g></svg>
      <div id="cnt" style="position:absolute;right:40px;top:20px;font:800 40px J,monospace;color:var(--ink)"></div>`;
    if (document.body.classList.contains('noite')) $('dia').style.background = 'linear-gradient(180deg,#3d7cc7,#a9cbe8)';
  }
  function render(t) {
    const mir = ease((t - 22.0) / 1.2);
    const pos = n => { const s = ST[n], f = 1 - 2 * mir; return [(s.x * f - 0.2 * f) * SC, -(s.y + .2) * SC]; };
    const sunUp = ease((t - 13.6) / 2.2), fade = clamp((t - 17.6) / 2.2), back = ease((t - 20.6) / .6);
    const noite = 1 - sunUp * (1 - back);
    $('dia').style.opacity = sunUp * .9 * (1 - back);
    NAMES.forEach((n, i) => {
      const c = $('s' + i), [x, y] = pos(n), app = ease((t - 4.5 - RANK[i] * .045) / .3);
      const gone = clamp(fade * 36 - (35 - RANK[i]));
      c.setAttribute('cx', x); c.setAttribute('cy', y);
      c.setAttribute('opacity', app * (1 - gone * (1 - back)) * (1 - .55 * (1 - noite)));
      c.setAttribute('fill', ST[n].c === 'Cruzeiro do Sul' && t > 20.6 ? 'var(--acc)' : 'var(--star)');
    });
    D.lines.forEach(([a, b], i) => {
      const l = $('l' + i), [x1, y1] = pos(a), [x2, y2] = pos(b), k = ease((t - 5.3 - i * .05) / .4);
      l.setAttribute('x1', x1); l.setAttribute('y1', y1); l.setAttribute('x2', x1 + (x2 - x1) * k); l.setAttribute('y2', y1 + (y2 - y1) * k);
      l.setAttribute('opacity', (k > 0 ? .8 : 0) * (1 - .7 * (1 - noite)) * (1 - fade * (1 - back)));
    });
    CONST.forEach((c, i) => {
      let mx = 0, my = 0; const ss = NAMES.filter(n => ST[n].c === c);
      ss.forEach(n => { const [x, y] = pos(n); mx += x; my = Math.max(my, y); });
      const el = $('c' + i); el.setAttribute('x', clamp(mx / ss.length, -380, 380)); el.setAttribute('y', my + 44);
      el.setAttribute('opacity', ease((t - 6.0 - i * .15) / .4) * noite * (i && t > 20.6 ? .5 : 1));
    });
    const su = ease((t - 13.8) / 2.4), ang = su * 44;
    $('sol').setAttribute('transform', `translate(${-330 + su * 330},${230 - Math.sin(ang * Math.PI / 180) * 330})`);
    $('sol').setAttribute('opacity', clamp((t - 13.7) / .3) * (1 - back));
    $('solt').textContent = Math.round(ang) + '°';
    $('cnt').style.opacity = io(t, 17.4, 20.5, .3, .3); $('cnt').textContent = Math.round(27 * (1 - fade)) + '/27';
  }
  return { init, render };
})();

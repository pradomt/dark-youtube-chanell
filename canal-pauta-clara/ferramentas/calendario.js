// Extra do palco: folhinha de calendário com dias riscados, circulados ou preenchidos no tempo da fala.
// Lê R.calendario = [{a, b, mes: "JANEIRO 2027", inicio: 5 (0 = domingo), dias: 31, marcas: [{dia, t, tipo: "circulo"|"risco"|"cheio", nota}]}]
window.EXTRA = {
  init(area, R) {
    this.M = (R.calendario || []).map(m => {
      const d = document.createElement('div'); d.style.cssText = 'position:absolute;inset:0;padding:6px 40px';
      let h = `<div style="font:800 34px J,monospace;letter-spacing:4px;color:var(--ink);text-align:center;margin-bottom:10px">${m.mes}</div>`;
      h += '<div style="display:grid;grid-template-columns:repeat(7,1fr);gap:6px;text-align:center">';
      for (const s of ['D', 'S', 'T', 'Q', 'Q', 'S', 'S']) h += `<div style="font:700 22px J,monospace;color:var(--muted)">${s}</div>`;
      for (let i = 0; i < m.inicio; i++) h += '<div></div>';
      for (let n = 1; n <= m.dias; n++) h += `<div class="cd" data-d="${n}" style="position:relative;height:56px;line-height:56px;border-radius:14px;font:800 30px M,sans-serif;color:var(--sub)">${n}<i class="ri" style="position:absolute;left:18%;right:18%;top:50%;height:5px;background:var(--ink);transform-origin:left;transform:rotate(-20deg) scaleX(0)"></i><i class="ci" style="position:absolute;inset:-4px 10px;border:5px solid var(--acc);border-radius:50%;opacity:0"></i></div>`;
      h += '</div><div class="nt" style="text-align:center;margin-top:12px;font:700 26px J,monospace;color:var(--acc)"></div>';
      d.innerHTML = h; area.appendChild(d); return { m, d };
    });
  },
  render(t) {
    for (const { m, d } of this.M) {
      const k = io(t, m.a, m.b, .4, .35); d.style.opacity = k; d.style.display = k > 0 ? 'block' : 'none'; if (k <= 0) continue;
      let nota = '';
      for (const mk of m.marcas) {
        const c = d.querySelector(`[data-d="${mk.dia}"]`), p = ease((t - mk.t) / .45);
        if (t >= mk.t && mk.nota) nota = mk.nota;
        if (mk.tipo === 'risco') { c.querySelector('.ri').style.transform = `rotate(-20deg) scaleX(${p})`; c.style.opacity = 1 - .45 * p; }
        if (mk.tipo === 'circulo') { const ci = c.querySelector('.ci'); ci.style.opacity = p; ci.style.transform = `scale(${1.6 - .6 * p})`; if (p > 0) c.style.color = 'var(--ink)'; }
        if (mk.tipo === 'cheio') { c.style.background = p > 0 ? 'var(--acc)' : ''; c.style.color = p > 0 ? '#fff' : ''; c.style.transform = `scale(${1 + .25 * Math.sin(Math.PI * clamp(p))})`; }
      }
      d.querySelector('.nt').textContent = nota;
    }
  }
};

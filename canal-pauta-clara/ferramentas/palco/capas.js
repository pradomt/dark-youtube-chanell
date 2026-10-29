// Gera as capas: node capas.js capas.json   (lista de {saida, w, h, apoio, titulo, selo, tamanho})
const { chromium } = require('playwright'), fs = require('fs'), path = require('path');
const L = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
(async () => {
  const b = await chromium.launch();
  for (const C of L) {
    const pg = await b.newPage({ viewport: { width: C.w, height: C.h } });
    await pg.addInitScript(`window.__CAPA=${JSON.stringify(C)}`);
    await pg.goto('file://' + path.join(__dirname, 'capa.html')); await pg.evaluate(() => document.fonts.ready); await pg.evaluate(() => ajustar());
    for (let k = 0; k < 4; k++) { try { await pg.screenshot({ path: C.saida }); break; } catch (e) { await new Promise(r => setTimeout(r, 1500)); } }
    await pg.close(); console.log(C.saida);
  }
  await b.close();
})();

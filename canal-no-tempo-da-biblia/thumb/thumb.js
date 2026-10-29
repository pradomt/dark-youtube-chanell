const { chromium } = require('playwright');
(async () => { const T = JSON.parse(process.argv[2]), out = process.argv[3];
  const b = await chromium.launch(), pg = await b.newPage({ viewport: { width: 1280, height: 720 } });
  await pg.addInitScript(`window.__T=${JSON.stringify(T)}`); await pg.goto('file://' + __dirname + '/thumb.html');
  await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(300); await pg.screenshot({ path: out }); await b.close(); })();

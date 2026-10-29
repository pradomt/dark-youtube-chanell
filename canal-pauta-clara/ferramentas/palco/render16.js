// Grava o vídeo longo (palco-16x9.html). Uso: node render16.js roteiro.json saida.mp4 [--de 0 --ate 120] [--quadros 5,60]
// --de/--ate gravam só um trecho sem áudio (para gravar em paralelo e juntar depois).
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const args = process.argv.slice(2), opt = n => { const i = args.indexOf(n); return i < 0 ? null : args[i + 1]; };
const [rp, out] = args, FPS = 30, R = JSON.parse(fs.readFileSync(rp, 'utf8'));
(async () => {
  const b = await chromium.launch(), pg = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await pg.addInitScript(`window.__ROTEIRO=${JSON.stringify(R)};`);
  await pg.goto('file://' + path.join(__dirname, 'palco-16x9.html'));
  await pg.evaluate(() => document.fonts.ready);
  if (opt('--quadros')) {
    for (const t of opt('--quadros').split(',')) { await pg.evaluate(t => render(t), +t); await pg.screenshot({ path: `${out.replace(/\.mp4$/, '')}_${t}.png` }); }
    return b.close();
  }
  const de = +(opt('--de') || 0), ate = +(opt('--ate') || R.duracao);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const i0 = Math.round(de * FPS), i1 = Math.round(ate * FPS);
  for (let i = i0; i < i1; i++) {
    await pg.evaluate(t => render(t), i / FPS);
    if (!ff.stdin.write(await pg.screenshot({ type: 'jpeg', quality: 92 }))) await new Promise(r => ff.stdin.once('drain', r));
    if ((i - i0) % 900 === 0) console.log(`${out}: ${i - i0}/${i1 - i0}`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close(); console.log('pronto:', out);
})();

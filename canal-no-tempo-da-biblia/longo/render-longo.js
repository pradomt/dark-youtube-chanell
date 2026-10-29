// Grava um vídeo longo do template "palco único" 16:9. Divide o tempo em partes e grava em paralelo (um Chromium por parte).
// Uso: node render-longo.js roteiro.json saida.mp4 [--quadros 12,80.5] [--partes 4] [--fps 30]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), os = require('os'), { spawn, execFileSync } = require('child_process');
const args = process.argv.slice(2), opt = n => { const i = args.indexOf(n); return i < 0 ? null : args[i + 1]; };
const [roteiroPath, out] = args, base = path.dirname(path.resolve(roteiroPath));
const FPS = +(opt('--fps') || 30), PARTES = +(opt('--partes') || Math.max(1, os.cpus().length));
const R = JSON.parse(fs.readFileSync(roteiroPath, 'utf8'));
const abs = p => path.isAbsolute(p) ? p : path.join(base, p);
R.duracao = R.duracao || +execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', abs(R.audio)]).toString();
for (const c of R.cenas) if (c.painel.src) c.painel.src = 'file://' + abs(c.painel.src);

async function pagina() {
  const b = await chromium.launch(), pg = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await pg.addInitScript(`window.__ROTEIRO=${JSON.stringify(R)};`);
  await pg.goto('file://' + path.join(__dirname, 'palco-longo.html'));
  await pg.evaluate(() => document.fonts.ready);
  await pg.evaluate(() => Promise.all([...document.images].map(i => i.decode().catch(() => 0))));
  return { b, pg };
}
async function parte(i0, i1, arq) {
  const { b, pg } = await pagina();
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', arq], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = i0; i < i1; i++) {
    await pg.evaluate(t => render(t), i / FPS);
    if (!ff.stdin.write(await pg.screenshot({ type: 'jpeg', quality: 92 }))) await new Promise(r => ff.stdin.once('drain', r));
    if ((i - i0) % 900 === 0) console.log(`${path.basename(arq)}: ${i - i0}/${i1 - i0}`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close();
}
(async () => {
  const quadros = opt('--quadros');
  if (quadros) {
    const { b, pg } = await pagina();
    for (const t of quadros.split(',')) { await pg.evaluate(t => render(t), +t); await pg.screenshot({ path: `${out.replace(/\.mp4$/, '')}_${t}.png` }); }
    return b.close();
  }
  if (opt('--faixa')) { const [a, z, arq] = opt('--faixa').split(':'); return parte(+a, +z, arq); }
  const N = Math.ceil(R.duracao * FPS), tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'longo-')), segs = [];
  const procs = [];
  for (let k = 0; k < PARTES; k++) {
    const a = Math.floor(N * k / PARTES), z = Math.floor(N * (k + 1) / PARTES), arq = path.join(tmp, `p${k}.mp4`); segs.push(arq);
    procs.push(new Promise(r => spawn(process.execPath, [__filename, roteiroPath, out, '--fps', String(FPS), '--faixa', `${a}:${z}:${arq}`], { stdio: 'inherit' }).on('close', r)));
  }
  await Promise.all(procs);
  fs.writeFileSync(path.join(tmp, 'lista.txt'), segs.map(s => `file '${s}'`).join('\n'));
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', path.join(tmp, 'lista.txt'), '-i', abs(R.audio),
    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out]);
  console.log('pronto:', out);
})();

// Grava um Short do template "palco único": abre palco.html no Chromium, tira um print por quadro e manda para o FFmpeg.
// Uso: node render.js caminho/roteiro.json saida.mp4 [--tema papel|noite] [--quadros 2.5,8,20]
//   --quadros salva só PNGs desses instantes (para conferir o visual antes de gravar tudo).
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { spawn, execFileSync } = require('child_process');

const args = process.argv.slice(2), opt = n => { const i = args.indexOf(n); return i < 0 ? null : args[i + 1]; };
const [roteiroPath, out] = args, FPS = 30, base = path.dirname(path.resolve(roteiroPath));
const R = JSON.parse(fs.readFileSync(roteiroPath, 'utf8'));
const abs = p => path.isAbsolute(p) ? p : path.join(base, p);
if (opt('--tema')) R.tema = opt('--tema');
R.duracao = R.duracao || +execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', abs(R.audio)]).toString();
for (const p of R.cartao.paineis || []) if (p.src) p.src = 'file://' + abs(p.src);
const extra = R.extra ? fs.readFileSync(abs(R.extra), 'utf8') : '';
const dados = R.dados ? fs.readFileSync(abs(R.dados), 'utf8') : 'null';

(async () => {
  const b = await chromium.launch(), pg = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await pg.addInitScript(`window.__ROTEIRO=${JSON.stringify(R)};window.__DADOS=${dados};\n${extra}`);
  await pg.goto('file://' + path.join(__dirname, 'palco.html'));
  await pg.evaluate(() => document.fonts.ready);
  const quadros = opt('--quadros');
  if (quadros) {
    for (const t of quadros.split(',')) { await pg.evaluate(t => render(t), +t); await pg.screenshot({ path: `${out.replace(/\.mp4$/, '')}_${t}.png` }); }
    return b.close();
  }
  const som = R.audio ? ['-i', abs(R.audio)] : ['-f', 'lavfi', '-t', String(R.duracao), '-i', 'anullsrc=r=48000:cl=stereo'];  // sem áudio: silêncio
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', ...som,
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out],
    { stdio: ['pipe', 'inherit', 'inherit'] });
  const N = Math.ceil(R.duracao * FPS);
  for (let i = 0; i < N; i++) {
    await pg.evaluate(t => render(t), i / FPS);
    if (!ff.stdin.write(await pg.screenshot({ type: 'jpeg', quality: 93 }))) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 150 === 0) console.log(`${i}/${N} quadros`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close(); console.log('pronto:', out);
})();

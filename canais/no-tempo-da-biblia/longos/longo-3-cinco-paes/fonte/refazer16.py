import sys, json, numpy as np, soundfile as sf
sys.argv = ['x', 'texto_vox.txt', '/tmp/w/vtest/v3-h3-avo-sabio.wav', open('ref_text.txt').read().strip()]
src = open('narrar_vox.py').read().split("import os; os.makedirs")[0]
exec(src)
linhas = [l for l in open('texto_vox.txt', encoding='utf-8') if l.strip()]
for idx in [33]:
    fr = linhas[idx].rstrip('\n').split('|', 1)[1]
    melhor = (-1, None, '')
    for k in range(10):
        alvo = fr if k % 2 == 0 else fr.replace('cêst', 'cest')
        a = corta(m.generate(text=alvo, prompt_wav_path=ref, prompt_text=ref_text, reference_wav_path=ref, cfg_value=2.0, inference_timesteps=10).astype(np.float32))
        r, ouv = nota(a, fr)
        if 'sext' in ouv.lower() or 'test' in ouv.lower(): r -= .3
        print(idx, k, f'{r:.2f}', ouv, flush=True)
        if r > melhor[0]: melhor = (r, a, ouv)
        if r >= .95: break
    r, a, ouv = melhor
    sf.write(f'frases/{idx:03d}.wav', a, SR); json.dump({'nota': round(r, 2), 'ouvido': ouv}, open(f'frases/{idx:03d}.wav.json', 'w'), ensure_ascii=False)
print('FIM')

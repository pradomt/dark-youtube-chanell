"""Gera de novo frases específicas da narração (VoxCPM2) até a transcrição conter as palavras exigidas e emenda no narracao.wav.
Uso: python refazer_frases.py ref.wav "texto da ref" 'idx:palavra1,palavra2' ..."""
import sys, json, numpy as np, soundfile as sf, torch, librosa
torch.set_num_threads(4)
from voxcpm import VoxCPM
from faster_whisper import WhisperModel
ref, ref_text = sys.argv[1:3]; alvos = {int(a.split(':')[0]): a.split(':')[1].split(',') for a in sys.argv[3:]}
m = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False, optimize=False, device="cpu"); SR = m.tts_model.sample_rate
W = WhisperModel('small', device='cpu', compute_type='int8')
y, sr = sf.read('narracao.wav'); assert sr == SR; T = json.load(open('tempos.json'))
def corta(a):
    nz = np.where(np.abs(a) > 0.01)[0]; return a[max(0, nz[0] - int(.03 * SR)): nz[-1] + int(.08 * SR)]
for i in sorted(alvos, reverse=True):
    fr = T[i]['text']; ok = None
    for k in range(8):
        a = corta(m.generate(text=fr, reference_wav_path=ref, cfg_value=2.0, inference_timesteps=10).astype(np.float32))
        seg, _ = W.transcribe(librosa.resample(a, orig_sr=SR, target_sr=16000), language='pt'); ouv = ' '.join(x.text for x in seg).lower()
        print(i, k, ouv, flush=True)
        if all(p in ouv for p in alvos[i]): ok = a; break
    if ok is None: print('NÃO CONSEGUI', i); continue
    s, e = int(T[i]['start'] * SR), int(T[i]['end'] * SR); d = (len(ok) - (e - s)) / SR
    y = np.concatenate([y[:s], ok, y[e:]]); T[i]['end'] = round(T[i]['start'] + len(ok) / SR, 3)
    for x in T[i + 1:]: x['start'] = round(x['start'] + d, 3); x['end'] = round(x['end'] + d, 3)
sf.write('narracao.wav', y, SR); json.dump(T, open('tempos.json', 'w'), ensure_ascii=False, indent=1); print('ok')

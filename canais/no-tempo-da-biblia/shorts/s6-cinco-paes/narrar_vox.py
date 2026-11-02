"""Narra uma frase por linha ('pausa|texto') com VoxCPM2 clonando a voz de referência do canal.
Cada frase é conferida com faster-whisper; se a transcrição não bater, gera de novo (até 4 vezes) e fica com a melhor.
Uso: python narrar_vox.py texto.txt referencia.wav "texto falado na referência" """
import sys, json, re, difflib, unicodedata, numpy as np, soundfile as sf, torch, librosa
torch.set_num_threads(4)
from voxcpm import VoxCPM
from faster_whisper import WhisperModel
txt, ref, ref_text = sys.argv[1:4]
m = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False, optimize=False, device="cpu"); SR = m.tts_model.sample_rate
W = WhisperModel('small', device='cpu', compute_type='int8')
NUM = {'doze': '12', 'cinco': '5', 'dois': '2', 'cem': '100', 'cinquenta': '50', 'duzentos': '200', 'quinze': '15', 'seis': '6'}
def norm(s):
    s = unicodedata.normalize('NFD', s.lower()); s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = re.sub(r'[^a-z0-9 ]', ' ', s); w = [NUM.get(x, x) for x in s.split()]
    return ' '.join(re.sub(r'c(?=[ei])', 's', x) for x in w)  # cevada = sevada
def nota(a, alvo):
    y = librosa.resample(a, orig_sr=SR, target_sr=16000); seg, _ = W.transcribe(y, language='pt')
    ouv = ' '.join(x.text for x in seg); return difflib.SequenceMatcher(None, norm(ouv), norm(alvo)).ratio(), ouv
def corta(a):
    nz = np.where(np.abs(a) > 0.01)[0]; return a[max(0, nz[0] - int(.03 * SR)): nz[-1] + int(.08 * SR)]
parts = [np.zeros(int(SR * .35), np.float32)]; t = .35; T = []
for ln in [l for l in open(txt, encoding='utf-8') if l.strip()]:
    gap, fr = ln.rstrip('\n').split('|', 1)
    parts.append(np.zeros(int(SR * float(gap)), np.float32)); t += float(gap)
    melhor = (-1, None, '')
    for k in range(4):
        a = corta(m.generate(text=fr, prompt_wav_path=ref, prompt_text=ref_text, reference_wav_path=ref, cfg_value=2.0, inference_timesteps=10).astype(np.float32))
        r, ouv = nota(a, fr)
        if r > melhor[0]: melhor = (r, a, ouv)
        if r >= .97: break
    r, a, ouv = melhor; print(f'{r:.2f} | {fr} | ouvido: {ouv}', flush=True)
    T.append({'start': round(t, 3), 'end': round(t + len(a) / SR, 3), 'text': fr, 'nota': round(r, 2)}); parts.append(a); t += len(a) / SR
parts.append(np.zeros(int(SR * 4.5), np.float32))
sf.write('narracao.wav', np.concatenate(parts), SR); json.dump(T, open('tempos.json', 'w'), ensure_ascii=False, indent=1)
print('duração', round(t + 4.5, 1))

"""Narra uma frase por linha ('pausa|texto') com voz neural (edge-tts) e grava narracao.wav + tempos.json + legendas.srt."""
import sys, json, asyncio, subprocess, numpy as np, edge_tts
txt, voice, rate = sys.argv[1:4]; SR = 24000
async def _tts(fr, path): await edge_tts.Communicate(fr, voice, rate=rate).save(path)
def tts_retry(fr, path):
    import time
    for k in range(5):
        try: return asyncio.run(_tts(fr, path))
        except Exception as e: print('tentando de novo:', e); time.sleep(3)
    raise SystemExit('edge-tts falhou')
def load(p): return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-f','f32le','-ac','1','-ar',str(SR),'-'],capture_output=True).stdout, np.float32)
parts=[np.zeros(int(SR*.35),np.float32)]; t=.35; T=[]
for i, ln in enumerate(l for l in open(txt, encoding='utf-8') if l.strip()):
    gap, fr = ln.rstrip('\n').split('|', 1)
    parts.append(np.zeros(int(SR*float(gap)),np.float32)); t += float(gap)
    p=f'/tmp/w/s6/edge_{i:02d}.mp3'; tts_retry(fr,p); a=load(p)
    nz=np.where(np.abs(a)>0.01)[0]; a=a[max(0,nz[0]-600):nz[-1]+1800]
    T.append({'start':round(t,3),'end':round(t+len(a)/SR,3),'text':fr}); parts.append(a); t+=len(a)/SR
parts.append(np.zeros(int(SR*4.5),np.float32))
import soundfile as sf; sf.write('narracao.wav',np.concatenate(parts),SR)
json.dump(T,open('tempos.json','w'),ensure_ascii=False,indent=1)
ts=lambda x:f"00:{int(x//60):02d}:{int(x%60):02d},{int((x%1)*1000):03d}"
with open('legendas.srt','w',encoding='utf-8') as f:
    for i,e in enumerate(T,1): f.write(f"{i}\n{ts(e['start'])} --> {ts(e['end']+.15)}\n{e['text']}\n\n")
print('duração',round(t+4.5,1)); [print(e['start'],e['text'][:40]) for e in T]

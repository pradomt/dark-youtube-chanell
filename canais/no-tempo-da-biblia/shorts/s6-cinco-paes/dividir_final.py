"""Divide a última frase ('Nas mãos dele, não falta. Sóbra.') em duas no maior silêncio, para manter um tempo por batida."""
import json, numpy as np, soundfile as sf
y,sr=sf.read('narracao.wav');T=json.load(open('tempos.json'))
e=T[-1];a,b=int(e['start']*sr),int(e['end']*sr);seg=np.abs(y[a:b])
w=int(.03*sr);en=np.convolve(seg,np.ones(w)/w,'same');q=en<0.004
best=(0,0);run=0
for i,v in enumerate(q):
    run=run+1 if v else 0
    if run>best[0] and i>len(q)*.5: best=(run,i)
ce=(a+best[1])/sr; cs=ce-best[0]/sr
ins=max(0,int((.5-(ce-cs))*sr)); y=np.concatenate([y[:a+best[1]],np.zeros(ins),y[a+best[1]:]]); sf.write('narracao.wav',y,sr)
T[-1]={'start':e['start'],'end':round(cs,3),'text':'Nas mãos dele, não falta.'}
T.append({'start':round(ce+ins/sr,3),'end':round(e['end']+ins/sr,3),'text':'Sobra.'})
json.dump(T,open('tempos.json','w'),ensure_ascii=False,indent=1)
ts=lambda x:f"00:{int(x//60):02d}:{int(x%60):02d},{int((x%1)*1000):03d}"
with open('legendas.srt','w',encoding='utf-8') as f:
    for i,x in enumerate(T,1): f.write(f"{i}\n{ts(x['start'])} --> {ts(x['end']+.15)}\n{x['text']}\n\n")
print(len(T),'frases; Sobra em',T[-1]['start'])

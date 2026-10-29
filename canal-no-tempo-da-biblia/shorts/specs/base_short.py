import sys, importlib.util
_sp = importlib.util.spec_from_file_location('comum_longo', '/tmp/w/longo/planos/comum.py'); _m = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_m)
credito, IMG = _m.credito, _m.IMG
import os
def im(nome, fa, fb=None, ajuste=None, foco=None):
    p = dict(tipo='imagem', src=f'{IMG}/{nome}.jpg', fa=fa, fb=fb, credito=credito(nome))
    if ajuste is None and os.path.exists(p['src']):
        from PIL import Image
        w, h = Image.open(p['src']).size
        if w / h < 1.25: ajuste = 'contain'
    if ajuste: p['ajuste'] = ajuste
    if foco: p['foco'] = foco
    return p
MARCA = 'NO TEMPO DA BÍBLIA'

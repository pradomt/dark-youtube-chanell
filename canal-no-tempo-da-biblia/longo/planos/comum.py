import json, os
IMG = '/tmp/w/img'
CRED = json.load(open(f'{IMG}/creditos.json')) if os.path.exists(f'{IMG}/creditos.json') else {}
def credito(nome):
    c = CRED.get(nome, {}); a = c.get('autor', '') or 'Wikimedia Commons'; l = c.get('licenca', '')
    l = 'domínio público' if l.lower().startswith('public domain') or l == 'CC0' or l == 'No restrictions' else l
    return f'{a} · {l} · Wikimedia Commons'
def img(nome, rotulo='', etiqueta='', f=0, ajuste=None, foco=None, zoom=None, pan=None, arquivo=None):
    p = dict(tipo='imagem', src=f'{IMG}/{nome}.jpg', credito=credito(nome))
    if ajuste is None and os.path.exists(p['src']):
        from PIL import Image
        w, h = Image.open(p['src']).size
        if w / h < 1.25: ajuste = 'contain'   # retrato ou quadrada: mostra inteira sobre fundo desfocado
    if ajuste: p['ajuste'] = ajuste
    if foco: p['foco'] = foco
    if zoom is not None: p['zoom'] = zoom
    if pan: p['pan'] = pan
    return dict(f=f, arquivo=arquivo or f'{nome}.jpg', etiqueta=etiqueta, rotulo=rotulo, painel=p)
def num(de, para, legenda, contaf=(0, 2), sufixo='', prefixo='', casas=0, f=0, arquivo='contador.txt', etiqueta='', rotulo=''):
    return dict(f=f, arquivo=arquivo, etiqueta=etiqueta, rotulo=rotulo, painel=dict(tipo='numero', de=de, para=para, legenda=legenda, contaf=list(contaf), sufixo=sufixo, prefixo=prefixo, casas=casas))
def lista(itens, f=0, arquivo='notas.txt', etiqueta='', rotulo=''):
    its = []
    for x in itens:
        texto, nota, fi, dt = list(x) + [None, None, 0, 0][len(x):]
        its.append(dict(texto=texto, nota=nota, f=fi, dt=dt))
    return dict(f=f, arquivo=arquivo, etiqueta=etiqueta, rotulo=rotulo, painel=dict(tipo='lista', itens=its))
def cit(texto, ref, f=0, arquivo='citacao.txt', etiqueta='', rotulo=''):
    return dict(f=f, arquivo=arquivo, etiqueta=etiqueta, rotulo=rotulo, painel=dict(tipo='citacao', texto=texto, ref=ref))
def svg(nome, passos, f=0, arquivo=None, etiqueta='', rotulo=''):
    return dict(f=f, arquivo=arquivo or f'{nome}.svg', etiqueta=etiqueta, rotulo=rotulo, painel=dict(tipo='svg', arquivo_svg=f'/tmp/w/longo/svg/{nome}.svg', passos_f=passos))

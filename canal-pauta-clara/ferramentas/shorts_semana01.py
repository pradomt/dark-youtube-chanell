"""Shorts da semana 1 do Pauta Clara: texto, narração (Kokoro) e roteiro.json do palco.
Uso (no venv do Kokoro):  python shorts_semana01.py PASTA_SAIDA [narrar|roteiro|tudo] [n1,n2...]
Cada linha de "linhas" = uma frase narrada = uma batida na tela.
Tempos: "L3" = início da frase 3, "L3+0.5" = meio segundo depois, "F" = início da chamada final."""
import sys, os, json, re

COR = {"bg": "#eef2f6", "bg2": "#d3dbe5", "ink": "#0f1b2d", "sub": "#4a5568", "acc": "#0a7e78",
       "card": "#ffffff", "cardh": "#f0f4f8", "line": "#d3dbe5", "muted": "#6b7a8f"}
SIMBOLO = ('<svg width="96" height="96" viewBox="0 0 96 96"><rect x="4" y="4" width="88" height="88" rx="22" fill="var(--ink)"/>'
           '<rect x="22" y="28" width="52" height="8" rx="4" fill="#fff"/><rect x="22" y="44" width="52" height="8" rx="4" fill="#fff"/>'
           '<rect x="22" y="60" width="34" height="8" rx="4" fill="var(--acc)"/></svg>')
BASE = {"tema": "papel", "marca": "PAUTA CLARA", "decoracao": "pauta", "cores": COR, "simbolo": SIMBOLO, "girarMarca": False,
        "aviso": "voz sintética · fontes na descrição", "audio": "narracao.wav"}

SHORTS = [
 {"id": "short-01-posse-5-de-janeiro", "dia": "2026-11-02",
  "linhas": [
   ("Desde 1995, o presidente do Brasil sempre tomou posse no dia primeiro de janeiro.", "desde 1995, a posse era em", ["*1º de*", "*janeiro*"]),
   ("Em 2027, isso muda.", "em 2027,", ["isso", "*muda*"]),
   ("O presidente eleito em outubro toma posse no dia cinco de janeiro.", "o presidente eleito assume em", ["*5 de*", "*janeiro*"]),
   ("A mudança veio da Emenda Constitucional cento e onze, de 2021, que reescreveu o artigo oitenta e dois da Constituição.", "quem mudou foi a", ["Emenda", "*111*"]),
   ("Um dos motivos foi tirar a posse do feriado de Ano Novo, que dificultava a vinda de chefes de Estado de outros países.", "um dos motivos:", ["sair do", "*Ano Novo*"]),
   ("Os governadores eleitos tomam posse um dia depois, em seis de janeiro.", "governadores assumem em", ["*6 de*", "*janeiro*"]),
   ("E tem um efeito curioso: o mandato que começou em 2023 vai durar quatro dias a mais.", "e o mandato atual ganha", ["*+4 dias*"]),
   ("No sábado, o Pauta Clara mostra o calendário completo até a posse.", "sábado, no Pauta Clara:", ["o", "*calendário*"]),
  ],
  "cartao": {"arquivo": [["L0", "constituicao-art82.txt"], ["L1", "janeiro-2027.cal"]], "etiqueta": [["L0", "● EC 111/2021"]],
             "rotulo": [["L0", "POSSE PRESIDENCIAL"], ["L6", "DURAÇÃO DO MANDATO ATUAL"]],
             "paineis": [{"tipo": "extra", "a": "L0+0.4", "b": "L6"},
                         {"tipo": "numero", "a": "L6", "b": "F", "de": 0, "para": 4, "prefixo": "+", "sufixo": " dias", "conta": ["L6+1.5", "L6+3.5"], "legenda": "01/01/2023 → 05/01/2027"}],
             "diario": [["L3+0.5", "§ EC 111/2021 · art. 82 da Constituição"], ["L4+0.5", "✓ fora do feriado de Ano Novo"],
                        ["L5+0.5", "06/01 · posse dos governadores"], ["L6+0.8", "+4 dias · até a posse do sucessor"]]},
  "calendario": [{"a": "L0+0.4", "b": "L6", "mes": "JANEIRO 2027", "inicio": 5, "dias": 31,
                  "marcas": [{"dia": 1, "t": "L1+0.5", "tipo": "risco", "nota": "1º/jan · fim da tradição"},
                             {"dia": 5, "t": "L2+1.2", "tipo": "circulo", "nota": "5/jan · posse do presidente"},
                             {"dia": 6, "t": "L5+0.8", "tipo": "circulo", "nota": "6/jan · posse dos governadores"}]}],
  "pilulas": ["Sábado: vídeo completo", "Pauta Clara"]},

 {"id": "short-02-transicao-reeleito", "dia": "2026-11-03",
  "linhas": [
   ("Quando um presidente novo é eleito, existe uma lei para a passagem do governo.", "troca de presidente tem", ["regra de", "*transição*"]),
   ("É a lei dez mil seiscentos e nove, de 2002.", "está na", ["Lei", "*10.609*"]),
   ("Ela permite que o eleito monte uma equipe de transição, com até cinquenta cargos especiais pagos pelo governo.", "a equipe pode ter até", ["*50*", "cargos"]),
   ("A equipe começa a trabalhar dois dias úteis depois da eleição, e os ministérios são obrigados a passar as informações que ela pedir.", "começa", ["*2 dias*", "*úteis* após"]),
   ("Mas e quando o presidente é reeleito?", "mas e quando o presidente é", ["*reeleito*?"]),
   ("Aí não há troca de governo: quem assume em janeiro já está no cargo e já tem acesso às informações.", "aí não há", ["troca de", "*governo*"]),
   ("A lei diz que o eleito pode criar a equipe. Não é uma obrigação.", "a equipe é", ["*opcional*"]),
   ("Nesta fase, a atenção vai para outra coisa: a escolha dos ministros do novo mandato.", "o foco passa a ser", ["os novos", "*ministros*"]),
   ("Siga o Pauta Clara e entenda cada etapa até a posse.", "cada etapa até a posse:", ["Pauta", "*Clara*"]),
  ],
  "cartao": {"arquivo": [["L0", "lei-10609-2002.txt"]], "etiqueta": [["L0", "● transição"], ["L4", "● reeleição"]],
             "rotulo": [["L0", "LEI 10.609/2002"], ["L4", "QUANDO O PRESIDENTE É REELEITO"]],
             "paineis": [{"tipo": "lista", "a": "L0+0.4", "b": "L4", "itens": [
                            {"t": "L1+0.3", "texto": "Lei *10.609*/2002", "nota": "regra da transição"},
                            {"t": "L2+0.6", "texto": "até *50* cargos", "nota": "cargos especiais de transição"},
                            {"t": "L3+0.6", "texto": "começa em *2 dias úteis*", "nota": "e termina com a posse"}]},
                         {"tipo": "lista", "a": "L4", "b": "F", "itens": [
                            {"t": "L4+0.3", "texto": "presidente *reeleito*", "nota": "mesmo governo"},
                            {"t": "L5+0.5", "texto": "*sem* troca de governo", "nota": "já tem as informações"},
                            {"t": "L6+0.5", "texto": "equipe *opcional*", "nota": "a lei diz \"poderá\""},
                            {"t": "L7+0.8", "texto": "foco: *ministros*", "nota": "do novo mandato"}]}],
             "diario": [["L2+0.5", "✓ cargos com prazo para acabar"], ["L3+1", "↳ ministérios devem informar a equipe"], ["L6+0.5", "✓ facultativa ao candidato eleito"]]},
  "pilulas": ["Sábado: vídeo completo", "Pauta Clara"]},

 {"id": "short-03-diplomacao", "dia": "2026-11-04",
  "linhas": [
   ("Ganhar a eleição não leva ninguém direto para a posse.", "ganhar a eleição", ["*não basta*"]),
   ("Antes, vem a diplomação.", "antes, vem a", ["*diplomação*"]),
   ("É quando a Justiça Eleitoral entrega ao eleito um diploma, o documento que prova que ele venceu e pode assumir.", "o eleito recebe um", ["*diploma*"]),
   ("Sem diploma, não existe posse.", "sem diploma,", ["não há", "*posse*"]),
   ("O presidente e o vice recebem o diploma do Tribunal Superior Eleitoral.", "presidente e vice:", ["*TSE*"]),
   ("Governadores, senadores e deputados recebem dos tribunais regionais eleitorais de cada estado.", "governadores e parlamentares:", ["*TREs*"]),
   ("Em 2026, o prazo final para todas as diplomações é dezoito de dezembro.", "prazo final:", ["*18 de*", "*dezembro*"]),
   ("E é a partir da diplomação que começam a contar os prazos para questionar um mandato na Justiça.", "e é dela que contam os", ["prazos de", "*contestação*"]),
   ("Na sexta, o Pauta Clara explica como funcionam esses prazos.", "sexta, no Pauta Clara:", ["os", "*prazos*"]),
  ],
  "cartao": {"arquivo": [["L0", "codigo-eleitoral-art215.txt"], ["L6", "dezembro-2026.cal"]], "etiqueta": [["L0", "● diplomação"]],
             "rotulo": [["L0", "DA URNA À POSSE"], ["L4", "QUEM ENTREGA O DIPLOMA"], ["L6", "CALENDÁRIO TSE 2026"]],
             "paineis": [{"tipo": "lista", "a": "L0+0.4", "b": "L4", "itens": [
                            {"t": "L0+0.6", "texto": "*1* · eleição", "nota": "25/10 · 2º turno"},
                            {"t": "L1+0.4", "texto": "*2* · diplomação", "nota": "Justiça Eleitoral"},
                            {"t": "L3+0.3", "texto": "*3* · posse", "nota": "5/1 · presidente"}]},
                         {"tipo": "lista", "a": "L4", "b": "L6", "itens": [
                            {"t": "L4+0.4", "texto": "presidente e vice → *TSE*", "nota": "Tribunal Superior Eleitoral"},
                            {"t": "L5+0.6", "texto": "estados e Congresso → *TREs*", "nota": "um tribunal por estado"}]},
                         {"tipo": "extra", "a": "L6", "b": "F"}],
             "diario": [["L2+0.6", "✓ diploma = prova de que venceu"], ["L4+0.5", "§ Código Eleitoral · art. 215"], ["L6+0.5", "Res. TSE 23.760/2026 · calendário"]]},
  "calendario": [{"a": "L6", "b": "F", "mes": "DEZEMBRO 2026", "inicio": 2, "dias": 31,
                  "marcas": [{"dia": 18, "t": "L6+1.2", "tipo": "circulo", "nota": "18/12 · prazo final"}]}],
  "pilulas": ["Sexta: os prazos", "Pauta Clara"]},

 {"id": "short-04-prestacao-de-contas", "dia": "2026-11-05",
  "linhas": [
   ("A eleição acabou, mas a campanha ainda tem uma conta para fechar.", "a eleição acabou, mas falta", ["fechar a", "*conta*"]),
   ("Quem disputou o segundo turno tem até catorze de novembro para entregar a prestação de contas final.", "2º turno: prazo até", ["*14 de*", "*novembro*"]),
   ("Nela entra tudo o que a campanha arrecadou e gastou, nos dois turnos.", "entra tudo o que foi", ["arrecadado", "e *gasto*"]),
   ("Quem ficou só no primeiro turno tinha até três de novembro.", "só 1º turno: prazo era", ["*3 de*", "*novembro*"]),
   ("A regra vale para quem ganhou e para quem perdeu.", "vale para quem", ["ganhou e", "*perdeu*"]),
   ("E, para quem venceu, atrasar tem um preço: pela Lei das Eleições, enquanto as contas não forem entregues, o eleito não pode ser diplomado.", "sem as contas entregues,", ["*sem*", "diploma"]),
   ("As contas ficam públicas no site do tê ésse é, e qualquer pessoa pode consultar.", "qualquer pessoa pode", ["*consultar*"]),
   ("Siga o Pauta Clara e entenda cada etapa até a posse.", "cada etapa até a posse:", ["Pauta", "*Clara*"]),
  ],
  "cartao": {"arquivo": [["L0", "novembro-2026.cal"], ["L4", "lei-9504-art29.txt"]], "etiqueta": [["L0", "● prestação de contas"]],
             "rotulo": [["L0", "PRAZOS DA PRESTAÇÃO FINAL"], ["L4", "O QUE A LEI DIZ"]],
             "paineis": [{"tipo": "extra", "a": "L0+0.4", "b": "L4"},
                         {"tipo": "lista", "a": "L4", "b": "F", "itens": [
                            {"t": "L4+0.3", "texto": "vale para *todos*", "nota": "eleitos e não eleitos"},
                            {"t": "L5+1.5", "texto": "sem contas = *sem diploma*", "nota": "Lei 9.504/97 · art. 29, § 2º"},
                            {"t": "L6+0.5", "texto": "consulta *pública*", "nota": "DivulgaCandContas · TSE"}]}],
             "diario": [["L1+0.8", "Conta+JE · sistema de envio"], ["L2+0.5", "✓ receitas e despesas dos 2 turnos"], ["L5+0.8", "§ Lei 9.504/97 · art. 29"]]},
  "calendario": [{"a": "L0+0.4", "b": "L4", "mes": "NOVEMBRO 2026", "inicio": 0, "dias": 30,
                  "marcas": [{"dia": 14, "t": "L1+1.2", "tipo": "circulo", "nota": "14/11 · quem foi ao 2º turno"},
                             {"dia": 3, "t": "L3+0.8", "tipo": "risco", "nota": "3/11 · só 1º turno (encerrado)"}]}],
  "pilulas": ["Sábado: vídeo completo", "Pauta Clara"]},

 {"id": "short-05-contestar-eleicao", "dia": "2026-11-06",
  "linhas": [
   ("Quem discorda do resultado de uma eleição pode ir à Justiça?", "dá para contestar uma", ["*eleição*?"]),
   ("Pode. Mas a lei define como, quando e com que provas.", "pode, mas a lei define", ["como e", "*quando*"]),
   ("O primeiro caminho é o recurso contra a expedição de diploma, do artigo duzentos e sessenta e dois do Código Eleitoral.", "caminho 1: recurso contra o", ["*diploma*"]),
   ("O prazo é de três dias depois da diplomação.", "prazo:", ["*3 dias*"]),
   ("O segundo é a ação de impugnação de mandato eletivo, prevista na Constituição.", "caminho 2: ação de", ["*impugnação*"]),
   ("O prazo é de quinze dias depois da diplomação, e a ação precisa vir com provas de abuso de poder econômico, corrupção ou fraude.", "prazo de 15 dias, e com", ["*provas*"]),
   ("Quem julga é a Justiça Eleitoral. No caso de presidente, o Tribunal Superior Eleitoral.", "quem julga:", ["*TSE*"]),
   ("E, enquanto o tribunal não julga o recurso contra o diploma, o diplomado pode exercer o mandato normalmente, como diz o artigo duzentos e dezesseis do Código Eleitoral.", "enquanto isso, o diplomado", ["*exerce* o", "mandato"]),
   ("Até uma decisão final da Justiça, vale o resultado proclamado pelo tê ésse é.", "até lá, vale o", ["resultado", "*oficial*"]),
   ("Amanhã, no Pauta Clara: o calendário completo até a posse.", "amanhã, vídeo completo:", ["o", "*calendário*"]),
  ],
  "cartao": {"arquivo": [["L0", "codigo-eleitoral.txt"], ["L4", "constituicao-art14.txt"], ["L6", "rito.txt"]], "etiqueta": [["L0", "● rito legal"]],
             "rotulo": [["L0", "OS DOIS CAMINHOS NA LEI"], ["L6", "DURANTE O PROCESSO"]],
             "paineis": [{"tipo": "lista", "a": "L0+0.4", "b": "L6", "itens": [
                            {"t": "L2+0.5", "texto": "*RCED* · contra o diploma", "nota": "Código Eleitoral · art. 262"},
                            {"t": "L3+0.4", "texto": "prazo: *3 dias*", "nota": "após a diplomação"},
                            {"t": "L4+0.5", "texto": "*AIME* · contra o mandato", "nota": "Constituição · art. 14, § 10"},
                            {"t": "L5+0.5", "texto": "prazo: *15 dias* + provas", "nota": "abuso econômico, corrupção ou fraude"}]},
                         {"tipo": "lista", "a": "L6", "b": "F", "itens": [
                            {"t": "L6+0.4", "texto": "quem julga: *TSE*", "nota": "no caso de presidente"},
                            {"t": "L7+1.0", "texto": "diplomado *exerce* o mandato", "nota": "Código Eleitoral · art. 216"},
                            {"t": "L8+0.5", "texto": "vale o resultado *oficial*", "nota": "proclamado pelo TSE"}]}],
             "diario": [["L1+0.5", "§ Constituição + Código Eleitoral"], ["L5+1.5", "✓ a ação exige provas"], ["L8+0.5", "fonte: TSE · Código Eleitoral"]]},
  "pilulas": ["Amanhã: vídeo completo", "Pauta Clara"]},

 {"id": "short-06-72-dias-ate-a-posse", "dia": "2026-11-07",
  "linhas": [
   ("Entre o segundo turno e a posse do presidente, são setenta e dois dias.", "do 2º turno à posse:", ["*72 dias*"]),
   ("Vinte e cinco de outubro: a eleição.", "25 de outubro:", ["*eleição*"]),
   ("Catorze de novembro: prazo final da prestação de contas de quem foi ao segundo turno.", "14 de novembro:", ["*contas*"]),
   ("Até dezoito de dezembro: a diplomação dos eleitos.", "até 18 de dezembro:", ["*diplomação*"]),
   ("Cinco de janeiro, a posse do presidente. Seis de janeiro, a dos governadores.", "5 e 6 de janeiro:", ["*posses*"]),
   ("E primeiro de fevereiro: começa o novo Congresso.", "1º de fevereiro:", ["novo", "*Congresso*"]),
   ("Hoje tem vídeo completo no canal, com o que acontece em cada etapa.", "cada etapa explicada no", ["vídeo", "*completo*"]),
  ],
  "cartao": {"arquivo": [["L0", "calendario-2026-2027.txt"]], "etiqueta": [["L0", "● pós-eleição"]],
             "rotulo": [["L0", "CONTAGEM"], ["L1", "LINHA DO TEMPO"]],
             "paineis": [{"tipo": "numero", "a": "L0+0.4", "b": "L1", "de": 0, "para": 72, "conta": ["L0+0.8", "L0+3"], "legenda": "DIAS ATÉ A POSSE"},
                         {"tipo": "lista", "a": "L1", "b": "F", "itens": [
                            {"t": "L1+0.2", "texto": "*25/10* · eleição"},
                            {"t": "L2+0.2", "texto": "*14/11* · prestação de contas"},
                            {"t": "L3+0.2", "texto": "*18/12* · diplomação"},
                            {"t": "L4+0.2", "texto": "*5/1 e 6/1* · posses"},
                            {"t": "L5+0.2", "texto": "*1/2* · novo Congresso"}]}],
             "diario": [["L0+0.5", "25/10/2026 → 05/01/2027"]]},
  "pilulas": ["Hoje: vídeo completo", "Pauta Clara"]},

 {"id": "short-07-governadores-6-de-janeiro", "dia": "2026-11-08",
  "linhas": [
   ("Em 2027, o Brasil vai ter duas posses em dois dias seguidos.", "em 2027, são", ["*2 posses*", "seguidas"]),
   ("Dia cinco de janeiro, o presidente.", "5 de janeiro:", ["*presidente*"]),
   ("Dia seis, os governadores dos vinte e seis estados e do Distrito Federal.", "6 de janeiro:", ["*governos*", "*estaduais*"]),
   ("Até agora, tudo acontecia no mesmo dia: primeiro de janeiro.", "antes, era tudo em", ["*1º de*", "*janeiro*"]),
   ("Com isso, ficava difícil para um governador eleito ir à posse do presidente, em Brasília, e assumir o próprio cargo no mesmo dia.", "governador não estava em", ["*2 lugares*"]),
   ("A Emenda Constitucional cento e onze separou as datas, e esta é a primeira vez que a regra vale.", "a Emenda 111 estreia em", ["*2027*"]),
   ("Deputados federais e senadores não mudam: tomam posse em primeiro de fevereiro.", "Congresso continua em", ["*1º de*", "*fevereiro*"]),
   ("E os prefeitos continuam assumindo no primeiro de janeiro.", "prefeitos seguem em", ["*1º de*", "*janeiro*"]),
   ("Siga o Pauta Clara: política explicada, sem torcida.", "política explicada, sem torcida:", ["Pauta", "*Clara*"]),
  ],
  "cartao": {"arquivo": [["L0", "janeiro-2027.cal"], ["L6", "fevereiro-2027.cal"], ["L7", "janeiro.cal"]], "etiqueta": [["L0", "● EC 111/2021"]],
             "rotulo": [["L0", "POSSES DE 2027"], ["L6", "CONGRESSO NACIONAL"], ["L7", "MUNICÍPIOS"]],
             "paineis": [{"tipo": "extra", "a": "L0+0.4", "b": "F"}],
             "diario": [["L2+0.5", "26 estados + DF · 27 posses"], ["L5+0.5", "§ EC 111/2021 · arts. 28 e 82"], ["L7+0.5", "✓ prefeitos: sem mudança"]]},
  "calendario": [{"a": "L0+0.4", "b": "L6", "mes": "JANEIRO 2027", "inicio": 5, "dias": 31,
                  "marcas": [{"dia": 5, "t": "L1+0.5", "tipo": "cheio", "nota": "5/jan · presidente"},
                             {"dia": 6, "t": "L2+0.5", "tipo": "cheio", "nota": "6/jan · governadores"},
                             {"dia": 1, "t": "L3+0.8", "tipo": "circulo", "nota": "1º/jan · como era até 2023"}]},
                 {"a": "L6", "b": "L7", "mes": "FEVEREIRO 2027", "inicio": 1, "dias": 28,
                  "marcas": [{"dia": 1, "t": "L6+1.5", "tipo": "cheio", "nota": "1º/fev · deputados e senadores"}]},
                 {"a": "L7", "b": "F", "mes": "JANEIRO", "inicio": 5, "dias": 31,
                  "marcas": [{"dia": 1, "t": "L7+1.2", "tipo": "cheio", "nota": "1º/jan · prefeitos (sem mudança)"}]}],
  "pilulas": ["Política sem torcida", "Pauta Clara"]},
]


def narrar(sh, pasta):
    import numpy as np, soundfile as sf
    from kokoro_onnx import Kokoro
    K = Kokoro(os.environ["KOKORO_ONNX"], os.environ["KOKORO_VOICES"]); SR = 24000
    pieces, t, tl = [np.zeros(int(SR * .3), np.float32)], .3, []
    for fala, *_ in sh["linhas"]:
        a, _ = K.create(fala, voice="pf_dora", speed=0.95, lang="pt-br")
        tl.append({"start": round(t, 3), "end": round(t + len(a) / SR, 3), "text": fala})
        pieces += [a.astype(np.float32), np.zeros(int(SR * .3), np.float32)]; t += len(a) / SR + .3
    pieces.append(np.zeros(int(SR * 1.6), np.float32))  # respiro para a chamada final
    sf.write(f"{pasta}/narracao.wav", np.concatenate(pieces), SR)
    json.dump(tl, open(f"{pasta}/tempos.json", "w"), ensure_ascii=False, indent=1)
    open(f"{pasta}/narracao.txt", "w").write("\n".join(l[0] for l in sh["linhas"]) + "\n")
    print(sh["id"], round(t + 1.6, 1), "s")


def ts(x):
    h, r = divmod(x, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}"


def roteiro(sh, pasta):
    tl = json.load(open(f"{pasta}/tempos.json")); n = len(tl)
    st = [e["start"] for e in tl]
    def T(x):
        if isinstance(x, (int, float)): return x
        m = re.fullmatch(r"(L(\d+)|F)([+-][\d.]+)?", x)
        base = st[-1] if m.group(1) == "F" else st[int(m.group(2))]
        return round(base + float(m.group(3) or 0), 3)
    def fix(o):
        if isinstance(o, dict): return {k: (T(v) if k in ("a", "b", "t") and isinstance(v, str) else fix(v)) for k, v in o.items()}
        if isinstance(o, list):
            if len(o) >= 2 and isinstance(o[0], str) and re.fullmatch(r"(L\d+|F)([+-][\d.]+)?", o[0]): return [T(o[0])] + [fix(v) for v in o[1:]]
            return [fix(v) for v in o]
        return o
    bat = []
    for i, (fala, apoio, tit) in enumerate(sh["linhas"]):
        a = st[i]; dur = tl[i]["end"] - a
        passo = min(0.75, dur * 0.3)
        b = 99 if i == n - 1 else round(st[i + 1] - 0.05, 3)
        bat.append({"b": b, "apoio": [round(max(0.05, a - 0.15), 3), apoio],
                    "titulo": [[round(a + 0.25 + k * passo, 3), w] for k, w in enumerate(tit)]})
    c = fix(sh["cartao"]); c["a"] = round(st[0] + 0.4, 3); c["b"] = st[-1]
    for p in c["paineis"]:
        if p.get("tipo") == "numero" and "conta" in p: p["conta"] = [T(x) for x in sh["cartao"]["paineis"][c["paineis"].index(p)]["conta"]]
    R = dict(BASE, batidas=bat, cartao=c, chamada={"a": st[-1], "pilulas": sh["pilulas"], "seta": False})
    if "calendario" in sh: R["calendario"] = fix(sh["calendario"]); R["extra"] = os.environ.get("CALENDARIO_JS", "calendario.js")
    json.dump(R, open(f"{pasta}/roteiro.json", "w"), ensure_ascii=False, indent=1)
    with open(f"{pasta}/legendas.srt", "w") as fh:
        for i, e in enumerate(tl, 1):
            fh.write(f"{i}\n{ts(e['start'])} --> {ts(e['end'] + .2)}\n{e['text'].replace('tê ésse é', 'TSE')}\n\n")


if __name__ == "__main__":
    out, passo = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "tudo")
    so = set(sys.argv[3].split(",")) if len(sys.argv) > 3 else None
    for k, sh in enumerate(SHORTS, 1):
        if so and str(k) not in so: continue
        pasta = os.path.join(out, sh["id"]); os.makedirs(pasta, exist_ok=True)
        if passo in ("narrar", "tudo"): narrar(sh, pasta)
        if passo in ("roteiro", "tudo"): roteiro(sh, pasta)

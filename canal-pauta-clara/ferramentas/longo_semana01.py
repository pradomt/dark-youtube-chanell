"""Roteiro visual do longo da semana 1 (Pauta Clara) para o palco-16x9.html.
Uso: python longo_semana01.py PASTA_DO_LONGO   (precisa de tempos.json e narracao.wav gerados pelo narrar_frases.py)
Cada parágrafo da narração = uma batida (linha de apoio + título). O painel da janela vale até o próximo parágrafo que define outro.
Tempos dos itens: "s2" = início da 3ª frase do parágrafo; "p0.5" = metade do parágrafo."""
import sys, json, re, subprocess
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from shorts_semana01 import COR, SIMBOLO

ETAPAS = [["25/10", "eleição"], ["14/11", "contas"], ["18/12", "diplomação"], ["+3 e +15 dias", "contestação"],
          ["5/1", "posse"], ["6/1", "governadores"], ["1/2", "Congresso"]]
SEC = {  # seção: (chip, etapa na linha do tempo, nome do arquivo na janela)
 "01-abertura": ("DO 2º TURNO À POSSE", -1, "calendario-2026-2027.txt"),
 "02-resultado": ("O RESULTADO", 0, "resultado-tse-2turno.csv"),
 "03-transicao": ("ETAPA 1 · TRANSIÇÃO", 0, "lei-10609-2002.txt"),
 "04-contas": ("ETAPA 2 · CONTAS", 1, "lei-9504-1997.txt"),
 "05-diplomacao": ("ETAPA 3 · DIPLOMAÇÃO", 2, "codigo-eleitoral.txt"),
 "05b-congresso-atual": ("ENQUANTO ISSO", 2, "orcamento-2027.txt"),
 "06-contestacao": ("ETAPA 4 · CONTESTAÇÃO", 3, "codigo-eleitoral.txt"),
 "07-posse": ("ETAPA 5 · POSSE", 4, "constituicao-art78-82.txt"),
 "08-governadores-e-congresso": ("ETAPA 6 · ESTADOS E CONGRESSO", 5, "constituicao-art28-57.txt"),
 "09-fechamento": ("RESUMO", 99, "calendario-2026-2027.txt"),
}
CAP = {"DO 2º TURNO À POSSE": "72 dias entre a urna e a posse", "O RESULTADO": "O resultado oficial", "ETAPA 1 · TRANSIÇÃO": "Etapa 1: transição de governo",
       "ETAPA 2 · CONTAS": "Etapa 2: prestação de contas", "ETAPA 3 · DIPLOMAÇÃO": "Etapa 3: diplomação", "ENQUANTO ISSO": "Enquanto isso: o Orçamento de 2027",
       "ETAPA 4 · CONTESTAÇÃO": "Etapa 4: o que a lei prevê para contestar", "ETAPA 5 · POSSE": "Etapa 5: a posse em 5 de janeiro",
       "ETAPA 6 · ESTADOS E CONGRESSO": "Etapa 6: governadores e novo Congresso", "RESUMO": "Resumo do calendário"}
P = {  # (seção, parágrafo): (apoio, [título], painel ou None, rótulo da janela ou None)
 ("01-abertura", 0): ("da urna até a posse são", ["*72 dias*"],
   {"tipo": "numero", "de": 0, "para": 72, "conta": ["s2", "s2+2.2"], "legenda": "DIAS ENTRE 25/10/2026 E 05/01/2027"}, "CONTAGEM"),
 ("01-abertura", 1): ("72 dias que não são", ["um intervalo", "*vazio*"],
   {"tipo": "lista", "itens": [{"t": "s1+1.5", "texto": "prestação de *contas*"}, {"t": "s1+3", "texto": "*diplomação*"},
                               {"t": "s1+4.2", "texto": "janela de *contestação*"}, {"t": "s1+6.5", "texto": "posse em *data nova*"}]}, "O QUE ACONTECE NESSES DIAS"),
 ("01-abertura", 2): ("etapa por etapa:", ["o que diz", "a *lei*"],
   {"tipo": "lista", "itens": [{"t": "s0+2", "texto": "o que *acontece*"}, {"t": "s0+3.3", "texto": "quem *decide*"}, {"t": "s0+4.5", "texto": "o que diz a *lei*"}]}, "NESTE VÍDEO"),
 ("02-resultado", 0): ("segundo o TSE, o presidente", ["*reeleito*"],
   {"tipo": "placar", "conta": ["s1", "s1+3"], "fonte": "fonte: TSE · 2º turno, 25/10/2026", "linhas": [
     {"nome": "Lula (PT)", "pct": 51.79, "v": True, "nota": "64.256.232 votos"}, {"nome": "Flávio Bolsonaro (PL)", "pct": 48.21, "nota": "59.826.041 votos"}]}, "VOTOS VÁLIDOS · 2º TURNO"),
 ("02-resultado", 1): ("a diferença:", ["*4,4 milhões*", "de votos"], None, None),
 ("02-resultado", 2): ("votos válidos =", ["votos em", "*candidatos*"],
   {"tipo": "citacao", "texto": "Brancos e nulos *não entram* na conta dos votos válidos.", "fonte": "por isso 51,79% + 48,21% = 100%"}, "COMO SE CONTA"),
 ("02-resultado", 3): ("declarar o resultado não é", ["entregar o", "*cargo*"],
   {"tipo": "lista", "itens": [{"t": "s0", "texto": "resultado *declarado*", "nota": "25/10 · noite da eleição"},
                               {"t": "s1+1", "texto": "diploma", "nota": "até 18/12"}, {"t": "s1+2", "texto": "posse", "nota": "5/1/2027"}]}, "STATUS"),
 ("03-transicao", 0): ("etapa 1:", ["a *transição*"],
   {"tipo": "citacao", "texto": "Lei *10.609*, de 2002: regras da transição de governo.", "fonte": "Lei 10.609/2002"}, "A LEI"),
 ("03-transicao", 1): ("a equipe pode ter até", ["*50* cargos"],
   {"tipo": "lista", "itens": [{"t": "s0+2", "texto": "até *50* cargos especiais", "nota": "só durante a transição"},
                               {"t": "s1", "texto": "início: *2º dia útil*", "nota": "depois da eleição"},
                               {"t": "s1+4", "texto": "acesso a *informações*", "nota": "contas, programas, projetos"}]}, "O QUE A LEI PERMITE"),
 ("03-transicao", 2): ("para o governo novo", ["não começar", "no *escuro*"], None, None),
 ("03-transicao", 3): ("desta vez, presidente", ["*reeleito*"],
   {"tipo": "lista", "itens": [{"t": "s0", "texto": "*mesmo* presidente", "nota": "não há troca de governo"},
                               {"t": "s2", "texto": "equipe *opcional*", "nota": "a lei diz que o eleito \"poderá\""}]}, "QUANDO HÁ REELEIÇÃO"),
 ("03-transicao", 4): ("o foco vira", ["os novos", "*ministros*"],
   {"tipo": "citacao", "texto": "Ministros são de *livre nomeação* do presidente, sem aprovação do Congresso.", "fonte": "Constituição · art. 84, I"}, "MINISTÉRIO"),
 ("04-contas", 0): ("etapa 2:", ["as *contas*"],
   {"tipo": "lista", "itens": [{"t": "s1+1.6", "texto": "quanto *arrecadou*"}, {"t": "s1+2.6", "texto": "de quem *recebeu*"}, {"t": "s1+3.6", "texto": "como *gastou*"}]}, "PRESTAÇÃO DE CONTAS"),
 ("04-contas", 1): ("2º turno: prazo até", ["*14 de*", "*novembro*"],
   {"tipo": "calendario", "mes": "NOVEMBRO 2026", "inicio": 0, "dias": 30, "marcas": [
     {"dia": 14, "t": "s0+2.5", "tipo": "circulo", "nota": "14/11 · quem foi ao 2º turno"}, {"dia": 3, "t": "s1+1.5", "tipo": "risco", "nota": "3/11 · só 1º turno (encerrado)"}]}, "RES. TSE 23.760/2026"),
 ("04-contas", 2): ("sem contas entregues,", ["*sem*", "diploma"],
   {"tipo": "citacao", "texto": "Sem as contas no prazo, o eleito *não pode ser diplomado* enquanto durar o atraso.", "fonte": "Lei 9.504/1997 · art. 29, § 2º"}, "A REGRA"),
 ("04-contas", 3): ("as contas são", ["*julgadas*"],
   {"tipo": "lista", "itens": [{"t": "s0+2", "texto": "*aprovadas*"}, {"t": "s0+3", "texto": "aprovadas com *ressalvas*"}, {"t": "s0+4.2", "texto": "*desaprovadas*"},
                               {"t": "s1", "texto": "consulta *pública*", "nota": "DivulgaCandContas · TSE"}]}, "DEPOIS DA ENTREGA"),
 ("05-diplomacao", 0): ("etapa 3:", ["a *diplomação*"],
   {"tipo": "citacao", "texto": "O diploma *certifica* a eleição e *habilita* o eleito a tomar posse.", "fonte": "Código Eleitoral · art. 215"}, "O QUE É"),
 ("05-diplomacao", 1): ("quem entrega o", ["*diploma*"],
   {"tipo": "lista", "itens": [{"t": "s1", "texto": "presidente e vice → *TSE*", "nota": "Brasília"},
                               {"t": "s2", "texto": "estados e Congresso → *TREs*", "nota": "um tribunal por estado"}]}, "QUEM DIPLOMA"),
 ("05-diplomacao", 2): ("prazo final:", ["*18 de*", "*dezembro*"],
   {"tipo": "calendario", "mes": "DEZEMBRO 2026", "inicio": 2, "dias": 31, "marcas": [{"dia": 18, "t": "s0+2.5", "tipo": "circulo", "nota": "18/12 · limite para todas as diplomações"}]}, "CALENDÁRIO TSE 2026"),
 ("05-diplomacao", 3): ("conferência final:", ["registro", "e *contas*"],
   {"tipo": "lista", "itens": [{"t": "s0+2", "texto": "registro *válido*"}, {"t": "s0+4", "texto": "contas *entregues*"}]}, "PARA SER DIPLOMADO"),
 ("05b-congresso-atual", 0): ("enquanto isso,", ["o país", "*não para*"],
   {"tipo": "citacao", "texto": "Presidente e Congresso atuais seguem com *todos os poderes* até o fim dos mandatos.", "fonte": "mandatos atuais"}, "ENQUANTO ISSO"),
 ("05b-congresso-atual", 1): ("o Congresso precisa votar o", ["*Orçamento*", "de 2027"],
   {"tipo": "lista", "itens": [{"t": "s1", "texto": "envio do projeto: *31/8*", "nota": "pelo governo"},
                               {"t": "s1+5", "texto": "volta para sanção: *22/12*", "nota": "fim da sessão legislativa"}]}, "ADCT · ART. 35, § 2º, III"),
 ("05b-congresso-atual", 2): ("quem sai ainda decide", ["o *gasto*", "de 2027"], None, None),
 ("06-contestacao", 0): ("etapa 4:", ["a *contestação*"],
   {"tipo": "lista", "itens": [{"t": "p0.4", "texto": "Justiça *Eleitoral*"}, {"t": "p0.7", "texto": "prazos *curtos*"}, {"t": "p0.9", "texto": "*provas*"}]}, "O CAMINHO LEGAL"),
 ("06-contestacao", 1): ("discordar pode, mas pela", ["*Justiça*"], None, None),
 ("06-contestacao", 2): ("caminho 1: recurso contra o", ["*diploma*"],
   {"tipo": "lista", "itens": [{"t": "s0+1", "texto": "*RCED*", "nota": "Código Eleitoral · art. 262"}, {"t": "s1", "texto": "prazo: *3 dias*", "nota": "após a diplomação"},
                               {"t": "s2", "texto": "casos *específicos*", "nota": "inelegibilidade · condição de elegibilidade"}]}, "INSTRUMENTO 1"),
 ("06-contestacao", 3): ("caminho 2: ação de", ["*impugnação*"],
   {"tipo": "lista", "itens": [{"t": "s0+1", "texto": "*AIME*", "nota": "Constituição · art. 14, § 10"}, {"t": "s1", "texto": "prazo: *15 dias*", "nota": "após a diplomação"},
                               {"t": "s1+3", "texto": "exige *provas*", "nota": "abuso econômico, corrupção ou fraude"}]}, "INSTRUMENTO 2"),
 ("06-contestacao", 4): ("presidente: quem julga é o", ["*TSE*"],
   {"tipo": "citacao", "texto": "Enquanto o TSE não decidir o recurso, o diplomado *exerce o mandato* em toda a sua plenitude.", "fonte": "Código Eleitoral · art. 216"}, "DURANTE O PROCESSO"),
 ("06-contestacao", 5): ("até a decisão final, vale o", ["resultado", "*proclamado*"], None, None),
 ("07-posse", 0): ("etapa 5:", ["a *posse*"],
   {"tipo": "calendario", "mes": "JANEIRO 2027", "inicio": 5, "dias": 31, "marcas": [
     {"dia": 1, "t": "p1.3", "tipo": "risco", "nota": "1º/jan · posse de 1995 a 2023"}, {"dia": 5, "t": "p1.85", "tipo": "circulo", "nota": "5/jan · posse do presidente"}]}, "EC 111/2021"),
 ("07-posse", 1): ("a Emenda 111 levou a posse para", ["*5 de*", "*janeiro*"], None, None),
 ("07-posse", 2): ("o mandato atual ganha", ["*+4 dias*"],
   {"tipo": "numero", "de": 0, "para": 4, "prefixo": "+", "sufixo": " dias", "conta": ["s1+3", "s1+5"], "legenda": "01/01/2023 → 05/01/2027"}, "MANDATO ATUAL"),
 ("07-posse", 3): ("no Congresso, o", ["*compromisso*"],
   {"tipo": "citacao", "texto": "Manter, defender e cumprir a Constituição, observar as leis, promover o *bem geral* do povo brasileiro.", "fonte": "Constituição · art. 78"}, "SESSÃO SOLENE"),
 ("07-posse", 4): ("não assumiu em 10 dias?", ["cargo", "*vago*"],
   {"tipo": "numero", "de": 0, "para": 10, "sufixo": " dias", "conta": ["s0+1", "s0+3"], "legenda": "PARA ASSUMIR, SALVO FORÇA MAIOR · ART. 78, PARÁGRAFO ÚNICO"}, "REGRA DE SEGURANÇA"),
 ("07-posse", 5): ("o novo mandato:", ["*2027*", "a *2031*"],
   {"tipo": "lista", "itens": [{"t": "s0+1", "texto": "início: *05/01/2027*"}, {"t": "s0+3", "texto": "fim: *05/01/2031*"}]}, "DURAÇÃO · 4 ANOS"),
 ("08-governadores-e-congresso", 0): ("6 de janeiro:", ["*governadores*"],
   {"tipo": "calendario", "mes": "JANEIRO 2027", "inicio": 5, "dias": 31, "marcas": [
     {"dia": 5, "t": "s0", "tipo": "cheio", "nota": "5/jan · presidente"}, {"dia": 6, "t": "s0+1.5", "tipo": "cheio", "nota": "6/jan · 26 estados + DF"}]}, "CONSTITUIÇÃO · ART. 28"),
 ("08-governadores-e-congresso", 1): ("o Congresso continua em", ["*1º de*", "*fevereiro*"],
   {"tipo": "calendario", "mes": "FEVEREIRO 2027", "inicio": 1, "dias": 28, "marcas": [{"dia": 1, "t": "s1", "tipo": "cheio", "nota": "1º/fev · posse e eleição das Mesas"}]}, "CONSTITUIÇÃO · ART. 57"),
 ("08-governadores-e-congresso", 2): ("prefeitos:", ["*sem*", "mudança"],
   {"tipo": "lista", "itens": [{"t": "s0", "texto": "prefeitos: *1º de janeiro*", "nota": "a EC 111 não mudou"}]}, "MUNICÍPIOS"),
 ("09-fechamento", 0): ("recapitulando:", ["o *calendário*"],
   {"tipo": "lista", "itens": [{"t": "s1", "texto": "*25/10* · eleição"}, {"t": "s2", "texto": "*14/11* · contas (2º turno)"}, {"t": "s3", "texto": "*18/12* · diplomação"},
                               {"t": "s4", "texto": "*+3 e +15 dias* · contestação"}, {"t": "s5", "texto": "*5/1* · presidente"}, {"t": "s6", "texto": "*6/1* · governadores"},
                               {"t": "s7", "texto": "*1/2* · novo Congresso"}]}, "RESUMO"),
 ("09-fechamento", 1): ("as fontes estão na", ["*descrição*"],
   {"tipo": "lista", "itens": [{"t": "s0+3", "texto": "Constituição *Federal*"}, {"t": "s0+4", "texto": "Código *Eleitoral*"}, {"t": "s0+5", "texto": "Lei das *Eleições*"},
                               {"t": "s0+6", "texto": "calendário do *TSE*"}]}, "FONTES"),
 ("09-fechamento", 2): ("política explicada, sem torcida:", ["Pauta", "*Clara*"],
   {"tipo": "citacao", "texto": "Toda semana, política *explicada*, sem torcida.", "fonte": "inscreva-se · Pauta Clara"}, "PAUTA CLARA"),
}

def main(pasta):
    tl = json.load(open(f"{pasta}/tempos.json"))
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{pasta}/narracao.wav"]))
    paras = {}
    for e in tl: paras.setdefault((e["sec"], e["para"]), []).append(e)
    keys = list(paras); assert set(keys) == set(P), (set(keys) ^ set(P))
    ini = [paras[k][0]["start"] for k in keys]
    bat, pain, arq, rot, chip, et = [], [], [], [], [], []
    for i, k in enumerate(keys):
        fr = paras[k]; a = fr[0]["start"]; fim = ini[i + 1] if i + 1 < len(keys) else dur
        def T(x):
            if isinstance(x, (int, float)): return x
            m = re.fullmatch(r"([sp])([\d.]+)([+-][\d.]+)?", x)
            base = fr[min(int(m.group(2)), len(fr) - 1)]["start"] if m.group(1) == "s" else a + float(m.group(2)) * (fr[-1]["end"] - a)
            return round(base + float(m.group(3) or 0), 3)
        apoio, tit, painel, rotulo = P[k]
        passo = min(.8, (fr[0]["end"] - a) * .25)
        bat.append({"b": round(fim - .05, 3) if i + 1 < len(keys) else 1e9, "apoio": [round(a - .1, 3), apoio],
                    "titulo": [[round(a + .3 + j * passo, 3), w] for j, w in enumerate(tit)]})
        if painel:
            if pain: pain[-1]["b"] = a
            p = json.loads(json.dumps(painel)); p["a"] = round(a + .15, 3); p["b"] = 1e9
            for it in p.get("itens", []) + p.get("marcas", []): it["t"] = T(it["t"])
            if "conta" in p: p["conta"] = [T(x) for x in p["conta"]]
            pain.append(p)
        if rotulo: rot.append([a, rotulo])
        if k[1] == 0:
            c, e, f = SEC[k[0]]; chip.append([a - .2, c]); et.append([a, e]); arq.append([a, f])
    pain[-1]["b"] = dur - 1.5
    R = {"simbolo": SIMBOLO.replace('width="96" height="96"', 'width="54" height="54"'), "aviso": "narração com voz sintética · fontes na descrição",
         "duracao": round(dur, 3), "batidas": bat, "paineis": pain, "arquivo": arq, "rotulo": rot, "chip": chip, "etapaAtual": et, "etapas": ETAPAS,
         "cartao": [0.6, dur - 1.2], "frases": [[e["start"], e["end"], e["text"].replace("tê ésse é", "TSE").replace("Divulga Cand Contas", "DivulgaCandContas")] for e in tl]}
    json.dump(R, open(f"{pasta}/roteiro.json", "w"), ensure_ascii=False)
    # capítulos para a descrição
    with open(f"{pasta}/capitulos.txt", "w") as fh:
        for a, c in chip:
            s = max(0, int(a)); fh.write(f"{s // 60}:{s % 60:02d} {CAP.get(c, c)}\n")
    print("ok", round(dur, 1), "s,", len(bat), "batidas,", len(pain), "painéis")

if __name__ == "__main__":
    main(sys.argv[1])

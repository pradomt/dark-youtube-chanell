"""Gera titulo-descricao.txt de cada vídeo da semana 1 e o calendário de publicação."""
import os, sys
OUT = sys.argv[1]
F = {
 "tse_res": "TSE, resultado do 2º turno: https://www.tse.jus.br/comunicacao/noticias/2026/Outubro/presidente-do-tse-anuncia-reeleicao-de-lula-e-faz-balanco-do-2o-turno-das-eleicoes-2026",
 "tse_cal": "TSE, calendário eleitoral 2026: https://www.tse.jus.br/comunicacao/noticias/2026/Marco/eleicoes-2026-confira-as-principais-datas-do-calendario-eleitoral",
 "cf": "Constituição Federal: https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm",
 "ec111": "Emenda Constitucional 111/2021: https://www.planalto.gov.br/ccivil_03/constituicao/emendas/emc/emc111.htm",
 "trepr": "TRE-PR, novas datas de posse: https://www.tre-pr.jus.br/comunicacao/noticias/2024/Janeiro/data-da-posse-de-presidente-e-governadores-e-alterada-para-5-e-6-de-janeiro-respectivamente",
 "sbt_posse": "SBT News, posses em 2027: https://sbtnews.sbt.com.br/noticia/eleicoes/posse-do-presidente-e-governadores-muda-em-2027-veja-novas-datas",
 "ce": "Código Eleitoral (Lei 4.737/1965): https://www.planalto.gov.br/ccivil_03/leis/l4737compilado.htm",
 "l9504": "Lei das Eleições (Lei 9.504/1997): https://www.planalto.gov.br/ccivil_03/leis/l9504.htm",
 "l10609": "Lei 10.609/2002 (transição): https://www.planalto.gov.br/ccivil_03/leis/2002/l10609.htm",
 "politize": "Politize!, equipe de transição: https://www.politize.com.br/equipe-de-transicao/",
 "tse_diplo": "TSE, contas como condição para diplomação: https://temasselecionados.tse.jus.br/temas-selecionados/contas-de-campanha-eleitoral/prestacao-de-contas/condicao-para-diplomacao",
 "tresp": "TRE-SP, prazos da prestação de contas 2026: https://www.tre-sp.jus.br/comunicacao/noticias/2026/Outubro/eleicoes-2026-prazo-para-prestar-contas-do-1o-turno-vai-ate-3-de-novembro",
 "nsc": "NSC Total, diplomação até 18/12: https://www.nsctotal.com.br/politica/diplomacao-eleitos-18-dezembro-2026",
 "mpf": "MPF, ações eleitorais (AIME e RCED): https://www.mpf.mp.br/atuacao/eleitoral/pre-go/tipos-de-acao",
 "metropoles": "Metrópoles, placar final do 2º turno (28/10/2026): https://www.metropoles.com/mundo/em-carta-flavio-se-declara-verdadeiro-presidente-eleito-do-brasil",
 "dgabc": "DGABC, votação recorde no 2º turno: https://www.dgabc.com.br/Noticia/4365100/lula-bate-recorde-com-64-3-milhoes-de-votos-na-eleicao",
 "vatican": "Vatican News, resultado do 2º turno: https://www.vaticannews.va/pt/mundo/news/2026-10/lula-reeleito-presidente-brasil-segundo-turno.html",
}
RODAPE = ("\n\nO Pauta Clara explica regras e consequências da política brasileira, sem torcida. "
          "Se encontrar algum erro, comente com a fonte que a gente corrige.\n"
          "Narração com voz sintética (Kokoro TTS). Imagens e animações próprias.")
TAGS = "política, eleições 2026, posse presidencial, TSE, Constituição, Pauta Clara"
V = [
 ("2026-11-02", "seg", "12:00", "short-01-posse-5-de-janeiro", "Short",
  "Por que a posse do presidente mudou para 5 de janeiro?",
  "Desde 1995 a posse presidencial era em 1º de janeiro. Em 2027 ela vai ser no dia 5, e os governadores assumem no dia 6. Quem mudou foi a Emenda Constitucional 111, de 2021.",
  ["ec111", "cf", "trepr", "sbt_posse"], "#Shorts #política #posse"),
 ("2026-11-03", "ter", "12:00", "short-02-transicao-reeleito", "Short",
  "Presidente reeleito precisa de equipe de transição?",
  "A Lei 10.609/2002 permite que o candidato eleito monte uma equipe de transição com até 50 cargos especiais. Mas a equipe é opcional, e numa reeleição não há troca de governo.",
  ["l10609", "politize"], "#Shorts #política #transição"),
 ("2026-11-04", "qua", "12:00", "short-03-diplomacao", "Short",
  "Diplomação: a etapa obrigatória entre a eleição e a posse",
  "Sem diploma, não há posse. O presidente e o vice são diplomados pelo TSE; governadores, senadores e deputados, pelos TREs. Em 2026, o prazo final é 18 de dezembro.",
  ["ce", "tse_cal", "nsc"], "#Shorts #política #TSE"),
 ("2026-11-05", "qui", "12:00", "short-04-prestacao-de-contas", "Short",
  "A eleição acabou, mas a conta da campanha ainda não",
  "Quem disputou o 2º turno tem até 14 de novembro para entregar a prestação de contas final. E, pela Lei das Eleições, sem as contas entregues o eleito não pode ser diplomado.",
  ["tresp", "l9504", "tse_diplo"], "#Shorts #política #eleições"),
 ("2026-11-06", "sex", "12:00", "short-05-contestar-eleicao", "Short",
  "Dá para contestar uma eleição na Justiça? O que diz a lei",
  "A lei prevê dois caminhos, com prazo curto e exigência de provas: o recurso contra a expedição de diploma (3 dias) e a ação de impugnação de mandato eletivo (15 dias). Este vídeo explica só o rito legal, sem opinião sobre casos.",
  ["ce", "cf", "mpf"], "#Shorts #política #TSE"),
 ("2026-11-07", "sáb", "10:00", "longo-01-do-2-turno-a-posse", "Longo",
  "Do 2º turno à posse: o que acontece até 5 de janeiro (e o que diz a lei)",
  "São 72 dias entre a eleição de 25 de outubro e a posse do presidente em 5 de janeiro de 2027. Neste vídeo, o calendário etapa por etapa: o resultado oficial, a transição, a prestação de contas, a diplomação, os prazos para contestar na Justiça, a posse com data nova e o novo Congresso.\n\nCAPÍTULOS\n{capitulos}",
  ["tse_res", "dgabc", "vatican", "tse_cal", "l10609", "l9504", "tse_diplo", "ce", "cf", "ec111", "trepr", "mpf"], "#política #eleições2026 #posse"),
 ("2026-11-07", "sáb", "18:00", "short-06-72-dias-ate-a-posse", "Short",
  "72 dias entre a urna e a posse: o calendário",
  "25/10 eleição · 14/11 contas · até 18/12 diplomação · 5/1 posse do presidente · 6/1 governadores · 1/2 novo Congresso. O vídeo completo está no canal.",
  ["tse_cal", "ec111", "l9504"], "#Shorts #política #posse"),
 ("2026-11-08", "dom", "12:00", "short-07-governadores-6-de-janeiro", "Short",
  "Por que os governadores tomam posse um dia depois do presidente?",
  "Em 2027, pela primeira vez, as posses foram separadas: presidente em 5 de janeiro, governadores em 6. Deputados e senadores continuam em 1º de fevereiro, e prefeitos em 1º de janeiro.",
  ["ec111", "cf", "trepr", "sbt_posse"], "#Shorts #política #governadores"),
]
cal = ["# Calendário de publicação · Pauta Clara · semana 1 (2 a 8/11/2026)\n",
       "Horários sugeridos (Brasília). Nada foi publicado: tudo fica para a sua revisão. Ao subir, marque \"Conteúdo alterado ou sintético\" (voz sintética).\n",
       "| Dia | Horário | Formato | Título | Pasta |", "|---|---|---|---|---|"]
for d, dia, h, pasta, fmt, tit, desc, fontes, hs in V:
    p = os.path.join(OUT, pasta); cap = ""
    if os.path.exists(f"{p}/capitulos.txt"): cap = open(f"{p}/capitulos.txt").read().strip()
    corpo = desc.replace("{capitulos}", cap) + "\n\nFONTES\n" + "\n".join("- " + F[k] for k in fontes) + RODAPE + "\n\n" + hs
    open(f"{p}/titulo-descricao.txt", "w").write(f"TÍTULO\n{tit}\n\nDESCRIÇÃO\n{corpo}\n\nTAGS\n{TAGS}\n\nPUBLICAR EM\n{dia} {d[8:]}/{d[5:7]} às {h} (Brasília) · {fmt}\nMarcar: Conteúdo alterado ou sintético = SIM (voz sintética)\n")
    cal.append(f"| {dia} {d[8:]}/{d[5:7]} | {h} | {fmt} | {tit} | `{pasta}/` |")
cal += ["", "Por que esses horários: sem dados do canal ainda, usei meio-dia para os Shorts (pausa do almoço) e 10h de sábado para o longo, com o Short de chamada às 18h do mesmo dia. Depois de 2 semanas, a gente ajusta pelos dados do YouTube Studio.",
        "", "Terça e quinta eram vagas para notícia do dia. Como os vídeos foram feitos com antecedência, entraram dois Shorts fixos no lugar (transição e prestação de contas). Se na véspera houver notícia melhor, eles podem ser trocados e ficam guardados para outra semana."]
open(os.path.join(OUT, "calendario-publicacao.md"), "w").write("\n".join(cal) + "\n")
print("ok")

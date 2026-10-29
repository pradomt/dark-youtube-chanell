import sys; sys.path.insert(0, '/tmp/w/longo/planos')
from comum import img, num, lista, cit, svg

MARCA = 'NO TEMPO DA BÍBLIA'
TEMA = 'noite'
ACENTO = '#ec7a35'
REF = 'SALMO 23 · TRADUÇÃO LIVRE'
V = {
 1: 'O Senhor é o meu pastor; *nada me faltará*.',
 2: 'Em pastos verdes me faz deitar; *me conduz a águas tranquilas*.',
 3: 'Restaura a minha vida; *me guia por trilhas certas*, por amor do seu nome.',
 4: 'Ainda que eu ande pelo vale da sombra da morte, não temerei mal nenhum, *porque tu estás comigo*; a tua vara e o teu cajado me consolam.',
 5: 'Preparas uma mesa diante de mim, na presença dos meus inimigos; unges com óleo a minha cabeça; *o meu cálice transborda*.',
 6: 'Certamente a bondade e o amor leal *me seguirão* todos os dias da minha vida; e habitarei na casa do Senhor por longos dias.',
}
def verso(n): return cit(V[n], f'SALMO 23:{n} · TRADUÇÃO LIVRE', arquivo='salmo-23.txt', etiqueta=f'● verso {n}', rotulo='O TEXTO')
CAP = {
    '02-quem-escreveu': ('01', 'Quem *escreveu*', 'um salmo de Davi'),
    '03-versos-1-2': ('02', 'Pastos verdes e *águas tranquilas*', 'versos 1 e 2'),
    '04-verso-3': ('03', 'Trilhas *certas*', 'verso 3'),
    '05-verso-4': ('04', 'O vale da *sombra*', 'verso 4'),
    '06-verso-5': ('05', 'A *mesa*', 'verso 5'),
    '07-verso-6': ('06', 'A *casa*', 'verso 6'),
    '08-reflexao': ('07', 'O que o salmo *não promete*', 'e o que ele promete'),
    '09-oracao': ('08', 'Uma oração para a *noite*', 'inspirada no Salmo 23'),
}
FOTO = 'OVELHAS NA JUDEIA · AMERICAN COLONY · c. 1900'
P = [
 dict(s='01-abertura', p=0, apoio='Salmo 23:1', titulo='O Senhor é o|meu *pastor*', cena=img('salmo23-a', FOTO, '● Salmo 23')),
 dict(s='01-abertura', p=1, apoio='hospitais, velórios, casamentos', titulo='o texto mais|*conhecido*', cena=img('pastor-por-do-sol', 'PASTOR AO PÔR DO SOL · AMERICAN COLONY', '● c. 1900')),
 dict(s='01-abertura', p=2, apoio='há três mil anos', titulo='o que o salmista|*via*',
      cena=lista([('Pastos verdes *só alguns meses*', None, 1), ('*Vales* estreitos e escuros', None, 2), ('A *mesa* de um anfitrião', None, 3)], rotulo='O MUNDO DO SALMO')),
 dict(s='01-abertura', p=3, apoio='verso a verso', titulo='e uma *oração*|para dormir', cena=img('pastores-noite', 'PASTORES À NOITE · BELÉM · AMERICAN COLONY', '● c. 1900')),
 dict(s='01-abertura', p=4, apoio='a tradução', titulo='*tradução livre*|do hebraico',
      cena=lista([('Feita a partir do *hebraico*', 'para este vídeo', 0, .5), ('A mesma *ideia* da sua Bíblia', 'palavras podem mudar', 1)], rotulo='SOBRE A TRADUÇÃO')),
 # 01 quem escreveu
 dict(s='02-quem-escreveu', p=0, apoio='o título em hebraico', titulo='*mizmor*|le David',
      cena=lista([('*mizmor*', 'salmo, canção com instrumento', 0, .8), ('*le* David', 'de Davi · para Davi · dedicado a Davi', 2)], rotulo='O TÍTULO DO SALMO'),
      d=[(5, '✓ tradição judaica e cristã: Davi')]),
 dict(s='02-quem-escreveu', p=1, apoio='1 Samuel 16', titulo='antes de rei,|*pastor*', cena=img('tissot-davi-samuel', 'DAVI APRESENTADO A SAMUEL · TISSOT', '● 1 Samuel 16:11', foco='50% 30%')),
 dict(s='02-quem-escreveu', p=2, apoio='1 Samuel 17', titulo='o *leão*|e o urso',
      cena=cit('Quando um leão ou um urso vinha e pegava uma ovelha do rebanho, *eu ia atrás dele* e tirava a ovelha da sua boca.', '1 SAMUEL 17:34-35 · PARÁFRASE', rotulo='DAVI A SAUL')),
 dict(s='02-quem-escreveu', p=3, apoio='a vida no campo', titulo='dias e noites|*ao relento*', cena=img('pastor-ovelhas', 'PASTOR E OVELHAS · AMERICAN COLONY', '● c. 1900')),
 dict(s='02-quem-escreveu', p=4, apoio='no Oriente antigo', titulo='reis chamados|de *pastores*',
      cenas=[img('hamurabi', 'CÓDIGO DE HAMURABI · MUSEU DO LOUVRE', '● c. 1750 a.C.', foco='50% 20%'),
             cit('*Tu apascentarás* o meu povo Israel.', '2 SAMUEL 5:2 · PARÁFRASE', f=3, rotulo='DAVI REI')]),
 dict(s='02-quem-escreveu', p=5, apoio='e mesmo assim', titulo='eu também preciso|de um *pastor*', cena=img('pastor-conduzindo', 'PASTOR CONDUZINDO O REBANHO · AMERICAN COLONY', '● c. 1900')),
 # 02 versos 1-2
 dict(s='03-versos-1-2', p=0, apoio='verso 1', titulo='nada me|*faltará*', cena=verso(1)),
 dict(s='03-versos-1-2', p=1, apoio='não "um" pastor', titulo='o *meu*|pastor', cena=img('salmo23-b', FOTO, '● verso 1'), d=[(6, '✓ o necessário não vai faltar')]),
 dict(s='03-versos-1-2', p=2, apoio='verso 2', titulo='pastos|*verdes*', cena=verso(2)),
 dict(s='03-versos-1-2', p=3, apoio='chuva de outubro a abril', titulo='verde só|*alguns meses*', cena=svg('chuvas', {'A': 1, 'B': 2}, rotulo='O ANO DO PASTOR', etiqueta='● Jerusalém')),
 dict(s='03-versos-1-2', p=4, apoio='me faz deitar', titulo='saciada|e *segura*', cena=img('salmo23-c', FOTO, '● descanso')),
 dict(s='03-versos-1-2', p=5, apoio='águas de descanso', titulo='águas|*tranquilas*',
      cenas=[img('aguas-tranquilas', '"JUNTO ÀS ÁGUAS TRANQUILAS" · AMERICAN COLONY', '● c. 1900'),
             img('tissot-jaco-raquel', 'JACÓ E RAQUEL NO POÇO · TISSOT', '● Gênesis 29:10', f=3, foco='50% 30%')]),
 dict(s='03-versos-1-2', p=6, apoio='o pastor vai na frente', titulo='uma água que ela|*não alcançaria*', cena=img('salmo23-d', FOTO, '● verso 2')),
 # 03 verso 3
 dict(s='04-verso-3', p=0, apoio='verso 3', titulo='restaura a|*minha vida*', cena=verso(3)),
 dict(s='04-verso-3', p=1, apoio='nefesh', titulo='devolver o|*fôlego*', cena=lista([('*nefesh*', 'vida · fôlego · alma', 0, .6), ('restaurar = *devolver o fôlego*', None, 2)], rotulo='A PALAVRA')),
 dict(s='04-verso-3', p=2, apoio='trilhas certas', titulo='o pastor|*sabe o caminho*',
      cenas=[img('uadi-qelt-2', 'DESERTO DA JUDEIA · UÁDI QELT', '● trilhas'), img('uadi-matson', 'UM UÁDI PROFUNDO · AMERICAN COLONY', '● c. 1900', f=5)],
      d=[(2, 'veredas = caminho batido, sulco')]),
 dict(s='04-verso-3', p=3, apoio='por amor do seu nome', titulo='o *nome*|do pastor',
      cena=lista([('Nome = *reputação*', 'no mundo antigo', 1), ('Cuidado pelo *caráter* de Deus', 'não pelo mérito da ovelha', 3)], rotulo='POR AMOR DO SEU NOME')),
 # 04 verso 4
 dict(s='05-verso-4', p=0, apoio='verso 4', titulo='o vale da|*sombra da morte*', cena=verso(4)),
 dict(s='05-verso-4', p=1, apoio='a palavra hebraica', titulo='*escuridão*|profunda', cena=lista([('*tsalmavet*', 'lido como "sombra da morte"', 1), ('ou *escuridão profunda*', 'as duas leituras têm defensores', 2)], rotulo='A PALAVRA')),
 dict(s='05-verso-4', p=2, apoio='deserto da Judeia', titulo='os|*uádis*',
      cenas=[img('uadi-qelt-1', 'UÁDI QELT · DESERTO DA JUDEIA', '● hoje'), img('uadi-qelt-3', 'UÁDI QELT · DESERTO DA JUDEIA', '● hoje', f=2)]),
 dict(s='05-verso-4', p=3, apoio='uma tradição antiga', titulo='o uádi|*Qelt*?', cena=img('mosteiro-qelt', 'MOSTEIRO DE SÃO JORGE · UÁDI QELT · c. 1900', '● tradição'), d=[(2, '? o texto não dá o nome do lugar')]),
 dict(s='05-verso-4', p=4, apoio='repare', titulo='de *ele*|para *tu*', cena=svg('pessoa-verbo', {'A': 1, 'B': 3}, rotulo='QUEM FALA COM QUEM', etiqueta='● versos 1 a 4')),
 dict(s='05-verso-4', p=5, apoio='no lugar mais escuro', titulo='falar|*com* Deus'),
 dict(s='05-verso-4', p=6, apoio='o que consola', titulo='a *vara*|e o cajado',
      cenas=[img('pastor-vale-jordao', 'PASTOR NO VALE DO JORDÃO · 1919', '● American Colony'),
             lista([('*Vara*', 'bastão curto e pesado · defesa', 3), ('*Cajado*', 'bastão longo · apoio e condução', 5)], f=2, rotulo='DUAS FERRAMENTAS')]),
 dict(s='05-verso-4', p=7, apoio='proteger e conduzir', titulo='o pastor|*está aqui*', cena=img('passando-vara', '"PASSANDO SOB A VARA" · CONTAGEM DAS OVELHAS', '● Ezequiel 20:37')),
 # 05 verso 5
 dict(s='06-verso-5', p=0, apoio='verso 5', titulo='uma *mesa*|preparada', cena=verso(5)),
 dict(s='06-verso-5', p=1, apoio='a imagem muda', titulo='Deus como|*anfitrião*', cena=svg('viagem', {'A': 0, 'B': 0, 'C': 1, 'D': 2}, rotulo='A VIAGEM DO SALMO', etiqueta='● campo → casa')),
 dict(s='06-verso-5', p=2, apoio='hospitalidade no Oriente antigo', titulo='o hóspede sob|*proteção*', cena=lista([('Hóspede sob o teto = *protegido*', None, 1), ('*Ló* em Sodoma', 'Gênesis 19', 2)], rotulo='HOSPITALIDADE')),
 dict(s='06-verso-5', p=3, apoio='na presença dos inimigos', titulo='uma declaração|de *proteção*', d=[(2, '✓ veem tudo, mas não tocam no convidado')]),
 dict(s='06-verso-5', p=4, apoio='Lucas 7:46', titulo='óleo na|*cabeça*', cena=cit('Você não ungiu a minha cabeça com óleo, mas *ela ungiu os meus pés com perfume*.', 'LUCAS 7:46 · PARÁFRASE', rotulo='HONRA AO HÓSPEDE')),
 dict(s='06-verso-5', p=5, apoio='o cálice transborda', titulo='até|*derramar*', cena=img('lamparinas', 'LAMPARINAS DE AZEITE · ÉPOCA HERODIANA', '● óleo')),
 # 06 verso 6
 dict(s='07-verso-6', p=0, apoio='verso 6', titulo='bondade e|*amor leal*', cena=verso(6)),
 dict(s='07-verso-6', p=1, apoio='o verbo hebraico', titulo='a bondade|*corre atrás*', cena=lista([('*radaf*', 'perseguir · correr atrás', 1), ('quem persegue aqui é a *bondade*', None, 3)], rotulo='A PALAVRA')),
 dict(s='07-verso-6', p=2, apoio='amor leal', titulo='*hesed*', cena=lista([('*hesed*', 'amor que cumpre a promessa', 0, .5), ('fiel mesmo quando o outro *falha*', None, 2), ('muitas Bíblias: *misericórdia*', None, 3)], rotulo='A PALAVRA')),
 dict(s='07-verso-6', p=3, apoio='do pasto até o lar', titulo='uma viagem|*completa*', cena=svg('viagem', {'A': 1, 'B': 1, 'C': 1, 'D': 2}, rotulo='A VIAGEM DO SALMO', etiqueta='● campo → casa')),
 # 07 reflexão
 dict(s='08-reflexao', p=0, apoio='agora repare', titulo='o que ele|*não promete*', cena=img('uadi-qelt-4', 'UÁDI QELT · DESERTO DA JUDEIA', '● hoje')),
 dict(s='08-reflexao', p=1, apoio='"ainda que eu ande"', titulo='o vale faz parte|do *caminho*'),
 dict(s='08-reflexao', p=2, apoio='os inimigos', titulo='continuam|*ali*'),
 dict(s='08-reflexao', p=3, apoio='o que ele promete', titulo='*companhia*', cena=img('pastor-conduzindo', 'PASTOR CONDUZINDO O REBANHO · AMERICAN COLONY', '● c. 1900')),
 dict(s='08-reflexao', p=4, apoio='momentos difíceis', titulo='quem está com você|*dentro da dor*'),
 dict(s='08-reflexao', p=5, apoio='o seu próprio vale', titulo='*tu estás*|comigo', cena=img('salmo23-e', FOTO, '● verso 4')),
 # 08 oração
 dict(s='09-oracao', p=0, apoio='se você quiser', titulo='respire|*fundo*', cena=img('pastores-noite', 'PASTORES À NOITE · BELÉM · AMERICAN COLONY', '● oração')),
 dict(s='09-oracao', p=1, apoio='Senhor,', titulo='tu és o meu|*pastor*'),
 dict(s='09-oracao', p=2, apoio='esta noite', titulo='deitar|em *paz*', cena=img('aguas-tranquilas', '"JUNTO ÀS ÁGUAS TRANQUILAS" · AMERICAN COLONY', '● oração')),
 dict(s='09-oracao', p=3, apoio='onde eu me cansei', titulo='restaura o|meu *fôlego*'),
 dict(s='09-oracao', p=4, apoio='se amanhã houver um vale', titulo='tu estás|*comigo*', cena=img('uadi-matson', 'UM UÁDI PROFUNDO · AMERICAN COLONY', '● oração')),
 dict(s='09-oracao', p=5, apoio='obrigado', titulo='pela|*mesa posta*'),
 dict(s='09-oracao', p=6, apoio='bondade e amor leal', titulo='descansar|na *tua casa*', cena=img('pastor-por-do-sol', 'PASTOR AO PÔR DO SOL · AMERICAN COLONY', '● amém')),
 # fechamento
 dict(s='10-fechamento', p=0, apoio='guarde este vídeo', titulo='para uma|*noite difícil*'),
 dict(s='10-fechamento', p=1, apoio='No Tempo da Bíblia', titulo='toda|*semana*', cena=lista([('Segunda · *como se vivia*', 'o mundo da Bíblia', 0, .3), ('Quinta · *um salmo*', 'contexto e oração', 0, 1.5)], rotulo='TODA SEMANA')),
 dict(s='10-fechamento', p=2, apoio='na próxima semana', titulo='*Salmo 91*', d=[(1, '→ quem escreveu e o que cada imagem significa')]),
]

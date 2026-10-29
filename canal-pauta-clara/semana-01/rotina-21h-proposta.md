# Rotina das 21h · proposta (ainda NÃO ligada)

Fica desligada até você validar as semanas 1 e 2. Quando aprovar, eu crio a rotina agendada.

## Como funcionaria, todo dia às 21h (Brasília)

1. **Leitura (5 min, automático).** Uma sessão minha abre as capas de política do g1 e do Metrópoles e as notícias do TSE, da Câmara e do Senado do dia.
2. **Triagem (automático).** Escolho até 3 pautas que cabem no formato "como funciona / o que acontece agora", com regra ou número que explique. Descarto briga, fala de político, pesquisa sem registro e qualquer coisa com uma fonte só.
3. **Checagem (automático).** Cada fato precisa aparecer em pelo menos duas fontes (uma oficial quando existir). O que não fechar vira "não usar".
4. **Produção (automático, ~15 min).** Para a pauta número 1: roteiro de 30 a 45 s, narração Dora 0,95, MP4 no template do canal, capa, título, descrição com fontes, legenda.
5. **Aprovação (você, ~10 min).** Você recebe uma mensagem com o vídeo, as 3 pautas e a checagem. Responde "aprova", "troca pela 2" ou manda a correção.
6. **Publicação.** Na fase atual, você sobe manualmente. Na fase 2, eu subo como **privado/agendado** pela YouTube Data API e você só confere. No canal de política, a aprovação humana fica sempre.

## Regras fixas da rotina

- Nunca publicar sem a sua aprovação.
- Nada de recorte de TV, foto ou texto copiado dos portais: tudo reescrito, com as fontes na descrição.
- Sem adjetivo sobre pessoas, sem previsão, sem opinião sobre mérito de processo.
- Se não houver pauta boa no dia, sai um Short fixo do banco (regra, número, data) em vez de forçar notícia.
- Se o assunto for desinformação eleitoral, só o rito e a posição oficial do TSE.

## Custos e limites

- Roda dentro do seu Claude Pro; sem custo extra de API da Anthropic.
- YouTube Data API: o upload usa a cota gratuita (cada upload custa 1.600 unidades de 10.000 por dia, então cabe com folga).
- A sua chave da API não fica salva em nenhum arquivo; para a fase 2 precisamos configurar a autorização OAuth do canal com você.

## O que eu preciso de você para ligar

1. Aprovar o formato depois de 1 a 2 semanas de validação.
2. Confirmar o horário (21h) e por onde quer receber a aprovação.
3. Para a fase 2: criar o canal e autorizar o app de upload (te guio no dia).

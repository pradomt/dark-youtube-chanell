# No Tempo da Bíblia · pipeline de produção

Canal cristão, ângulo misto: por semana, 1 longo histórico (voz Kokoro `pm_alex` 1,05, tema papel) e 1 longo devocional com contexto (voz `pf_dora` 0,95, tema noite), mais 5 Shorts derivados dos dois.
Os vídeos prontos ficam na pasta do projeto (`/mnt/project-files/canal-no-tempo-da-biblia/`); aqui ficam os roteiros e os scripts.

## Etapas

1. **Roteiro**: um `.txt` por seção em `semana-XX/<video>/textos/`. Cada linha é um parágrafo, e cada parágrafo vira uma batida na tela.
2. **Narração**: `producao/narrar_frases.py modelo.onnx voices.bin pasta_textos pasta_saida voz velocidade`.
   Gera `narracao.wav`, `tempos.json` (início e fim de cada frase) e `legendas.srt`.
   Seções com `oracao` no nome ganham pausas maiores. O dicionário `PRON` troca grafias só para a voz (ex.: `hesed` → `réssed`).
3. **Imagens**: `producao/commons.py busca.json "termo 1" "termo 2"` procura no Wikimedia Commons; `producao/baixar.py lista.txt` baixa (`nome = trecho do título do arquivo`) e grava `creditos.json` com autor e licença.
   O proxy da nuvem bloqueia o arquivo original (erro 429), por isso o script pede a miniatura de 1920, 1280 ou 960 px.
4. **Longo 16:9** (`longo/`): `palco-longo.html` é a versão horizontal do template "palco único" dos Shorts.
   - `planos/plano_N.py`: um item por parágrafo, com apoio, título (`|` separa os pedaços, `*palavra*` vai na cor de acento) e a cena do cartão (`img`, `lista`, `num`, `cit`, `svg`).
   - `python montar_roteiro.py planos/plano_1.py tempos.json narracao.mp3 roteiro1.json`
   - `node render-longo.js roteiro1.json saida.mp4 --partes 4` grava em 4 processos paralelos (cerca de 25 a 35 min para 15 min de vídeo num container de 4 núcleos). `--quadros 10,62` salva só PNGs para conferir.
5. **Shorts** (`shorts/`): `palco.html` é o template aprovado, com a decoração nova `"decoracao": "biblia"` (arco de pedra + lamparina) e painel `svg`.
   - `specs/sN.py`: batidas por frase, cartão e painéis por frase.
   - `python montar_short.py specs/s1.py tempos.json narracao.mp3 r1.json` e `node render.js r1.json short-1.mp4`.
6. **Thumbnail**: `node thumb/thumb.js '{"tema":"papel","img":"file:///...jpg","k":"LINHA PEQUENA","h":"TÍTULO COM *DESTAQUE*","s":"pílula"}' thumb.png`.

Os scripts ainda usam caminhos absolutos de `/tmp/w` (pasta de trabalho do container). Para rodar em outro lugar, troque `IMG` em `longo/planos/comum.py` e os caminhos dos SVGs.

## Regras editoriais

- Bíblia: tradução livre do hebraico ou paráfrase, sempre marcada na tela. Nunca NVI ou ARA.
- Toda afirmação histórica com fonte na descrição; o que é tradição ou estimativa é dito como tal na narração.
- Tom respeitoso e sem denominação.
- Imagens: domínio público ou licença livre, com crédito. Se entrar imagem de IA realista, avisar na tela e marcar "conteúdo alterado ou sintético".

# Template de Short "palco único"

Modelo aprovado em 29/10/2026 (Short 1 do vídeo "As estrelas da bandeira"). Estilo extraído de um Reel de referência: uma tela só, sem cortes, título grande a cada frase e uma "janela" embaixo que se monta junto com a fala.

O visual fica em `palco.html`. Cada vídeo é só um `roteiro.json`, e um script extra quando precisa de um desenho próprio, como a carta celeste.

## Regras de estilo

- **Formato:** 1080x1920, 30 fps, sem cortes. Tudo entra e sai com desfoque, fade e um leve deslize (0,3 s).
- **Batida:** uma frase da narração = uma batida de 3 a 5 s. Uma linha de apoio pequena e cinza, e embaixo o título enorme (Montserrat Black, 118 px). A palavra-chave vai na cor de acento (`*assim*` no roteiro).
- **Janela:** cartão estilo app (3 bolinhas, nome de arquivo, etiqueta à direita), um rótulo em mono, uma área visual e um "diário" no rodapé com até 3 linhas. A primeira palavra de cada linha do diário sai na cor de acento.
- **Chamada final:** a marca volta, com duas pílulas (a última preenchida) e a seta pulando.
- **Fontes:** Montserrat (500/800/900) e JetBrains Mono (500/700/800). Licença OFL, uso comercial liberado.
- **Decoração:** um planeta cortado no canto superior esquerdo e um astrolábio girando no inferior direito. Use `"decoracao": "nenhuma"` para tirar.

| Tema | Fundo | Texto | Apoio | Acento | Cartão |
|---|---|---|---|---|---|
| `papel` | #f4f0e6 → #ddd6c6 | #141414 | #5a5650 | #e8641e | #fffdf8 |
| `noite` | #0d1430 → #05081a | #f3efe6 | #9aa3b5 | #f1691b | #121a33 |

Para trocar o acento: `"acento": "#2f9e44"`.

## Como usar

```bash
cd templates/short-palco-unico
npm install                      # fontes + playwright
npx playwright install chromium  # só na primeira vez, no PC
node render.js exemplos/demo-paineis/roteiro.json teste.mp4 --quadros 2.5,7,11.5   # confere quadros soltos (PNG)
node render.js exemplos/short-1-ceu/roteiro.json short-1.mp4                        # grava o vídeo inteiro
node render.js exemplos/short-1-ceu/roteiro.json short-1-noite.mp4 --tema noite
```

São cerca de 3 minutos para 30 s de vídeo. Precisa de Node 18+ e FFmpeg.

## roteiro.json

```jsonc
{
  "tema": "papel",                 // papel | noite
  "marca": "MAPA DO CÉU",          // texto pequeno no topo
  "audio": "narracao.mp3",         // sem áudio, use "duracao": 16
  "aviso": "",                     // linha pequena no rodapé (ex.: aviso de imagem gerada por IA)
  "batidas": [                     // tempos em segundos, a partir das frases da narração (tempos.json)
    {"b": 4.15, "apoio": [0.3, "a bandeira do Brasil mostra"], "titulo": [[1.5, "um céu que"], [2.55, "*ninguém viu*"]]}
  ],
  "cartao": {
    "a": 0.7, "b": 25.1,           // entra e sai
    "arquivo":  [[0, "bandeira.png"], [4.4, "carta-celeste.svg"]],   // muda com o tempo
    "etiqueta": [[0, "● 1889"]],
    "rotulo":   [[0, "CÉU DO RIO · 15/11/1889"]],
    "paineis": [                   // área visual; cada painel com seu intervalo a..b
      {"tipo": "imagem", "src": "foto.png", "a": 0, "b": 4.6},
      {"tipo": "lista",  "a": 5, "b": 10, "itens": [{"t": 5.2, "texto": "Item *um*", "nota": "detalhe"}]},
      {"tipo": "numero", "a": 10, "b": 14, "de": 0, "para": 44, "sufixo": "°", "conta": [10.5, 12], "legenda": "ALTURA DO SOL"},
      {"tipo": "barra",  "a": 14, "b": 18, "de": 0, "para": 100, "conta": [14.5, 16], "legenda": "PROGRESSO"},
      {"tipo": "extra",  "a": 4.3, "b": 99}   // desenhado pelo script "extra"
    ],
    "diario": [[5.2, "✓ primeira linha", 6.8], [8.2, "08:30 · segunda linha"]]   // [início, texto, fim opcional]
  },
  "chamada": {"a": 25.1, "pilulas": ["5 min", "Mapa do Céu"], "seta": true},
  "extra": "ceu.js",               // opcional: define window.EXTRA = {init(painel, roteiro), render(t)}
  "dados": "ceu.json"              // opcional: vira window.__DADOS para o extra
}
```

Os tempos saem do `tempos.json` da narração (início de cada frase). Dentro da frase, estime proporcionalmente pelo número de letras. Os pedaços do título entram 0,3 a 0,6 s antes da palavra ser dita.

## Exemplos

- `exemplos/short-1-ceu/`: o Short aprovado, com a carta celeste animada em `ceu.js`.
- `exemplos/demo-paineis/`: mostra os painéis prontos (lista, número, barra) sem áudio.

Ao publicar: marque "Conteúdo alterado ou sintético" quando houver voz sintética ou imagem de IA.

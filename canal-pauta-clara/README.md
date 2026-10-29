# Pauta Clara (canal de política)

Explicador apartidário: "como funciona" e "consequências de". Voz Kokoro pf_dora 0,95.

- `semana-01/`: roteiros, roteiro.json, legendas, títulos e descrições da semana de 2 a 8/11/2026. Os MP4, áudios e capas ficam na pasta do projeto (`canal-pauta-clara/semana-01/`).
- `ferramentas/`: scripts.
  - `shorts_semana01.py`: texto + narração + roteiro.json dos Shorts (`python shorts_semana01.py SAIDA tudo`; precisa de KOKORO_ONNX, KOKORO_VOICES e CALENDARIO_JS).
  - `narrar_frases.py` + `longo_semana01.py`: narração e roteiro visual do longo.
  - `palco/`: template de Shorts (com opções `decoracao: "pauta"`, `cores`, `simbolo`), palco horizontal do longo (`palco-16x9.html`, `render16.js`) e capas (`capa.html`, `capas.js`).
  - `textos_publicacao.py`: títulos, descrições com fontes e calendário de publicação.

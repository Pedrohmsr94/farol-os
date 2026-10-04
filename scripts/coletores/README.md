# Coletores

Dado público de perfil e de post, coletado pra análise interna — o que alimenta
o `/investigar` (modo nicho), o `/diagnostico` e o `/relatorio`. Nada daqui é
publicado.

| Coletor | Alvo | Traz | Precisa |
|---|---|---|---|
| `instagram.js` | handle sem @ | seguidores, seguindo, posts, nome e bio do perfil público | `npm run setup` |
| `apify.py` | ator do Apify + JSON de entrada | posts, legendas, curtidas, comentários, views, links de mídia — o que o ator devolver | `APIFY_TOKEN` (pago por uso) |
| `baixar-referencias.py` | JSON do `apify.py` | capa, slides e vídeo de cada post; quadros do vídeo (gancho, 3 s, 1/3, 2/3, fim) | ffmpeg pros quadros |
| `resumir-perfil.py` | handle + JSON do `apify.py` | folha de contato top-12, ritmo de postagem, mix de formato, medianas | Pillow |
| `baixar-posts-ig.py` | JSON do `apify.py` (a própria conta) | capas de todos os posts, carrosséis que mais engajaram inteiros, `indice.json` | — |

## Uso

```powershell
node scripts/coletores/instagram.js "handle" --out pesquisa/coleta/ig-handle-2026-10-03.json
py scripts/coletores/apify.py apify~instagram-scraper ig-handle-posts @pesquisa/coleta/entrada.json
py scripts/coletores/baixar-referencias.py --json pesquisa/coleta/raw/ig-handle-posts.json
py scripts/coletores/resumir-perfil.py handle ig-handle-posts
py scripts/coletores/baixar-posts-ig.py ig-conta-posts
```

Entrada típica do ator de Instagram (`entrada.json`):

```json
{"directUrls": ["https://www.instagram.com/HANDLE/"], "resultsType": "posts", "resultsLimit": 60}
```

No PowerShell, passar o JSON por arquivo (`@entrada.json`) evita a briga com aspas.

## Regras

- **Um alvo por chamada, volume pequeno.** É coleta educada de dado público pra
  análise, não raspagem em massa. 60 posts por perfil bastam pra ler padrão
- **Só dado público.** Nada atrás de login de terceiro, nada de perfil privado
- **Nunca inventar.** Campo que não veio sai `null`. Bloqueio ou muro de login
  sai `{ "bloqueado": true, "motivo": "..." }`. Nos relatórios, tudo daqui entra
  como `observado`, com a data da coleta
- O Apify cobra por execução: conferir o custo que o `apify.py` imprime
- O DOM do Instagram muda. Se o `instagram.js` quebrar, o conserto é no seletor;
  `--headed` abre janela de verdade quando o headless for barrado

## O caminho do dado

```
coleta            apify.py → pesquisa/coleta/raw/<nome>.json
   ↓              (instagram.js → pesquisa/coleta/, só números do perfil)
mídia             baixar-referencias.py · resumir-perfil.py · baixar-posts-ig.py
   ↓              NO MESMO DIA: os links do CDN do Instagram expiram em poucos dias
fichas            uma ficha por referência, lida a partir da mídia — /investigar modo nicho
   ↓
padrões           o que se repete entre as fichas: gancho, estrutura, formato, ritmo
```

A mídia (`pesquisa/referencias/midia/`) e o vídeo dos reels ficam fora do git —
é matéria-prima de terceiro, pesada e sem direito de republicar. O JSON cru, os
índices, a folha `_top12.jpg` e as fichas entram: são o registro da pesquisa.

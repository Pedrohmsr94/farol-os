---
name: aprovar-post
description: >
  Publica uma peça já aprovada — move de `conteudo/fila/` pra `conteudo/publicados/`,
  atualiza o calendário e, quando a Meta API estiver configurada, posta o carrossel
  no Instagram e no Facebook. Use quando o usuário disser "aprovar post X", "pode
  publicar", "sobe esse conteúdo", "/aprovar-post".
---

# /aprovar-post — Publicação

Faz a ponte entre a peça aprovada e o feed.

## Quando NÃO usar

- A peça ainda não foi criada → `/publicar-tema` ou `/carrossel`
- Não passou pelo `/revisar` → revisar primeiro. **Sem exceção**
- O cliente ainda não aprovou → não rodar até ele dizer que pode

## Workflow

### Passo 1 — Localizar e conferir

1. Achar a peça em `conteudo/fila/`
2. Conferir que existe `revisao.md` com veredito **APROVADO** ou **APROVADO COM
   AJUSTES**, e que os ajustes foram aplicados
3. Se o veredito for REPROVADO, ou não houver revisão, parar:
   > "Essa peça não passou pelo `/revisar` *(ou: foi reprovada)*. Rodo agora?"
4. Conferir que os PNGs existem, se for carrossel

### Passo 2 — Confirmar

Mostrar resumo e pedir confirmação explícita:

```
Peça: <nome>
Canais: Instagram · Facebook
Slides: <n> · Legenda: <primeiras linhas>

Publico agora?
```

Publicação é irreversível na prática — post apagado depois de publicado já foi
visto. Nunca publicar sem essa confirmação, nem quando o operador parecer com pressa.

### Passo 3 — Publicar

**Se a Meta API estiver configurada** (ver Setup), postar carrossel no Instagram e
no Facebook via Graph API, e reportar o link de cada um.

**Se não estiver**, entregar o pacote pronto pra publicação manual:

```
Pra postar:
1. Slides: conteudo/fila/<pasta>/instagram/ (na ordem 01, 02, ...)
2. Legenda: legenda.md (copiar inteiro)
3. LinkedIn: legenda-linkedin.md
```

Publicação manual é o padrão. A maioria dos clientes pequenos não tem conta Business
conectada, e configurar a API pra postar 8 vezes por mês raramente compensa.

### Passo 4 — Registrar

Independente de como publicou:

1. Mover a peça de `conteudo/fila/` pra `conteudo/publicados/`
2. Marcar no arquivo: `status: publicado` e a data real de publicação
3. Atualizar a linha em `conteudo/calendario.md`
4. Deixar a seção **Resultado** vazia — o `/semana` preenche em sete dias

O passo 4 é o que faz o sistema aprender. Peça publicada que não é registrada some
do histórico e não ensina nada pro calendário do mês seguinte.

---

## Setup da Meta API (opcional, uma vez)

Só vale se o volume justificar. Precisa de:

- Conta do Instagram **Business ou Creator**, vinculada a uma Página do Facebook
- App no Meta for Developers com as permissões de publicação
- `.env` na raiz com `META_PAGE_ACCESS_TOKEN` (token de longa duração) e
  `META_IG_USER_ID`

O `.env` **nunca** entra no git — conferir que está no `.gitignore` antes de criar.

Fluxo de carrossel na Graph API: criar um container por imagem → criar o container
do carrossel com os filhos → publicar. Cada imagem precisa estar acessível por URL
pública, então os PNGs sobem antes pra algum lugar servível.

Se o token expirar (acontece), o erro é de autenticação — renovar o token de longa
duração, não tentar contornar.

## Regras

- **Nunca publicar sem revisão aprovada e sem confirmação do operador**
- Não publicar peça cujo campo "Atenção" da pauta de origem não foi resolvido
- Erro de API não vira publicação parcial: se o Instagram foi e o Facebook não,
  dizer exatamente isso, com o link do que foi
- Não apagar a pasta da peça depois de publicar. Ela é o histórico

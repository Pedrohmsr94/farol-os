// Coletor Instagram público — seguidores, seguindo, posts, nome e bio.
// Fonte mais estável: meta tag og:description (renderizada no servidor, sobrevive ao muro de login).
// Uso: node scripts/coletores/instagram.js "handle" [--out pesquisa/coleta/ig-handle-AAAA-MM-DD.json] [--headed]
// Nunca inventa: campo não extraído sai null; muro de login ou perfil inexistente sai { bloqueado: true, motivo }.
const { parseArgs, abrirNavegador, esperarQuieto, base, emitir, parseNumAbrev } = require('./_lib');

async function main() {
  const { alvo, out, headed } = parseArgs(process.argv);
  if (!alvo) {
    emitir({ ...base('instagram', null), bloqueado: true, motivo: 'alvo não informado (handle sem @)' }, out);
    process.exit(0);
  }
  const handle = alvo.replace(/^@/, '');
  const resultado = base('instagram', handle);
  let browser;
  try {
    const nav = await abrirNavegador(headed);
    browser = nav.browser;
    const page = await nav.context.newPage();
    await page.goto(`https://www.instagram.com/${encodeURIComponent(handle)}/`, {
      waitUntil: 'domcontentloaded',
      timeout: 60000,
    });
    await esperarQuieto(page, 12000);

    // metas vêm no HTML do servidor — presentes mesmo com muro de login
    const metas = await page.evaluate(() => {
      const pega = (sel) => {
        const el = document.querySelector(sel);
        return el ? el.getAttribute('content') : null;
      };
      return {
        desc: pega('meta[property="og:description"]') || pega('meta[name="description"]'),
        titulo: pega('meta[property="og:title"]'),
        corpo: document.body ? document.body.innerText.slice(0, 3000) : '',
      };
    });

    if (!metas.desc) {
      resultado.seguidores = null;
      resultado.seguindo = null;
      resultado.posts = null;
      resultado.nome = null;
      resultado.bio = null;
      resultado.bloqueado = true;
      const parece404 = /não está disponível|isn't available|Page Not Found/i.test(metas.corpo || '');
      resultado.motivo = parece404
        ? 'perfil não existe ou está indisponível'
        : 'muro de login sem meta tag og:description — tentar --headed ou aguardar e repetir';
      emitir(resultado, out);
      return;
    }

    // Formatos vistos: "X Followers, Y Following, Z Posts - ..." (EN)
    //                  "X seguidores, Y seguindo, Z publicações – ..." (pt-BR)
    const d = metas.desc;
    const pegaNum = (rx) => {
      const m = d.match(rx);
      return m ? parseNumAbrev(m[1]) : null;
    };
    resultado.seguidores = pegaNum(/([\d.,]+\s?(?:mil|mi|[KMB])?)\s*(?:seguidores|followers)/i);
    resultado.seguindo = pegaNum(/([\d.,]+\s?(?:mil|mi|[KMB])?)\s*(?:seguindo|following)/i);
    resultado.posts = pegaNum(/([\d.,]+\s?(?:mil|mi|[KMB])?)\s*(?:publica[çc][õo]es|posts)/i);

    // nome sai do og:title: "Nome (@handle) • ..."
    let nome = null;
    if (metas.titulo) {
      const m = metas.titulo.match(/^(.*?)\s*\(@/);
      if (m && m[1].trim()) nome = m[1].trim();
    }
    resultado.nome = nome;

    // bio: formato novo da og:description traz depois de 'Instagram: "..."'
    let bio = null;
    const mBio = d.match(/Instagram:\s*[""]([\s\S]*)[""]\s*$/) || d.match(/Instagram:\s*"([\s\S]*)"\s*$/);
    if (mBio) bio = mBio[1].trim();
    if (!bio) {
      // fallback: header renderizado (só quando não caiu no muro de login)
      bio = await page
        .evaluate(() => {
          const header = document.querySelector('header section');
          if (!header) return null;
          const t = header.innerText.split('\n').filter(Boolean);
          // heurística: linhas após os contadores; devolve null se não achar nada plausível
          const idx = t.findIndex((l) => /seguidores|followers/i.test(l));
          const resto = idx >= 0 ? t.slice(idx + 2).join('\n').trim() : null;
          return resto || null;
        })
        .catch(() => null);
    }
    resultado.bio = bio;

    if (resultado.seguidores === null && resultado.posts === null) {
      resultado.bloqueado = true;
      resultado.motivo = `og:description presente mas em formato não reconhecido: "${d.slice(0, 120)}"`;
    }
    emitir(resultado, out);
  } catch (err) {
    resultado.bloqueado = true;
    resultado.motivo = `erro inesperado: ${err.message}`;
    emitir(resultado, out);
  } finally {
    if (browser) await browser.close().catch(() => {});
  }
}

main();

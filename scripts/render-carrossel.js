/**
 * render-carrossel.js — transforma carrossel.html em PNGs prontos pra postar.
 *
 * Um script pro projeto inteiro. Não copiar pra dentro de cada pasta de peça:
 * quando o layout mudar, muda aqui e vale pras próximas.
 *
 *   npm run carrossel -- conteudo/fila/2026-10-03-tres-erros
 *   npm run carrossel -- conteudo/fila/2026-10-03-tres-erros --formato 9:16
 *   node scripts/render-carrossel.js <arquivo.html> [pasta-de-saida]
 *
 * Aceita a pasta da peça (procura carrossel.html dentro) ou o próprio HTML.
 * Cada elemento com class="slide" vira um PNG numerado (slide-01.png, ...).
 * Saída padrão: instagram/ (ou stories/ no 9:16) ao lado do HTML.
 * Quem chama este script no fluxo normal é o `py scripts/carrossel/gerar.py --render`.
 *
 * Antes de fotografar, confere se a fonte da marca carregou. Sem isso o PNG
 * sai com fonte de sistema e ninguém percebe até estar no feed.
 *
 * Formatos: 4:5 (1080x1350, padrão) · 1:1 (1080x1080) · 9:16 (1080x1920)
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const { pathToFileURL } = require('url');

const FORMATOS = {
  '4:5': { width: 1080, height: 1350, pasta: 'instagram' },
  '1:1': { width: 1080, height: 1080, pasta: 'instagram' },
  '9:16': { width: 1080, height: 1920, pasta: 'stories' },
};

function argumentos() {
  const args = process.argv.slice(2);
  const i = args.indexOf('--formato');
  const formato = i !== -1 ? args[i + 1] : '4:5';
  const soltos = args.filter((a, k) => !a.startsWith('--') && !(i !== -1 && k === i + 1));
  const [alvo, saidaArg] = soltos;

  if (!alvo) {
    console.error('Uso: npm run carrossel -- <pasta-da-peca | arquivo.html> [pasta-de-saida] [--formato 4:5|1:1|9:16]');
    process.exit(1);
  }
  if (!FORMATOS[formato]) {
    console.error(`Formato desconhecido: ${formato}. Use 4:5, 1:1 ou 9:16.`);
    process.exit(1);
  }
  let html = path.resolve(alvo);
  if (fs.existsSync(html) && fs.statSync(html).isDirectory()) html = path.join(html, 'carrossel.html');
  if (!fs.existsSync(html)) {
    console.error(`Nao achei ${html}`);
    process.exit(1);
  }
  const saida = path.resolve(saidaArg || path.join(path.dirname(html), FORMATOS[formato].pasta));
  return { html, saida, formato };
}

// Confere se a família ganhou um @font-face carregado. document.fonts.check() sozinho
// mente: devolve true pra fonte que nem existe na página.
async function conferirFonte(page, seletor, papel) {
  const r = await page.evaluate((sel) => {
    const el = document.querySelector(sel);
    if (!el) return null;
    const familia = getComputedStyle(el).fontFamily.split(',')[0].replace(/['"]/g, '').trim();
    const faces = [...document.fonts].filter((f) => f.family.replace(/['"]/g, '').trim() === familia);
    return { familia, faces: faces.length, carregadas: faces.filter((f) => f.status === 'loaded').length };
  }, seletor);
  if (!r) return true;
  const generica = /^(system-ui|sans-serif|serif|monospace|Segoe UI|Arial|Helvetica)$/i.test(r.familia);
  if (r.carregadas > 0) {
    console.log(`fonte de ${papel} "${r.familia}": carregou`);
    return true;
  }
  if (generica) {
    console.log(`fonte de ${papel} "${r.familia}": fonte do sistema (sem Google Fonts)`);
    return true;
  }
  console.warn(`AVISO: fonte de ${papel} "${r.familia}" NAO CARREGOU — o PNG sai com fonte de sistema. ` +
    'Conferir o nome e os pesos em identidade/marca-visual.yaml e a internet.');
  return false;
}

(async () => {
  const { html, saida, formato } = argumentos();
  const { width, height } = FORMATOS[formato];
  fs.mkdirSync(saida, { recursive: true });

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });

  await page.goto(pathToFileURL(html).href, { waitUntil: 'networkidle' });
  // Fonte do Google carrega depois do networkidle em conexão lenta.
  await page.evaluate(() => document.fonts.ready);

  await conferirFonte(page, '.slide', 'corpo');
  await conferirFonte(page, '.slide h1, .slide h2', 'título');

  const slides = await page.$$('.slide');
  if (slides.length === 0) {
    console.error('Nenhum elemento com class="slide" no HTML.');
    await browser.close();
    process.exit(1);
  }

  console.log(`${slides.length} slides · ${width}x${height}`);
  for (let i = 0; i < slides.length; i++) {
    const nome = `slide-${String(i + 1).padStart(2, '0')}.png`;
    await slides[i].screenshot({ path: path.join(saida, nome) });
  }

  await browser.close();
  console.log(`OK: ${slides.length} PNGs em ${path.relative(process.cwd(), saida) || '.'}`);
})();

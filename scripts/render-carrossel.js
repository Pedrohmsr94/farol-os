/**
 * render-carrossel.js — transforma carrossel.html em PNGs prontos pra postar.
 *
 * Um script pro projeto inteiro. Não copiar pra dentro de cada pasta de peça:
 * quando o layout mudar, muda aqui e vale pras próximas.
 *
 *   npm run carrossel -- conteudo/fila/2026-09-03-malha-fina
 *   npm run carrossel -- conteudo/fila/2026-09-03-malha-fina --formato 9:16
 *
 * Espera encontrar carrossel.html na pasta passada, com um <div class="slide">
 * por slide. Salva em instagram/slide-01.png, slide-02.png, ...
 *
 * Formatos: 4:5 (1080x1350, padrão) · 1:1 (1080x1080) · 9:16 (1080x1920)
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const FORMATOS = {
  '4:5': { width: 1080, height: 1350, pasta: 'instagram' },
  '1:1': { width: 1080, height: 1080, pasta: 'instagram' },
  '9:16': { width: 1080, height: 1920, pasta: 'stories' },
};

function argumentos() {
  const args = process.argv.slice(2);
  const pasta = args.find((a) => !a.startsWith('--'));
  const i = args.indexOf('--formato');
  const formato = i !== -1 ? args[i + 1] : '4:5';

  if (!pasta) {
    console.error('Uso: npm run carrossel -- <pasta-da-peca> [--formato 4:5|1:1|9:16]');
    process.exit(1);
  }
  if (!FORMATOS[formato]) {
    console.error(`Formato desconhecido: ${formato}. Use 4:5, 1:1 ou 9:16.`);
    process.exit(1);
  }
  return { pasta: path.resolve(pasta), formato };
}

(async () => {
  const { pasta, formato } = argumentos();
  const { width, height, pasta: subpasta } = FORMATOS[formato];

  const html = path.join(pasta, 'carrossel.html');
  if (!fs.existsSync(html)) {
    console.error(`Nao achei carrossel.html em ${pasta}`);
    process.exit(1);
  }

  const saida = path.join(pasta, subpasta);
  fs.mkdirSync(saida, { recursive: true });

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width, height } });

  await page.goto('file://' + html.replace(/\\/g, '/'), { waitUntil: 'networkidle' });
  // Fonte do Google carrega depois do networkidle em conexao lenta. Sem isso o
  // primeiro slide sai com fonte de sistema e ninguem percebe ate publicar.
  await page.evaluate(() => document.fonts.ready);

  const slides = await page.$$('.slide');
  if (slides.length === 0) {
    console.error('Nenhum <div class="slide"> encontrado no HTML.');
    await browser.close();
    process.exit(1);
  }

  console.log(`${slides.length} slides · ${width}x${height}`);

  for (let i = 0; i < slides.length; i++) {
    const num = String(i + 1).padStart(2, '0');
    const arquivo = path.join(saida, `slide-${num}.png`);
    await slides[i].screenshot({ path: arquivo });
    console.log(`  slide-${num}.png`);
  }

  await browser.close();
  console.log(`\nOK: ${slides.length} PNGs em ${path.relative(process.cwd(), saida)}`);
})();

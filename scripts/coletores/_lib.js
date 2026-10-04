// Utilitários comuns dos coletores Playwright. Não é um coletor — não rodar direto.
const fs = require('fs');
const path = require('path');

let chromium;
try {
  ({ chromium } = require('playwright'));
} catch (_) {
  console.error('Playwright não instalado. Na raiz do repo: npm run setup');
  process.exit(1);
}

const UA =
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36';

// node coletor.js "<alvo>" [--out caminho.json] [--headed]
function parseArgs(argv) {
  const args = argv.slice(2);
  let alvo = null;
  let out = null;
  let headed = false;
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--out') out = args[++i];
    else if (args[i] === '--headed') headed = true;
    else if (alvo === null) alvo = args[i];
  }
  return { alvo, out, headed };
}

// Chromium completo (channel) é menos detectável que o headless shell.
async function abrirNavegador(headed) {
  const opts = {
    headless: !headed,
    args: ['--disable-blink-features=AutomationControlled', '--lang=pt-BR'],
  };
  let browser;
  try {
    browser = await chromium.launch({ ...opts, channel: 'chromium' });
  } catch (_) {
    browser = await chromium.launch(opts);
  }
  const context = await browser.newContext({
    locale: 'pt-BR',
    timezoneId: 'America/Sao_Paulo',
    userAgent: UA,
    viewport: { width: 1366, height: 900 },
    extraHTTPHeaders: { 'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8' },
  });
  context.setDefaultTimeout(45000);
  return { browser, context };
}

// networkidle nem sempre chega em app JS pesado — esperar com tolerância.
async function esperarQuieto(page, ms) {
  try {
    await page.waitForLoadState('networkidle', { timeout: ms || 20000 });
  } catch (_) {
    /* segue com o que carregou */
  }
}

function base(coletor, alvo) {
  return {
    coletor,
    alvo,
    coletado_em: new Date().toISOString(),
    origem: 'observado',
  };
}

// Imprime compacto no stdout e, com --out, salva o mesmo JSON.
function emitir(resultado, out) {
  const json = JSON.stringify(resultado);
  process.stdout.write(json + '\n');
  if (out) {
    const destino = path.resolve(out);
    fs.mkdirSync(path.dirname(destino), { recursive: true });
    fs.writeFileSync(destino, json);
  }
}

// "1.234" -> 1234 | "14,2 mil" -> 14200 | "10.5K" -> 10500 | "1,2 mi" -> 1200000
function parseNumAbrev(s) {
  if (s === null || s === undefined) return null;
  s = String(s).trim().toLowerCase().replace(/\s+/g, '');
  let mult = 1;
  if (/mil$/.test(s)) { mult = 1e3; s = s.replace(/mil$/, ''); }
  else if (/(mi|m)$/.test(s)) { mult = 1e6; s = s.replace(/(mi|m)$/, ''); }
  else if (/k$/.test(s)) { mult = 1e3; s = s.replace(/k$/, ''); }
  else if (/(bi|b)$/.test(s)) { mult = 1e9; s = s.replace(/(bi|b)$/, ''); }
  if (!s) return null;
  if (mult === 1) {
    const n = parseInt(s.replace(/[.,]/g, ''), 10);
    return Number.isNaN(n) ? null : n;
  }
  const n = parseFloat(s.replace(',', '.'));
  return Number.isNaN(n) ? null : Math.round(n * mult);
}

module.exports = {
  parseArgs,
  abrirNavegador,
  esperarQuieto,
  base,
  emitir,
  parseNumAbrev,
};

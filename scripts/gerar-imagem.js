/**
 * gerar-imagem.js — gera imagem por IA pra usar em peça de conteúdo.
 *
 *   node scripts/gerar-imagem.js "PROMPT EM INGLES" conteudo/fila/<pasta>/foto-capa.png
 *   node scripts/gerar-imagem.js "PROMPT" saida.png --tamanho 1024x1536
 *
 * Precisa de OPENAI_API_KEY no arquivo .env da raiz do projeto (o .env nunca
 * entra no git). Custa por imagem — conferir o preço antes de gerar em série.
 *
 * Prompt em inglês: a API responde melhor.
 *
 * Foto real da empresa vem sempre na frente disso. Imagem gerada serve pra
 * fundo, textura e cena genérica — nunca pra fingir equipe, cliente ou
 * resultado que não existe.
 */

const fs = require('fs');
const path = require('path');

const TAMANHOS = ['1024x1024', '1024x1536', '1536x1024'];

function carregarEnv() {
  const arquivo = path.resolve(__dirname, '..', '.env');
  if (!fs.existsSync(arquivo)) return;
  for (const linha of fs.readFileSync(arquivo, 'utf8').split('\n')) {
    const t = linha.trim();
    if (!t || t.startsWith('#')) continue;
    const i = t.indexOf('=');
    if (i === -1) continue;
    const chave = t.slice(0, i).trim();
    const valor = t.slice(i + 1).trim().replace(/^["']|["']$/g, '');
    if (!process.env[chave]) process.env[chave] = valor;
  }
}

(async () => {
  carregarEnv();

  const args = process.argv.slice(2);
  const posicionais = args.filter((a) => !a.startsWith('--'));
  const [prompt, destino] = posicionais;
  const i = args.indexOf('--tamanho');
  const tamanho = i !== -1 ? args[i + 1] : '1024x1536';

  if (!prompt || !destino) {
    console.error('Uso: node scripts/gerar-imagem.js "PROMPT EM INGLES" <caminho-de-saida.png> [--tamanho 1024x1536]');
    process.exit(1);
  }
  if (!TAMANHOS.includes(tamanho)) {
    console.error(`Tamanho invalido. Use: ${TAMANHOS.join(', ')}`);
    process.exit(1);
  }
  if (!process.env.OPENAI_API_KEY) {
    console.error('Falta OPENAI_API_KEY. Criar o arquivo .env na raiz com:');
    console.error('  OPENAI_API_KEY=sk-...');
    console.error('Conferir que .env esta no .gitignore antes de salvar a chave.');
    process.exit(1);
  }

  console.log(`gerando ${tamanho}...`);

  let resposta;
  try {
    resposta = await fetch('https://api.openai.com/v1/images/generations', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
      },
      body: JSON.stringify({ model: 'gpt-image-1', prompt, size: tamanho, n: 1 }),
    });
  } catch (e) {
    console.error(`Falhou a chamada: ${e.message}`);
    process.exit(1);
  }

  if (!resposta.ok) {
    const erro = await resposta.text();
    console.error(`Erro ${resposta.status} da OpenAI:\n${erro}`);
    process.exit(1);
  }

  const dados = await resposta.json();
  const b64 = dados?.data?.[0]?.b64_json;
  if (!b64) {
    console.error('A resposta veio sem imagem. Conteudo:\n' + JSON.stringify(dados).slice(0, 500));
    process.exit(1);
  }

  fs.mkdirSync(path.dirname(path.resolve(destino)), { recursive: true });
  fs.writeFileSync(path.resolve(destino), Buffer.from(b64, 'base64'));

  console.log(`OK: ${destino}`);
  console.log('Mostrar pro operador antes de usar no carrossel.');
})();

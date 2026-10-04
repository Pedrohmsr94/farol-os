# -*- coding: utf-8 -*-
"""Baixa as imagens dos posts da PRÓPRIA conta já coletados pelo Apify.

    py scripts/coletores/baixar-posts-ig.py <nome-do-json> [--destino <pasta>]
    py scripts/coletores/baixar-posts-ig.py ig-conta-posts
    py scripts/coletores/baixar-posts-ig.py pesquisa/coleta/raw/ig-conta-posts.json --destino dados/ig-conta-posts

<nome-do-json> é o <nome> usado no apify.py (lê pesquisa/coleta/raw/<nome>.json)
ou o caminho de um JSON qualquer no mesmo formato.

As URLs do CDN do Instagram são assinadas e expiram em poucos dias. Este script
puxa o que está no JSON cru enquanto os links vivem — rodar no mesmo dia da coleta.

Saída (padrão: dados/<nome-do-json>/, fora do git):
    capas/       a 1ª imagem de cada post, numerada do mais novo pro mais velho
    carrosseis/  todos os slides dos carrosséis que mais engajaram
    indice.json  data, formato, curtidas, comentários, views, legenda de cada post

É a matéria-prima do /diagnostico e do /relatorio pra ler o feed como um todo.
Pra posts de perfis de referência (não da própria conta), usar baixar-referencias.py.
"""
import argparse
import json
import os
import re
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RAW = os.path.join(RAIZ, "pesquisa", "coleta", "raw")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

TOP_CARROSSEIS = 6   # quantos carrosséis baixar inteiros
MIN_LIKES = 60       # ou qualquer um acima disso


def baixar(url, caminho):
    if not url:
        return "erro: sem url"
    if os.path.exists(caminho) and os.path.getsize(caminho) > 1000:
        return "cache"
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            dados = r.read()
        with open(caminho, "wb") as f:
            f.write(dados)
        return "ok"
    except Exception as e:
        return f"erro: {type(e).__name__}"


def slug(txt, n=42):
    txt = re.sub(r"\s+", " ", (txt or "").strip())
    txt = re.sub(r"[^\w\s-]", "", txt, flags=re.U)
    return re.sub(r"\s+", "-", txt).lower()[:n] or "sem-legenda"


def resolver_json(arg):
    if os.path.exists(arg):
        return os.path.abspath(arg)
    candidato = os.path.join(RAW, arg if arg.endswith(".json") else arg + ".json")
    if os.path.exists(candidato):
        return candidato
    raise SystemExit(f"JSON não encontrado: {arg} (nem em {os.path.relpath(candidato, RAIZ)})")


def main():
    p = argparse.ArgumentParser(description="Baixa capas e carrosséis da própria conta a partir do JSON do Apify.")
    p.add_argument("json", help="nome do JSON em pesquisa/coleta/raw/ (sem .json) ou caminho")
    p.add_argument("--destino", help="pasta de saída (padrão: dados/<nome-do-json>/)")
    args = p.parse_args()

    cru = resolver_json(args.json)
    nome = os.path.splitext(os.path.basename(cru))[0]
    destino = os.path.abspath(args.destino) if args.destino else os.path.join(RAIZ, "dados", nome)

    with open(cru, encoding="utf-8") as f:
        itens = [p for p in json.load(f)["itens"] if not p.get("error")]

    itens.sort(key=lambda p: p.get("timestamp") or "", reverse=True)
    os.makedirs(os.path.join(destino, "capas"), exist_ok=True)
    os.makedirs(os.path.join(destino, "carrosseis"), exist_ok=True)

    indice = []
    falhas = 0
    for i, p in enumerate(itens, 1):
        data = (p.get("timestamp") or "")[:10]
        nome_capa = f"{i:02d}_{data}_{p.get('type', '?')}_{slug(p.get('caption'))}.jpg"
        r = baixar(p.get("displayUrl", ""), os.path.join(destino, "capas", nome_capa))
        if r.startswith("erro"):
            falhas += 1
        indice.append({
            "n": i, "data": data, "tipo": p.get("type"),
            "likes": p.get("likesCount"), "comentarios": p.get("commentsCount"),
            "views": p.get("videoPlayCount") or p.get("videoViewCount"),
            "slides": len(p.get("images") or []),
            "url": p.get("url"), "capa": nome_capa if not r.startswith("erro") else None,
            "legenda": (p.get("caption") or "").strip(),
        })

    # carrosséis inteiros: os que mais engajaram
    carros = [x for x in indice if x["tipo"] == "Sidecar"]
    carros.sort(key=lambda x: x["likes"] or 0, reverse=True)
    escolhidos = [x for x in carros if (x["likes"] or 0) >= MIN_LIKES][:TOP_CARROSSEIS]
    if not escolhidos:
        escolhidos = carros[:TOP_CARROSSEIS]

    porurl = {p.get("url"): p for p in itens}
    for x in escolhidos:
        pasta = os.path.join(destino, "carrosseis", f"{(x['likes'] or 0):04d}-{x['data']}-{slug(x['legenda'], 34)}")
        os.makedirs(pasta, exist_ok=True)
        for j, img in enumerate(porurl[x["url"]].get("images") or [], 1):
            baixar(img, os.path.join(pasta, f"s{j:02d}.jpg"))
        x["pasta_slides"] = os.path.relpath(pasta, RAIZ).replace("\\", "/")

    with open(os.path.join(destino, "indice.json"), "w", encoding="utf-8") as f:
        json.dump(indice, f, ensure_ascii=False, indent=2)

    print(f"capas: {len(indice)} ({falhas} falharam) -> {os.path.relpath(destino, RAIZ)}")
    print(f"carrosséis inteiros: {len(escolhidos)}")
    for x in escolhidos:
        print(f"  {(x['likes'] or 0):>4} likes · {x['slides']} slides · {x['data']} · {x['legenda'][:60]}")
    if falhas and falhas == len(indice):
        print("Nenhuma capa baixou: link expirado. Coletar de novo e rodar no mesmo dia.")


if __name__ == "__main__":
    main()

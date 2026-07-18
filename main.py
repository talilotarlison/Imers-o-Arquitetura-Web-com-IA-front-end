# ===================================================
# Alura Album — API — Versão final
# ===================================================

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import glob

app = FastAPI()

# Libera o acesso para o frontend (qualquer origem pode chamar a API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Caminhos absolutos: o servidor acha a pasta de imagens
# independente de onde o comando for executado
PASTA_BASE = os.path.dirname(os.path.abspath(__file__))
PASTA_IMAGENS = os.path.join(PASTA_BASE, "figurinhas")

# Lista de figurinhas do álbum.
# As figurinhas sem imagem na pasta figurinhas/ ficam comentadas
# até a imagem ser adicionada.
figurinhas = [
    {"id": 1,  "nome": "Alan Turing",         "categoria": "IA",                "imagem_url": "/figurinhas/1/imagem"},
    {"id": 2,  "nome": "John McCarthy",       "categoria": "IA",                "imagem_url": "/figurinhas/2/imagem"},
    {"id": 3,  "nome": "Sam Altman",          "categoria": "IA",                "imagem_url": "/figurinhas/3/imagem"},
    {"id": 4,  "nome": "Geoffrey Hinton",     "categoria": "IA",                "imagem_url": "/figurinhas/4/imagem"},
    {"id": 5,  "nome": "Yann LeCun",          "categoria": "IA",                "imagem_url": "/figurinhas/5/imagem"},
    {"id": 6,  "nome": "Guido van Rossum",    "categoria": "Linguagens",        "imagem_url": "/figurinhas/6/imagem"},
    {"id": 7,  "nome": "Tim Berners-Lee",     "categoria": "Web",               "imagem_url": "/figurinhas/7/imagem"},
    {"id": 8,  "nome": "Ray Kurzweil",        "categoria": "IA",                "imagem_url": "/figurinhas/8/imagem"},
    {"id": 9,  "nome": "Travis Oliphant",     "categoria": "Dados",             "imagem_url": "/figurinhas/9/imagem"},
    {"id": 10, "nome": "Wes McKinney",        "categoria": "Dados",             "imagem_url": "/figurinhas/10/imagem"},
    {"id": 11, "nome": "Edgar Codd",          "categoria": "Banco de Dados",    "imagem_url": "/figurinhas/11/imagem"},
    {"id": 12, "nome": "Larry Ellison",       "categoria": "Banco de Dados",    "imagem_url": "/figurinhas/12/imagem"},
    {"id": 13, "nome": "Michael Stonebraker", "categoria": "Banco de Dados",    "imagem_url": "/figurinhas/13/imagem"},
    {"id": 14, "nome": "Salvatore Sanfilippo","categoria": "Banco de Dados",    "imagem_url": "/figurinhas/14/imagem"},
    {"id": 15, "nome": "Eliot Horowitz",      "categoria": "Banco de Dados",    "imagem_url": "/figurinhas/15/imagem"},
    {"id": 16, "nome": "Linus Torvalds",      "categoria": "Sistemas",          "imagem_url": "/figurinhas/16/imagem"},
    {"id": 17, "nome": "Dennis Ritchie",      "categoria": "Linguagens",        "imagem_url": "/figurinhas/17/imagem"},
    {"id": 18, "nome": "Richard Stallman",    "categoria": "Software Livre",    "imagem_url": "/figurinhas/18/imagem"},
    {"id": 19, "nome": "Bill Gates",          "categoria": "Empreendedorismo",  "imagem_url": "/figurinhas/19/imagem"},
    {"id": 20, "nome": "Steve Jobs",          "categoria": "Empreendedorismo",  "imagem_url": "/figurinhas/20/imagem"},
    # Time Alura — confira os nomes completos antes de publicar
    {"id": 21, "nome": "Paulo",               "categoria": "Alura",             "imagem_url": "/figurinhas/21/imagem"},
    {"id": 22, "nome": "Guilherme",           "categoria": "Alura",             "imagem_url": "/figurinhas/22/imagem"},
    {"id": 23, "nome": "Gus",                 "categoria": "Alura",             "imagem_url": "/figurinhas/23/imagem"},
    {"id": 24, "nome": "Mauricio",            "categoria": "Alura",             "imagem_url": "/figurinhas/24/imagem"},
    {"id": 25, "nome": "Andre",               "categoria": "Alura",             "imagem_url": "/figurinhas/25/imagem"},
    {"id": 26, "nome": "Guilherme",           "categoria": "Alura",             "imagem_url": "/figurinhas/26/imagem"},
    {"id": 27, "nome": "Gi",                  "categoria": "Alura",             "imagem_url": "/figurinhas/27/imagem"},
    {"id": 28, "nome": "Vinicius",            "categoria": "Alura",             "imagem_url": "/figurinhas/28/imagem"},
    {"id": 29, "nome": "Rafa",                "categoria": "Alura",             "imagem_url": "/figurinhas/29/imagem"},
    # Ainda sem imagem na pasta figurinhas/ — descomente quando adicionar o arquivo 30-*
    # {"id": 30, "nome": "???",               "categoria": "Alura",             "imagem_url": "/figurinhas/30/imagem"},
]


@app.get("/figurinhas")
def listar_figurinhas():
    # Devolve o JSON com todas as figurinhas do álbum
    return figurinhas


@app.get("/figurinhas/{id}/imagem")
def imagem_da_figurinha(id: int):
    # Procura o arquivo que começa com o número da figurinha (ex: "07-Tim.jpeg").
    # O [!0-9] logo depois do número evita que o id 1 case com "10-Wes.jpg".
    padrao = os.path.join(PASTA_IMAGENS, f"{id:02d}[!0-9]*")
    arquivos = glob.glob(padrao)

    # Nenhum arquivo encontrado para esse id
    if not arquivos:
        raise HTTPException(status_code=404, detail="Figurinha não encontrada")

    # Entrega os bytes da imagem (o FastAPI descobre o Content-Type pela extensão)
    return FileResponse(arquivos[0])

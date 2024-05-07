from fastapi import FastAPI
from pydantic import BaseModel
from utils.db import engine
from models.documentoModel import Ssdc
import formatar


class Prompt(BaseModel):
    pergunta: str


app = FastAPI()


@app.post("/chat")
async def chat(prompt: Prompt):
    prompt_formatado, titulos_formatados = formatacoes(prompt.pergunta)
    print(prompt_formatado, titulos_formatados)
    return prompt.pergunta


def formatacoes(texto):
    formatacao_pergunta = formatar.remover_pontuacao(texto)
    formatacao_pergunta = formatar.remover_stopwords(formatacao_pergunta)
    formatacao_pergunta = formatar.radicalizar(formatacao_pergunta)

    titulos_formatados = []
    registros = Ssdc.ler_documentos()
    for registro in registros:
        titulo = registro.sstitu
        titulo = formatar.remover_pontuacao(titulo)
        titulo = formatar.remover_stopwords(titulo)
        titulo = formatar.radicalizar(titulo)
        titulos_formatados.append(titulo)
    return formatacao_pergunta, titulos_formatados


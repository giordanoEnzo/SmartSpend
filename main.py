from fastapi import FastAPI
from pydantic import BaseModel
from utils.db import engine
import formatar


class Prompt(BaseModel):
    pergunta: str


app = FastAPI()


@app.post("/chat")
async def chat(prompt: Prompt):
    prompt_formatado = formatacoes(prompt.pergunta)
    print(prompt_formatado)
    return prompt.pergunta


def formatacoes(texto):
    formatacao = formatar.remover_pontuacao(texto)
    formatacao = formatar.remover_stopwords(formatacao)
    formatacao = formatar.radicalizar(formatacao)
    return formatacao

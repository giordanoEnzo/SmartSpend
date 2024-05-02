from fastapi import FastAPI
from pydantic import BaseModel
from utils.db import db
import formatar


class Prompt(BaseModel):
    pergunta: str


app = FastAPI()

db.init_app(app)


@app.on_event("startup")
async def startup():
    db.create_all()

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
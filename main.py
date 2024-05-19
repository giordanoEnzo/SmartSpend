from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from models.documentoModel import Ssdc
from ia.gpt import GPT
from BM25.score import ScoreBM25
from pdfs.manipulador import extrair, gerar_processado, extrair_bytea
import formatar
import shutil
import os


class Prompt(BaseModel):
    pergunta: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.post("/chat")
async def chat(prompt: Prompt):
    prompt_formatado, titulos_formatados, total_documentos = formatacoes(prompt.pergunta)

    repeticao_termos_pergunta = calcular_repeticao_geral(prompt_formatado, titulos_formatados)

    tokens_por_documento = calcular_repeticao_por_documento(prompt_formatado, titulos_formatados)

    total_tokens_titulos, tokens_por_titulo = calcular_tokens_titulos(titulos_formatados)

    score_titulos = calcular_score(total_documentos, repeticao_termos_pergunta, total_tokens_titulos, tokens_por_documento)

    conteudos_docs = {}
    quantidade_tokens_pdf = {}
    for chave, valor in score_titulos:
        registro = Ssdc.ler_documento(chave)
        valor_bytea = registro.sspdfp
        conteudo_chave = extrair_bytea(valor_bytea)
        conteudo_chave = conteudo_chave.split()
        conteudos_docs[chave] = conteudo_chave
        quantidade_tokens_pdf[chave] = registro.ssqttk

    repeticao_termos_prompt = calcular_repeticao_geral(prompt_formatado, conteudos_docs)
    tokens_por_pdf = calcular_repeticao_por_documento(prompt_formatado, conteudos_docs)
    total_tokens_pdf = Ssdc.somar_ssqttk()
    score = calcular_score(total_documentos, repeticao_termos_prompt, total_tokens_pdf, tokens_por_pdf)

    melhor_documento = next(iter(score))
    registro_md = Ssdc.ler_documento(melhor_documento[0])
    bytea_md = registro_md.sspdfo
    conteudo_md = extrair_bytea(bytea_md)
    prompt_gpt = montar_prompt_gpt(prompt.pergunta, conteudo_md)
    resposta = GPT(prompt_gpt).gerar_resposta()
    return {"resposta": resposta}


@app.post("/administrador")
async def administrador(nome_pdf: str = Form(...), arquivo_pdf: UploadFile = File(...)):

    with open(os.path.join('/Users/enzogiordanoaraujo/SmartSpend/smartspendAPI/documentos/', arquivo_pdf.filename),"wb") as buffer:
        shutil.copyfileobj(arquivo_pdf.file, buffer)

    conteudo_documento = extrair(arquivo_pdf.filename)
    conteudo_processado = processar_documento(conteudo_documento)
    gerar_processado(conteudo_processado, arquivo_pdf.filename)

    caminho_original = '/Users/enzogiordanoaraujo/SmartSpend/smartspendAPI/documentos/' + arquivo_pdf.filename
    with open(caminho_original, 'rb') as arquivo:
        binario_original = arquivo.read()

    caminho_processado = '/Users/enzogiordanoaraujo/SmartSpend/smartspendAPI/documentos-processados/' + arquivo_pdf.filename
    with open(caminho_processado, 'rb') as arquivo:
        binario_processado = arquivo.read()

    Ssdc.gravar_documento(nome_pdf, len(conteudo_processado), binario_original, binario_processado)

    os.remove(caminho_original)
    os.remove(caminho_processado)

    return 'ok'


def processar_documento(conteudo_pdf):
    conteudo_formatado = formatar.remover_pontuacao(conteudo_pdf)
    conteudo_formatado = formatar.remover_stopwords(conteudo_formatado)
    conteudo_formatado = formatar.radicalizar(conteudo_formatado)

    return conteudo_formatado


def formatacoes(texto):
    formatacao_pergunta = formatar.remover_pontuacao(texto)
    formatacao_pergunta = formatar.remover_stopwords(formatacao_pergunta)
    formatacao_pergunta = formatar.radicalizar(formatacao_pergunta)

    titulos_formatados = {}
    registros = Ssdc.ler_documentos()
    for registro in registros:
        titulo = registro.sstitu
        titulo = formatar.remover_pontuacao(titulo)
        titulo = formatar.remover_stopwords(titulo)
        titulo = formatar.radicalizar(titulo)
        titulos_formatados[registro.id] = (titulo)

    return formatacao_pergunta, titulos_formatados, len(registros)


def calcular_tokens_titulos(titulos_formatados):
    total_tokens = 0
    tokens_por_titulo = {}
    for id in titulos_formatados:
        total_tokens += len(titulos_formatados[id])
        tokens_por_titulo[id] = len(titulos_formatados[id])
    return total_tokens, tokens_por_titulo


def calcular_repeticao_geral(termos_perguntas, termos_textos):
    repeticao_termos_perguntas = {}

    for termo_pergunta in termos_perguntas:
        repeticao_termo = 0

        for id in termos_textos:
            for termo_chave in termos_textos[id]:
                if termo_pergunta == termo_chave:
                    repeticao_termo += 1

        repeticao_termos_perguntas[termo_pergunta] = repeticao_termo

    return repeticao_termos_perguntas


def calcular_repeticao_por_documento(termos_perguntas, termos_textos):
    tokens_por_documentos = {}

    for termo_pergunta in termos_perguntas:

        qtd_por_documentos = {}
        for id in termos_textos:
            repeticao_termo = 0
            for termo_chave in termos_textos[id]:
                if termo_pergunta == termo_chave:
                    repeticao_termo += 1
            qtd_por_documentos[id] = repeticao_termo
        tokens_por_documentos[termo_pergunta] = qtd_por_documentos

    return tokens_por_documentos


def calcular_score(total_documentos, repeticoes_termos_perguntas, total_tokens_documentos, tokens_por_documento):
    idf = {}
    for termo in repeticoes_termos_perguntas:
        if repeticoes_termos_perguntas[termo] > 0:
            idf_termo = ScoreBM25(total_documentos=total_documentos, total_documento_termo=repeticoes_termos_perguntas[termo]).inverse_term_frequency()
            idf[termo] = idf_termo

    tf = {}
    for termo_pesquisa, documento_termos in tokens_por_documento.items():
        term_frequency = {}
        for id, termos_documento in documento_termos.items():
            if termos_documento > 0:
                tf_documento = ScoreBM25(total_termos_documento=termos_documento, total_documentos=total_documentos, total_tokens_documento=total_tokens_documentos).term_frequency()
                term_frequency[id] = tf_documento

        if term_frequency:
            tf[termo_pesquisa] = term_frequency

    pontuacoes_doc = {}
    anterior = 0

    for termo_tf, tf_doc in tf.items():
        tf_doc_ordenado = dict(sorted(tf_doc.items()))

        for id_doc, term_f in tf_doc_ordenado.items():
            score_doc = ScoreBM25(idf=idf[termo_tf], tf=term_f).score()

            if id_doc in pontuacoes_doc:
                soma = pontuacoes_doc[id_doc] + score_doc
                pontuacoes_doc[id_doc] = soma
            else:
                pontuacoes_doc[id_doc] = score_doc

            anterior = id_doc

    pontuacoes_ordenadas = sorted(pontuacoes_doc.items(), key=lambda x: x[1], reverse=True)

    maiores_pontuacoes = pontuacoes_ordenadas[:3]

    return maiores_pontuacoes


def montar_prompt_gpt(pergunta, conteudo_doc):
    prompt = f'Por favor, forneça uma resposta para esta pergunta [{pergunta}] com base no seguinte texto: [{conteudo_doc}]'
    return prompt
from openai import OpenAI
import os


class GPT():
    def __init__(self, prompt):
        self.client = OpenAI(api_key='')
        self.model = "gpt-3.5-turbo-instruct"
        self.prompt = prompt

    def gerar_resposta(self):
        resposta = self.client.completions.create(model=self.model, prompt=self.prompt, max_tokens=1000)
        return resposta.choices[0].text.strip()
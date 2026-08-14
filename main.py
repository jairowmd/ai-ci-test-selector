# O main.py é o orquestrador.

import json

from git.git_utils import (
    obter_arquivos_alterados,
    obter_testes_disponiveis,
    executar_testes
)

from ai.gemini_client import perguntar_gemini


def main():
    arquivos = obter_arquivos_alterados()
    testes = obter_testes_disponiveis()

    pergunta = f"""
Você é um especialista em testes de software.

Arquivos alterados:
{arquivos}

Testes disponíveis:
{testes}

Com base nos arquivos alterados, escolha quais testes devem ser executados.

Retorne exclusivamente um JSON válido neste formato:

{{
  "testes": [
    "nome_do_teste_1",
    "nome_do_teste_2"
  ]
}}

Não inclua explicações.
Não inclua Markdown.
Não invente testes que não estejam na lista de testes disponíveis.
"""

    resposta = perguntar_gemini(pergunta)

    dados = json.loads(resposta)

    testes_selecionados = dados["testes"]

    expressao_pytest = " or ".join(testes_selecionados)

    print(expressao_pytest)

    print(testes_selecionados)

    dados = json.loads(resposta)

    testes_selecionados = dados["testes"]

    resultado_testes = executar_testes(testes_selecionados)

    print(resultado_testes)



if __name__ == "__main__":
    main()
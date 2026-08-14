# O main.py é o orquestrador.

import json

from git.git_utils import (
    obter_testes_disponiveis,
    executar_testes,
    obter_arquivos_alterados_no_commit
)

from ai.gemini_client import perguntar_gemini


def main():
    arquivos = obter_arquivos_alterados_no_commit()
    testes = obter_testes_disponiveis()
    pergunta = f"""
Você é um especialista em testes de software.

Arquivos alterados:
{arquivos}

Testes disponíveis:
{testes}

Com base nos arquivos alterados, escolha quais testes devem ser executados.

Analise a relação entre os arquivos alterados e os testes disponíveis.

Um teste deve ser selecionado quando ele testa diretamente uma função,
módulo ou comportamento relacionado a um dos arquivos alterados.

Se um arquivo alterado estiver relacionado aos testes disponíveis,
selecione esses testes.

Se nenhum teste estiver relacionado aos arquivos alterados,
retorne uma lista vazia.



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

Os testes disponíveis podem estar relacionados aos arquivos alterados
mesmo quando o nome do teste não contém exatamente o nome do arquivo.
Considere também o módulo que o teste importa e as funções que ele testa.

"""

    resposta = perguntar_gemini(pergunta)

    dados = json.loads(resposta)

    testes_selecionados = dados["testes"]

    if not testes_selecionados:

        print("Nenhum teste selecionado.")

        return

    resultado_testes = executar_testes(testes_selecionados)

    print(resultado_testes)


if __name__ == "__main__":
    main()
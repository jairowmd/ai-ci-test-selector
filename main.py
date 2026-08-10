from ai.gemini_client import perguntar_gemini
from git.git_utils import obter_arquivos_alterados


def main():
    arquivos = obter_arquivos_alterados()

    arquivos_texto = "\n".join(arquivos)

    pergunta = f"""
Os seguintes arquivos foram alterados:

{arquivos_texto}

Quais testes deveriam ser executados?
"""
    resposta = perguntar_gemini(pergunta)
    print(resposta)


if __name__ == "__main__":
    main()
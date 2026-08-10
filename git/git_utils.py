# O subprocess é um módulo nativo da biblioteca padrão do Python que serve para executar e interagir com programas externos, comandos do sistema operacional ou scripts
import subprocess

def obter_arquivos_alterados():
    resultado = subprocess.run(
        ["git", "status", "--short"],
        # "Python, capture a saída do comando em vez de simplesmente jogar na tela."
        capture_output=True,
        # "Quero receber essa saída como texto."
        text=True
    )

    linhas = resultado.stdout.splitlines()

    arquivos = []

    for linha in linhas:
        arquivo = linha[3:]
        arquivos.append(arquivo)


    return arquivos
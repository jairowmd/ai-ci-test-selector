# Ele verifica se nossas funções estão funcionando.

import subprocess

from git.git_utils import (
    obter_arquivos_alterados,
    extrair_arquivos_alterados
)


def test_obter_arquivos_alterados_retorna_lista():
    arquivos = obter_arquivos_alterados()

    assert isinstance(arquivos, list)


def test_extrair_arquivos_alterados():
    status = " M main.py\n?? git/"

    arquivos = extrair_arquivos_alterados(status)

    assert arquivos == ["main.py", "git/"]


def obter_testes_disponiveis():
    resultado = subprocess.run(
    ["python", "-m", "pytest", "--collect-only"],
    capture_output=True,
    text=True

    
)
    return resultado.stdout

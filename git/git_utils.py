# Funções utilitárias para Git, pytest e seleção de testes

import subprocess
import sys
import os



def obter_status_git():
    resultado = subprocess.run(
        ["git", "status", "--short"],
        capture_output=True,
        text=True
    )

    return resultado.stdout


def extrair_arquivos_alterados(status):
    linhas = status.splitlines()

    arquivos = []

    for linha in linhas:
        arquivo = linha[3:]
        arquivos.append(arquivo)

    return arquivos


def obter_arquivos_alterados():
    status = obter_status_git()

    return extrair_arquivos_alterados(status)


def obter_testes_disponiveis():
    resultado = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only"],
        capture_output=True,
        text=True
    )

    linhas = resultado.stdout.splitlines()

    testes = []

    for linha in linhas:
        if "<Function" in linha:
            nome_teste = linha.strip()
            nome_teste = nome_teste.replace("<Function ", "")
            nome_teste = nome_teste.replace(">", "")

            testes.append(nome_teste)

    return testes

def obter_arquivos_alterados_no_commit():
    commit_anterior = os.getenv("GIT_BEFORE")
    commit_atual = os.getenv("GIT_AFTER")

    if commit_anterior == "0000000000000000000000000000000000000000":
        commit_anterior = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

    resultado = subprocess.run(
        [
            "git",
            "diff",
            "--name-only",
            commit_anterior,
            commit_atual
        ],
        capture_output=True,
        text=True
    )

    return resultado.stdout.splitlines()

    testes = []

    for linha in linhas:
        if "<Function" in linha:
            nome_teste = linha.strip()
            nome_teste = nome_teste.replace("<Function ", "")
            nome_teste = nome_teste.replace(">", "")

            testes.append(nome_teste)

    return testes


def executar_testes(testes):
    expressao_pytest = " or ".join(testes)

    resultado = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-k",
            expressao_pytest
        ],
        capture_output=True,
        text=True
    )

    return resultado.stdout
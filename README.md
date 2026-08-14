# 🤖 AI CI Test Selector

Ferramenta desenvolvida em Python que utiliza Inteligência Artificial (Google Gemini) para selecionar quais testes automatizados devem ser executados com base nos arquivos alterados em um commit.

O projeto integra **Git, Python, pytest, Google Gemini e GitHub Actions**, criando um fluxo simples de CI orientado por IA.

---

## 🎯 Objetivo

Em um projeto de software, nem sempre é necessário executar todos os testes após uma alteração.

A proposta deste projeto é utilizar IA para analisar:

- quais arquivos foram alterados;
- quais testes estão disponíveis;
- a relação entre os arquivos alterados e os testes;

e então selecionar os testes que devem ser executados.

### Fluxo

```text
                Git
                 │
                 ▼
        Arquivos alterados
                 │
                 ▼
        Testes disponíveis
                 │
                 ▼
          Google Gemini
                 │
                 ▼
       Testes selecionados
                 │
                 ▼
              pytest
                 │
                 ▼
          Resultado dos testes
```

---

## 🧠 Como funciona

O processo é dividido em algumas etapas.

### 1. Identificação dos arquivos alterados

O projeto utiliza o Git para identificar os arquivos modificados entre dois commits:

```text
GIT_BEFORE → commit anterior
GIT_AFTER  → commit atual
```

A comparação é realizada através de:

```bash
git diff --name-only
```

Em um GitHub Actions, esses valores são obtidos automaticamente através de:

```yaml
GIT_BEFORE: ${{ github.event.before }}
GIT_AFTER: ${{ github.sha }}
```

---

### 2. Descoberta dos testes disponíveis

O projeto executa:

```bash
python -m pytest --collect-only
```

O objetivo é descobrir quais testes existem no projeto sem executá-los.

Por exemplo:

```text
test_obter_arquivos_alterados_retorna_lista
test_extrair_arquivos_alterados
```

Esses nomes são enviados posteriormente para a IA.

---

### 3. Análise utilizando Gemini

O programa monta uma solicitação contendo:

- arquivos alterados;
- testes disponíveis;
- regras para seleção dos testes.

Exemplo:

```text
Arquivos alterados:
['git/git_utils.py']

Testes disponíveis:
[
    'test_obter_arquivos_alterados_retorna_lista',
    'test_extrair_arquivos_alterados'
]
```

O Gemini analisa a relação entre essas informações.

A resposta esperada é exclusivamente um JSON:

```json
{
  "testes": [
    "test_obter_arquivos_alterados_retorna_lista",
    "test_extrair_arquivos_alterados"
  ]
}
```

---

### 4. Validação dos testes selecionados

Depois de receber a resposta da IA, o Python valida se os testes retornados realmente existem entre os testes disponíveis.

Isso evita que a IA indique um teste inexistente.

---

### 5. Execução dos testes

Os testes selecionados são enviados para o pytest utilizando a opção:

```bash
pytest -k
```

Por exemplo:

```bash
python -m pytest -k "test_obter_arquivos_alterados_retorna_lista or test_extrair_arquivos_alterados"
```

O resultado da execução é então apresentado no CI.

---

# 🏗️ Estrutura do projeto

```text
ai-ci-test-selector/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── ai/
│   └── gemini_client.py
│
├── git/
│   ├── __init__.py
│   └── git_utils.py
│
├── tests/
│   └── test_git_utils.py
│
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

---

# 📂 Responsabilidade dos arquivos

## `main.py`

É o **orquestrador da aplicação**.

Ele coordena o fluxo:

```text
Git
 ↓
arquivos alterados
 ↓
pytest
 ↓
testes disponíveis
 ↓
Gemini
 ↓
testes selecionados
 ↓
pytest
```

---

## `git/git_utils.py`

Contém as funções relacionadas ao Git e ao pytest.

Responsabilidades principais:

- obter arquivos alterados;
- comparar commits;
- descobrir testes disponíveis;
- executar testes selecionados.

---

## `ai/gemini_client.py`

Responsável pela comunicação com a API do Google Gemini.

O módulo:

1. recebe uma pergunta;
2. envia a solicitação para a API;
3. processa a resposta;
4. retorna o conteúdo recebido.

A chave da API não fica armazenada no código.

---

## `tests/test_git_utils.py`

Contém os testes automatizados das funções relacionadas ao Git.

Atualmente são utilizados testes para validar:

```text
obter_arquivos_alterados()
extrair_arquivos_alterados()
```

---

## `.github/workflows/ci.yml`

Define o pipeline de Continuous Integration.

O workflow:

1. baixa o código;
2. configura o Python;
3. instala as dependências;
4. configura as variáveis necessárias;
5. executa o seletor de testes com IA.

---

# ⚙️ Tecnologias utilizadas

| Tecnologia | Utilização |
|---|---|
| Python | Linguagem principal |
| pytest | Testes automatizados |
| Git | Identificação das alterações |
| Google Gemini | Seleção dos testes utilizando IA |
| GitHub Actions | Execução do CI |
| Requests | Comunicação HTTP com a API Gemini |

---

# 🚀 Como executar localmente

## 1. Clonar o projeto

```bash
git clone <URL_DO_REPOSITORIO>
cd ai-ci-test-selector
```

---

## 2. Criar ambiente virtual

### Windows

```powershell
python -m venv .venv
```

Ativar:

```powershell
.venv\Scripts\Activate.ps1
```

---

## 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

## 4. Configurar a API do Gemini

No Windows PowerShell:

```powershell
$env:GEMINI_API_KEY="SUA_CHAVE"
```

A chave não deve ser adicionada ao Git ou ao código-fonte.

---

## 5. Configurar os commits para execução local

O programa utiliza:

```text
GIT_BEFORE
GIT_AFTER
```

Exemplo:

```powershell
$env:GIT_BEFORE="commit_anterior"
$env:GIT_AFTER="commit_atual"
```

---

## 6. Executar

```bash
python main.py
```

---

# 🧪 Executar os testes manualmente

Para executar todos os testes:

```bash
python -m pytest
```

Resultado esperado:

```text
collected 2 items

tests/test_git_utils.py .. [100%]

2 passed
```

---

# 🔄 Pipeline GitHub Actions

O projeto possui um workflow de CI configurado em:

```text
.github/workflows/ci.yml
```

O pipeline utiliza:

```yaml
GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
GIT_BEFORE: ${{ github.event.before }}
GIT_AFTER: ${{ github.sha }}
```

A `GEMINI_API_KEY` é armazenada como **GitHub Secret**, evitando que a chave seja exposta no código.

---

# 🔐 Segurança

A chave da API do Gemini não deve ser armazenada diretamente no código.

O projeto utiliza:

```text
GEMINI_API_KEY
```

como variável de ambiente.

No GitHub Actions:

```yaml
GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
```

Também é recomendado manter arquivos de ambiente e credenciais fora do Git através do `.gitignore`.

---

# 🧩 Exemplo do fluxo

Suponha que o arquivo:

```text
git/git_utils.py
```

seja alterado.

O sistema identifica:

```text
Arquivo alterado:
git/git_utils.py
```

Os testes disponíveis são:

```text
test_obter_arquivos_alterados_retorna_lista
test_extrair_arquivos_alterados
```

A IA analisa a relação entre eles e pode retornar:

```json
{
  "testes": [
    "test_obter_arquivos_alterados_retorna_lista",
    "test_extrair_arquivos_alterados"
  ]
}
```

O pytest então executa os testes selecionados.

Resultado:

```text
tests/test_git_utils.py .. [100%]

2 passed
```

---

# 📊 Arquitetura simplificada

```text
┌──────────────────────┐
│    Git Repository    │
└──────────┬───────────┘
           │
           │ arquivos alterados
           ▼
┌──────────────────────┐
│    git_utils.py      │
└──────────┬───────────┘
           │
           │ arquivos + testes
           ▼
┌──────────────────────┐
│   Gemini Client      │
│                      │
│   Google Gemini      │
└──────────┬───────────┘
           │
           │ testes selecionados
           ▼
┌──────────────────────┐
│       pytest         │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Resultado dos testes │
└──────────────────────┘
```

---

# 🎓 Objetivos de aprendizado

O projeto foi desenvolvido para praticar a integração entre diferentes conceitos:

- Python;
- programação modular;
- funções;
- listas e dicionários;
- JSON;
- subprocess;
- Git;
- pytest;
- APIs REST;
- integração com modelos de IA;
- variáveis de ambiente;
- GitHub Actions;
- Continuous Integration (CI).

---

# ✅ Status do projeto

### Implementado

- [x] Estrutura Python
- [x] Integração com Git
- [x] Identificação de arquivos alterados
- [x] Descoberta dos testes disponíveis
- [x] Integração com Google Gemini
- [x] Seleção de testes utilizando IA
- [x] Validação dos testes selecionados
- [x] Execução dos testes selecionados com pytest
- [x] Integração com GitHub Actions
- [x] Uso de GitHub Secret para a API Key
- [x] Tratamento do primeiro push do repositório
- [x] Testes automatizados

---

# 📌 Conclusão

O projeto demonstra uma aplicação prática de Inteligência Artificial integrada a um pipeline de Continuous Integration.

Em vez de executar automaticamente todos os testes do projeto, a aplicação utiliza o Gemini para analisar as alterações realizadas e selecionar os testes potencialmente relacionados às mudanças.

O objetivo principal não é substituir o pytest ou o CI, mas utilizar IA como uma camada de decisão dentro do processo de testes.

---

## 👨‍💻 Projeto

**AI CI Test Selector**

Projeto desenvolvido para estudos de **Python, IA, testes automatizados e CI/CD**.
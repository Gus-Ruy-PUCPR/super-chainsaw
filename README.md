Projeto ICS AVA PucPR

Este projeto automatiza a leitura de entregas do AVA da PUCPR (Canvas) e gera um arquivo .ics para importar no calendário. O fluxo é simples: acessamos a página, extraímos os nomes e datas, e criamos o arquivo de calendário.

📚 Breve Resumo de Python (Para nivelamento do grupo)

Como vimos até Estruturas de Dados na faculdade, vamos usar alguns conceitos de Orientação a Objetos de forma bem prática:

Funções (def): São blocos de código que executam uma tarefa específica e podem ser chamados várias vezes.

Classes: Funcionam como "moldes" ou "plantas". A biblioteca cria esses moldes para nós (ex: a classe Event é o molde para criar um evento genérico).

Métodos: São as funções que pertencem a um "molde" (Classe). Por exemplo, o método add() pertence à classe Calendário e serve para adicionar o evento que criamos lá dentro.

📅 Biblioteca iCalendar para Python

Usaremos a biblioteca ICS para python.

Documentação → ICS Documentation

Exemplo de uso:

# importar apenas as classes Calendar e Event da biblioteca.
from ics import Calendar, Event

# agora c e e sao variaveis que contem as Classes Calendar() e Event().
c = Calendar()
e = Event()

# método name e begin em Event, que setam as informações de nome e inicio.
e.name = "My cool event"
e.begin = '2014-01-01 00:00:00'

# metodo events e add em Calendar, que setam os eventos no calendario.
c.events.add(e)
c.events
# [<Event 'My cool event' begin:2014-01-01 00:00:00 end:2014-01-01 00:00:01>]

with open('my.ics', 'w') as my_file:
    my_file.writelines(c.serialize_iter())
# and it's done !


Para instalar:

$ pip install ics


🌐 Biblioteca Playwright (Automação de Navegador)

Usaremos o Playwright para simular o Google Chrome. Como a PUCPR exige login, ele vai digitar nosso usuário e senha automaticamente e carregar as tarefas.

Documentação → Playwright Documentation

Exemplo de uso:

# Importamos a função de sincronização do navegador
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Abre o navegador Chromium (headless=False mostra a tela abrindo)
    browser = p.chromium.launch(headless=False) 
    page = browser.new_page()

    # Acessa uma página da web
    page.goto("https://pucpr.instructure.com")

    # Extrai o código-fonte (HTML) inteiro da página depois de carregada
    html = page.content()

    browser.close()


Para instalar (instala a biblioteca e os navegadores de fundo):

$ pip install playwright
$ playwright install chromium


🔍 Biblioteca BeautifulSoup4 (Extração de Dados)

Usaremos o BS4 para ler o HTML gigante que o Playwright pegou e encontrar exatamente as "tags" onde estão escritos os nomes das atividades e as datas de entrega.

Documentação → BeautifulSoup Documentation

Exemplo de uso:

from bs4 import BeautifulSoup

# Exemplo de HTML fictício que pegaríamos da página
html_doc = "<html><body><h1>Trabalho de Python</h1><p>Data: 25/10</p></body></html>"

# Criamos a variável soup aplicando o molde BeautifulSoup para ler o HTML
soup = BeautifulSoup(html_doc, 'html.parser')

# Buscamos a tag <h1> e pegamos apenas o texto de dentro dela
titulo = soup.find('h1').text
print(titulo)
# Resultado esperado no terminal: Trabalho de Python


Para instalar:

$ pip install beautifulsoup4


🚀 Ambiente de Desenvolvimento Rápido (Deep Freeze)

Como os PCs dos laboratórios da faculdade têm Deep Freeze (zeram ao reiniciar), criamos um script para instalar tudo automaticamente.

1. Arquivo requirements.txt

Este arquivo diz ao Python quais bibliotecas nosso projeto precisa. Ele deve ficar na pasta raiz com este conteúdo:

ics
playwright
beautifulsoup4


2. Script setup.ps1

Crie um arquivo chamado setup.ps1 na mesma pasta do projeto. Ele cria o ambiente virtual (.venv) e instala as bibliotecas:

Write-Host "🚀 Iniciando configuração do ambiente..." -ForegroundColor Green

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

$venvPython = ".\.venv\Scripts\python.exe"

& $venvPython -m pip install --upgrade pip --quiet
& $venvPython -m pip install -r requirements.txt
& $venvPython -m playwright install chromium

Write-Host "✅ Ambiente pronto! Ative com: .\.venv\Scripts\Activate.ps1" -ForegroundColor Green


3. Como usar o .venv no dia a dia

Para Entrar (Ativar):

.\.venv\Scripts\Activate.ps1


(Se der erro vermelho de permissão, rode isso primeiro: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process e tente de novo).

Para Sair (Desativar):

deactivate


🐙 Resumo de Uso: Git e GitHub

Fluxo de trabalho diário no PC da faculdade:

1. Baixar o projeto pela primeira vez (Clonar):

$ git clone https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
$ cd NOME_DO_REPOSITORIO


2. Puxar atualizações do grupo (Fetch e Pull):

$ git fetch origin
$ git pull origin main


📝 Obs Importante: Configurando seu Usuário no Git
O que motiva essa necessidade? O Git precisa saber quem está enviando o código. Como o Deep Freeze zera o PC, ele apaga suas configurações. Antes de salvar algo (dar commit), configure:

$ git config --global user.name "Seu Nome e Sobrenome"
$ git config --global user.email "seu.email@exemplo.com"

# Trabalho de puxar os blogs do site e importar num arquivo csv
# Site do professor erlanio

import pandas as pd
import requests
from bs4 import BeautifulSoup
from PySimpleGUI import PySimpleGUI as sg


# List + id
blog_list = []
id = 0

# Response Site
response = requests.get("https://www.erlaniofreire.com.br/web/posts")
content = response.content
site = BeautifulSoup(content, 'html.parser')

# Html do site

blog = site.findAll('div', attrs={'class': 'journal-info'})

# Buscar todos topicos
for blogs in blog:
    # Id do topico
    id += 1

    # titulo
    titulo = blogs.find('h4')

    # subtitulo
    subtitulo = blogs.find('p', attrs={'class': 'separator'})

    # link
    link = blogs.find('a')

    blog_list.append([id, titulo.text, subtitulo.text, link['href']])

    # print(f"\nID: {id}{titulo.text}: \n{subtitulo.text} \n{link['href']}")


#PySimpleGUI
sg.theme('Reddit')
layoutscrapping = [
    [sg.Text('WebScrapping - Erlanio Freire')],
    [sg.Text('Desejar salvar com que nome?'), sg.Input(key='nome')],
    [sg.Button('Enviar')]
]


# Janela
janela = sg.Window('Tela de WebScraping', layoutscrapping)

while True:
    eventos, valores = janela.read()
    if eventos == sg.WINDOW_CLOSED:
        break
    if eventos == 'Enviar':
        if valores['nome'] == '':
            # Error
            layoutError = [
                [sg.Text('Preencher todos os campos')],
            ]
            janelaError = sg.Window('Algo ta errado', layoutError)
            eventos2, valores2 = janelaError.read()
        else:
            # Arquivo bruto
            blogexcel = pd.DataFrame(blog_list, columns=['Id', 'Título', 'Subtítulo', 'Link'])

            blogexcel.to_csv(f"{valores['nome']}.csv", index=False)
            blogexcel.to_excel(f"{valores['nome']}.xlsx", index=False)
            # Ao Salvar
            layoutSucesso = [
                [sg.Text('Sucesso ao salvar arquivo')],
                [sg.Button('Fechar')]
            ]
            janelaLogar = sg.Window('Sucesso', layoutSucesso)
            eventos2, valores2 = janelaLogar.read()

            if eventos2 == sg.WINDOW_CLOSED:
                break

            if eventos2 == 'Fechar':
                break
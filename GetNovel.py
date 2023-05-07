import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
from termcolor import colored
from time import sleep
from PyPDF2 import PdfMerger
from os import listdir, getcwd


def GetNovel(name, first_cap, last_cap, volume=-1):
    name = name.lower().split()
    name = '-'.join(name)
    if "'s" in name: name = name.replace("'s", 's')

    chapter_links = list()
    chapter_ids = list()

    for l in range(first_cap, last_cap + 1):
        if volume == -1:
            chapter_links.append(f'https://centralnovel.com/{name}-capitulo-{l}/')

        elif volume > -1:
            chapter_links.append(f'https://centralnovel.com/{name}-volume-{volume}-capitulo-{l}/')

        chapter_ids.append(f'{name} capítulo {l}')

    caps_info = {'links': chapter_links, 'info': chapter_ids}

    return caps_info


print(colored('\n\n                              Get', 'yellow'), end='')
print(colored('Novel\n\n\n', 'red'))




novel = GetNovel(
    name=str(input('Nome da Novel: ')),
    first_cap=int(input('Primeiro capítulo: ')),
    last_cap=int(input('Último capítulo: ')),
    volume=int(input('Volume [-1 SEM VOLUME]: ')))


path = str(input('Onde quer salvar os capítulos? Cole o caminho aqui: '))
this_path = getcwd()
key = True


for c in range(0, len(novel['links'])):
    try:
        response = requests.get(novel["links"][c]).text
    except:
        print(colored('Um erro ocorreu. Verifique se o nome e número dos capítulos da Novel estão corretos e tente novamente', 'red'))
        print('Programa fechando em 5 segundos...')
        sleep(6)
        key = False
        break

    html = BeautifulSoup(response, 'html.parser')
    chapter_html = html.find('div', class_='epcontent')
    chapter_title = html.find('h1', class_='entry-title').prettify()
    chapter_name = html.find('div', class_='cat-series').prettify()
    # Gets the element that I want from the page

    pdf = FPDF() # Creates an instance
    pdf.add_page()


    pdf.add_font('Lora', '', f'{this_path}/fonts/Lora-Regular.ttf')
    pdf.add_font('Lora', 'B', f'{this_path}/fonts/Lora-Bold.ttf')
    pdf.add_font('Lora', 'I', f'{this_path}/fonts/Lora-Italic.ttf')
    pdf.add_font('Lora', 'BI', f'{this_path}/fonts/Lora-Bold.ttf')
    pdf.set_font('Lora', size=12)

    try:
        pdf.ln(3)
        pdf.write_html(f"<center>{chapter_title}</center>")
        pdf.ln(1)
        pdf.write_html(f"<center>{chapter_name}</center>")
        pdf.ln(15)
        pdf.write_html(chapter_html.prettify())
        pdf.output(f'{path}/{novel["info"][c]}.pdf') # Outputs the PDF result
    except:
        print(colored('Um erro ocorreu ao baixar o PDF', 'red'))
        print('Programa fechando em 5 segundos...')
        sleep(5)
        key = False
        break

    print(colored(f'{novel["info"][c].capitalize().replace("-", " ")} baixado com sucesso!', 'green'))

if key is True:
    sn = str(input('Deseja mesclar os PDFs? [S/N]: ')).upper()[0]

    while sn not in 'SN' or sn == 'SN':
        print(colored('Digite "S" para sim e "N" para não', 'red'))
        sn = str(input('Deseja mesclar os PDFs? [S/N]: ')).upper()[0]


    if sn == 'S':
        merger = PdfMerger()
        for arquivo in listdir(path):
            if '.pdf' in arquivo:
                merger.append(f'{path}/{arquivo}')

        nome = str(input('Nome final do arquivo: '))
        merger.write(f'{path}/{nome}.pdf')


print(colored('Tarefa concluída. GetNovel fechará automaticamente em alguns segundos...', 'cyan'))
print(colored('Créditos: Davi𝓦oo#5327 (discord)'))
sleep(10)
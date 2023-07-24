import requests
from PyPDF2 import PdfReader

def download_pdf(url, file_name):

    headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    }

    response = requests.get(url = url, headers=headers, allow_redirects = True)
    if response.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(response.content)
    else:
        print(response.status_code)

# definir a URL do arquivo PDF
url = "https://rl.senado.gov.br/reports/rwservlet?legis&report=/forms/parlam/vono_r01.RDF&paramform=no&p_cod_materia_i=138100&p_cod_materia_f=138100&p_cod_sessao_votacao_i=6675&p_cod_sessao_votacao_f=6675&p_order_by=nom_parlamentar"
file_name = "out/page.pdf"
download_pdf(url, file_name)

def extrair_texto_pdf(file_name):
    texto = ""
    with open(file_name, "rb") as arquivo:
        pdf_reader = PdfReader(arquivo)
        num_paginas = len(pdf_reader.pages)
        for pagina_num in range(num_paginas):
            pagina = pdf_reader.pages[pagina_num]
            texto += pagina.extract_text()
    return texto

texto_extraido = extrair_texto_pdf(file_name)

with open("out/texto_pdf.txt", "w") as arquivo:
    # Escrever o texto no arquivo
    arquivo.write(texto_extraido)

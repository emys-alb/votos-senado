import requests
from PyPDF2 import PdfReader

from pathlib import Path

def download_pdf(url, file_name):
    headers = {
        "User-Agent": "Chrome/51.0.2704.103",
    }
    response = requests.get(url, headers=headers)
    filename = Path(file_name)
    
    # Save the PDF
    if response.status_code == 200:
        filename.write_bytes(response.content)
    else:
        print(response.status_code)

# definir a URL do arquivo PDF
url = "https://rl.senado.gov.br/reports/rwservlet?legis&report=/forms/parlam/vono_r01.RDF&paramform=no&p_cod_materia_i=138100&p_cod_materia_f=138100&p_cod_sessao_votacao_i=6675&p_cod_sessao_votacao_f=6675&p_order_by=nom_parlamentar"
download_pdf(url, "page.pdf")

# abrir o arquivo PDF a partir do conteúdo da resposta HTTP
pdf_file = PdfReader("page.pdf")
infos = pdf_file.documentInfo
# percorrer todas as páginas do PDF
for page in pdf_file.pages:
    # extrair o conteúdo de uma página específica
    content = page.extract_text
    # fazer algo com o conteúdo extraído
    print(content)
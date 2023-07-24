import scrapy
import requests
import PyPDF2

class PDFSpider(scrapy.Spider):
    name = "pdf_spider"
    periodo = ["11/04/2022", "11/04/2023"]
    url = f"https://www25.senado.leg.br/web/atividade/votacoes-nominais/-/v/periodo/{periodo[0]}/a/{periodo[1]}"
    start_urls = [url]

    # Div dos resultados da pesquisa
    resultados = ".accordion"

    def parse(self, response):
        # encontrar links para arquivos PDF
        pdf_links = response.css("a[href$='.pdf']::attr(href)").getall()
        
        for pdf_link in pdf_links:
            # baixar o arquivo PDF
            pdf_response = requests.get(pdf_link)
            # criar um objeto leitor do PyPDF2
            reader = PyPDF2.PdfFileReader(pdf_response.content)
            # percorrer todas as páginas do PDF
            for page_num in range(reader.numPages):
                # extrair o conteúdo de uma página específica
                page = reader.getPage(page_num)
                content = page.extractText()
                # fazer algo com o conteúdo extraído
                print(content)

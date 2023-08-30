import scrapy
from scrapy.crawler import CrawlerProcess

url = ["https://www25.senado.leg.br/web/atividade/materias/-/materia/158035/votacoes"]

class VotacaoSpider(scrapy.Spider):
    name = "votacao"
    start_urls = url
    custom_settings = {
        'FEEDS': {
            'votacao_6718.csv': {
                'format': 'csv'
            }
        }
    }

    def parse(self, response):
        #informações gerais da votação
        data_votacao = response.css("#conteudoSessaoPlenaria25602 > div:nth-child(1) > p:nth-child(1) > span:nth-child(2)::text")
        status_votacao = response.css(".label::text")
        conteudo_votacao = response.css("dl.dl-horizontal:nth-child(4) > dd:nth-child(4)::text")

        for colunas in response.css("div.row-fluid:nth-child(4)"):
            for votacao in colunas.css(".span4 > table > tbody:nth-child(2) > tr"):
                obs = votacao.css("td:nth-child(4)::text").extract_first()
                yield {
                    "data_votacao": data_votacao.extract_first(),
                    "status_votacao": status_votacao.extract_first(),
                    "conteudo_votacao": conteudo_votacao.extract_first(),
                    
                    "parlamentar" : votacao.css("td:nth-child(2)::text").extract_first(),
                    "voto" : votacao.css("td:nth-child(3)::text").extract_first(),
                    "obs" : "" if obs is None else obs
                }

process = CrawlerProcess()
process.crawl(VotacaoSpider)
process.start()
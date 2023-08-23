import scrapy

url = "https://www25.senado.leg.br/web/atividade/materias/-/materia/158035/votacoes"

class VotacaoScrapper(scrapy.Spider):
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
        conteudo_votacao = response.css(".content > .portlet-body > .dl-horizontal > dd:nth-child(2)::text").extract_first()
        print(conteudo_votacao)
        
        for votacao in response.css("#conteudoVotacao6718 > .row-fluid:nth-child(2)"):
            for linha in votacao.css("table > tbody > tr"):
                yield {
                    "parlamentar" : linha.css("td:nth-child(2)::text").extract_first(),
                    "voto" : linha.css("td:nth-child(3)::text").extract_first(),
                    "obs" : linha.css("td:nth-child(4)::text").extract_first()
                }

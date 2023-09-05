import scrapy
from scrapy.crawler import CrawlerProcess

def parse_url(start_date, end_date):
    url = [f"https://www25.senado.leg.br/web/atividade/votacoes-nominais/-/v/periodo/01/01/{start_date}/a/31/12/{end_date}"]
    return url

class PaginaSpider(scrapy.Spider):
    name = "paginação"
    start_urls = parse_url(2019, 2023)
    custom_settings = {
        'FEEDS': {
            'out/votos.csv': {
                'format': 'csv',
                'encoding': 'utf8'
            }
        }
    }

    def parse(self, response):
        for table in response.css(".painel-corpo > div:nth-child(1) > table.table"):
            for sessao in table.css("tbody:nth-child(3) > tr"):
                items = VotacaoItem()

                items["materia"] = sessao.css("td:nth-child(1)::text").get()
                items["link"] = sessao.css("td:nth-child(2) > a::attr(href)").get()
                items["descricao"] = sessao.css("td:nth-child(2) > a::text").get()

                yield response.follow(url=items["link"], callback=self.votacao, meta={'items':items})
    
    def votacao(self, response):
        items = response.meta['items']

        # Informações gerais da votação
        data_votacao = response.css("#conteudoSessaoPlenaria25602 > div:nth-child(1) > p:nth-child(1) > span:nth-child(2)::text")
        status_votacao = response.css(".label::text")
        conteudo_votacao = response.css("dl.dl-horizontal:nth-child(4) > dd:nth-child(4)::text")

        #Informações especificas da votação
        for colunas in response.css("div.row-fluid:nth-child(4)"):
            for votacao in colunas.css(".span4 > table > tbody:nth-child(2) > tr"):
                items["data_votacao"]: data_votacao.get()
                items["status_votacao"]: status_votacao.get()
                items["conteudo_votacao"]: conteudo_votacao.get()
                items["parlamentar"] : votacao.css("td:nth-child(2)::text").get()
                items["voto"] : votacao.css("td:nth-child(3)::text").get()
                items["obs"] : votacao.css("td:nth-child(4)::text").get()

class VotacaoItem(scrapy.Item):
    materia = scrapy.Field()
    link = scrapy.Field()
    descricao = scrapy.Field()

    data_votacao = scrapy.Field()
    status_votacao = scrapy.Field()
    conteudo_votacao = scrapy.Field()

    parlamentar = scrapy.Field()
    voto = scrapy.Field()
    obs = scrapy.Field()

process = CrawlerProcess()
process.crawl(PaginaSpider)
process.start()
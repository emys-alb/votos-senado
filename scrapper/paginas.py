import scrapy
from scrapy.crawler import CrawlerProcess
from core.items import VotacaoItem
from core.settings import FILENAME_SETTING, INIT_DATE_SETTING, FINISH_DATE_SETTING

def parse_url(start_date, end_date):
    url = [f"https://www25.senado.leg.br/web/atividade/votacoes-nominais/-/v/periodo/{start_date}/a/{end_date}"]
    return url

filename = FILENAME_SETTING
class PaginaSpider(scrapy.Spider):
    name = "paginas"
    start_urls = parse_url(INIT_DATE_SETTING, FINISH_DATE_SETTING)
    custom_settings = {
        "FEEDS": {
            f"../out/{filename}": {
                "format": "csv",
                "encoding": "utf8",
                "item_export_kwargs": 
                {
                    "include_headers_line": False
                }
            }
        }
    }

    def parse(self, response):
        for table in response.css(".painel-corpo > div:nth-child(1) > table.table"):
            for sessao in table.css("tbody:nth-child(3) > tr"):
                items = VotacaoItem()

                materia = sessao.css("td:nth-child(1)::text").get()
                items["materia"] = materia.replace(u'\xa0', u' ')
                items["link"] = sessao.css("td:nth-child(2) > a::attr(href)").get()
                items["descricao"] = sessao.css("td:nth-child(2) > a::text").get()

                yield response.follow(url=items["link"], callback=self.votacao, meta={'items':items})
    
    def votacao(self, response):
        items = response.meta['items']

        if "congressonacional" in response.url:
            # Informações gerais da votação
            data_votacao = response.xpath("/html/body/div/section/div[1]/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/div[1]/dl/dd[1]/span/text()")
        else:
            # Informações gerais da votação
            data_votacao = response.xpath("/html/body/div/div[6]/div/div/div/div/div/div/div/div/div/div[2]/div/p[1]/span/text()")
        
        status_votacao = response.css(".label::text")

        #Informações especificas da votação
        for colunas in response.css("div.row-fluid:nth-child(4)"):
            for votacao in colunas.css(".span4 > table > tbody:nth-child(2) > tr"):
                items["data_votacao"] = data_votacao.get()
                items["status_votacao"] = status_votacao.get()
                items["parlamentar"] = votacao.css("td:nth-child(2)::text").get()
                items["voto"] = votacao.css("td:nth-child(3)::text").get()
                items["obs"] = votacao.css("td:nth-child(4)::text").get()

                yield items

process = CrawlerProcess()
process.crawl(PaginaSpider)
process.start()
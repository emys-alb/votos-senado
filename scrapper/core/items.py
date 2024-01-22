import scrapy

class VotacaoItem(scrapy.Item):
    materia = scrapy.Field()
    link = scrapy.Field()
    descricao = scrapy.Field()

    data_votacao = scrapy.Field()
    status_votacao = scrapy.Field()

    parlamentar = scrapy.Field()
    voto = scrapy.Field()
    obs = scrapy.Field()

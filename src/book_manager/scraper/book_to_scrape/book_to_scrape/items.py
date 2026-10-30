# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


import scrapy


class BookToScrapeItem(scrapy.Item):
    # define the fields for your item here like:
    # name: str | None = None
    titulo_buscado = scrapy.Field()
    titulo_libro = scrapy.Field()
    precio = scrapy.Field()
    forma_de_pago = scrapy.Field()
    descripcion = scrapy.Field()
    url_imagen = scrapy.Field()
    url = scrapy.Field()
    autor_buscado = scrapy.Field()
    titulo_producto = scrapy.Field()
    autor_libro = scrapy.Field()

import re
import unicodedata
import scrapy
from urllib.parse import quote_plus

from ..loaders import CuspideLoader


URL_BASE = "https://cuspide.com/"

def normalizar_texto(texto: str) ->list[str]:
    """Normaliza el texto eliminando acentos y caracteres especiales."""
    texto = texto.replace("¥", "ñ").casefold()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(
        caracter
        for caracter in texto
        if not unicodedata.combining(caracter)
    )
    return re.findall(r"[a-z0-9]+", texto)

def comparar_titulo(titulo_catalogo: str, titulo_producto: str) -> bool:
    """Compara dos títulos de libros normalizados y devuelve True si son iguales."""

    esperado = normalizar_texto(titulo_catalogo)
    encontrado = normalizar_texto(titulo_producto)

    if not esperado:
        return False

    largo = len(esperado)
    return any(
        encontrado[i:i + largo] == esperado
        for i in range(len(encontrado) - largo + 1)
    ) 

def comparar_autor(autor_catalogo: str, autor_libro: str) -> bool:
    """Compara dos nombres de autores normalizados y devuelve True si son iguales."""

    esperado = set(normalizar_texto(autor_catalogo))
    encontrado = set(normalizar_texto(autor_libro))

    return bool(esperado) and esperado.issubset(encontrado)

  


class CuspideSpider(scrapy.Spider):
    name = "cuspide_spider"
    allowed_domains = ["cuspide.com"]
    MAX_RESULTADOS = 10


    def __init__(self,libros=None, titulo=None, autor=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if libros is None and titulo and autor:
            libros = [{"titulo": titulo, "autor": autor}]

        self.libros = libros or []


    async def start(self):
        if not self.libros:
            self.logger.error("No se proporcionaron títulos de libros para buscar.")
            return

        for libro in self.libros:
            titulo = libro["titulo"]
            autor = libro["autor"]
            consulta = f"{titulo} {autor}"
            url = f"{URL_BASE}?s={quote_plus(consulta)}&post_type=product"

            yield scrapy.Request(
                url,
                callback=self.parse,
                meta={
                    "titulo_buscado": titulo, 
                    "autor_buscado": autor
                    },
            )

    def parse(self, response):
        """Toma solo los primeros 10 resultados de la busqueda y extrae los datos de cada libro."""

        
        vistos = set()
        cantidad = 0

        for card in response.css("div.product-small"):

            href = card.css(
                "a.woocommerce-LoopProduct-link::attr(href)"
            ).get()

            if not href or href in vistos:
                continue

            vistos.add(href)
            cantidad += 1

            yield response.follow(
                href,
                callback=self.parse_producto,
                dont_filter=True,
                meta={
                    "titulo_buscado": response.meta["titulo_buscado"],
                    "autor_buscado": response.meta["autor_buscado"],
                    "precio_listado": card.css(
                        "span.woocommerce-Price-amount bdi::text"
                    ).get()
                    },
            )

            if cantidad >= self.MAX_RESULTADOS:
                break


    def parse_producto(self, response):
        """Conservamos los candidatos cuyo titulo y autor coinciden."""

        titulo_producto = (
            response.css("h1.product-title::text").get()
            or response.css("h1::text").get()
            or ""
        ).strip()

        autor_libro = (
            response.css("p.livriz-authors::text").get() or ""
        ).strip()

        titulo_buscado = response.meta["titulo_buscado"]
        autor_buscado = response.meta["autor_buscado"]

        if not comparar_titulo(titulo_buscado, titulo_producto):
            self.logger.debug(
                "Descartado por título: %s (se buscaba %s)",
                titulo_producto,
                titulo_buscado,
            )
            return

        if not comparar_autor(autor_buscado, autor_libro):
            self.logger.debug(
                "Descartado por autor: producto=%s, encontrado=%s, buscado=%s",
                titulo_producto,
                autor_libro,
                autor_buscado,
            )
            return

        loader = CuspideLoader(response=response)
        loader.add_value("titulo_buscado", response.meta["titulo_buscado"])
        loader.add_value("autor_buscado", response.meta["autor_buscado"])
        loader.add_value("autor_libro", autor_libro)
        loader.add_value("titulo_producto", titulo_producto)
        loader.add_value("url", response.url)
        loader.add_css("titulo_libro", "h1.product-title::text")
        loader.add_css("titulo_libro", "h1::text")

        loader.add_css("precio", "p.price bdi::text")
        loader.add_css("precio", "span.woocommerce-Price-amount bdi::text")

        loader.add_value("precio", response.meta.get("precio_listado"))

        loader.add_css("url_imagen", "img.wp-post-image::attr(data-large-file)")
        loader.add_css("url_imagen", "img.wp-post-image::attr(data-src)")
        loader.add_css("url_imagen", "img.wp-post-image::attr(src)")

        loader.add_xpath(
            "forma_de_pago",
            "//li[contains(., 'Depósito o transferencia')"
            " or contains(., 'Tarjetas de créditos')"
            " or contains(., 'MercadoPago')"
            " or contains(., 'Mobbex')"
            " or contains(., 'RapiPago')]//text()",
        )

        loader.add_xpath(
            "descripcion",
            "//h5[normalize-space()='Descripción']"
            "/parent::div/following-sibling::div[contains(@class, 'large-10')]"
            "//div[contains(@class, 'panel')]//text()",
        )

        yield loader.load_item()

            
        

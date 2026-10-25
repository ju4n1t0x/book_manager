import re

from itemloaders.processors import Join, MapCompose, TakeFirst
from scrapy.loader import ItemLoader

from .items import BookToScrapeItem

def limpiar_texto(texto: str | None) -> str | None:
    """Limpia el texto eliminando espacios en blanco y saltos de línea."""
    if texto is None:
        return None
    
    texto_limpio: str = texto.strip()

    return texto_limpio or None

def parse_precio(valor: str | None) -> float | None:
    """Extrae el precio de un libro eliminando el símbolo de moneda y espacios en blanco.
    Convierte '$ 15.999,00 -> 15999.00
    """

    if not valor:
        return None

    texto = re.sub(r"[^\d.,]", "", valor)

    if not texto:
        return None

    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")
    else:
        texto = texto.replace(".", "")
    try:
        return float(texto)
    except ValueError:
        return None


class CuspideLoader(ItemLoader):
    """Loader para procersar los items de libros de la tienda Cuspide."""

    default_item_class = BookToScrapeItem

    default_input_processor = MapCompose(limpiar_texto)

    default_output_processor = TakeFirst()

    precio_in = MapCompose(parse_precio)

    forma_de_pago_out = Join("; ")

    descripcion_out = Join(" ")
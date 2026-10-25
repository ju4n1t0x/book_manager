# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv

from pathlib import Path
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class PipelineValidacion:

    CAMPOS_OBLIGATORIOS = (
        "titulo_buscado",
        "titulo_libro",
        "precio",
        "url",
        "autor_buscado",
        "titulo_producto"
    )

    def process_item(self, item):
        """Valida que los campos obligatorios estén presentes en el item."""
        adapter = ItemAdapter(item)

        for campo in self.CAMPOS_OBLIGATORIOS:
            if not adapter.get(campo):
                raise DropItem(
                    f"Faltan campos obligatorios: {campo}"
                    )
        return item

class PipelineCsv:
    """Guarda cada item valido como una fila de un CSV."""

    CAMPOS = (
        "titulo_buscado",
        "titulo_libro",
        "precio",
        "forma_de_pago",
        "descripcion",
        "url_imagen",
        "url",
        "autor_buscado",
        "titulo_producto",
        "autor_libro"
    )

    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            ruta_archivo=crawler.settings.get(
                "RUTA_ARCHIVO",
                "cuspide_resultados.csv"
            )
        )
    
    def open_spider(self):
        ruta = Path(self.ruta_archivo)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        self.archivo = open(self.ruta_archivo, "w", newline="", encoding="utf-8")
        self.writer = csv.DictWriter(self.archivo, fieldnames=self.CAMPOS)
        self.writer.writeheader()

    def close_spider(self):
        self.archivo.close()

    def process_item(self, item):
        self.writer.writerow(ItemAdapter(item).asdict())
        return item
    
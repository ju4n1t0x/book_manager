"""Tablas de la base de datos del sistema."""

import datetime
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import (
    CheckConstraint,
    Date,
    Engine,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Clase base de las tablas."""


class GeneroModelo(Base):
    """Tabla generos: categorías literarias de los libros."""

    __tablename__ = "generos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    descripcion: Mapped[str] = mapped_column(String(255), default="")

    libros: Mapped[List["LibroModelo"]] = relationship(back_populates="genero")


class EditorialModelo(Base):
    """Tabla editoriales: proveedores de los libros."""

    __tablename__ = "editoriales"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    pais: Mapped[str] = mapped_column(String(100))
    sitio_web: Mapped[str] = mapped_column(String(255), default="")

    libros: Mapped[List["LibroModelo"]] = relationship(
        back_populates="editorial"
    )


class MonedaModelo(Base):
    """Tabla monedas: monedas en las que se expresan los precios."""

    __tablename__ = "monedas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo: Mapped[str] = mapped_column(String(3), unique=True)
    nombre: Mapped[str] = mapped_column(String(100))
    simbolo: Mapped[str] = mapped_column(String(10))

    precios: Mapped[List["PrecioModelo"]] = relationship(
        back_populates="moneda"
    )


class TipoCotizacionModelo(Base):
    """Tabla tipos_cotizacion: tipos de dólar (Oficial, Blue, MEP, etc.)."""

    __tablename__ = "tipos_cotizacion"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo: Mapped[str] = mapped_column(String(30), unique=True)
    nombre: Mapped[str] = mapped_column(String(100))

    cotizaciones: Mapped[List["CotizacionDolarModelo"]] = relationship(
        back_populates="tipo"
    )


class LibroModelo(Base):
    """Tabla libros: títulos del catálogo."""

    __tablename__ = "libros"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    isbn: Mapped[str] = mapped_column(String(13), unique=True)
    titulo: Mapped[str] = mapped_column(String(255))
    autor: Mapped[str] = mapped_column(String(150))
    editorial_id: Mapped[int] = mapped_column(ForeignKey("editoriales.id"))
    genero_id: Mapped[int] = mapped_column(ForeignKey("generos.id"))
    anio_publicacion: Mapped[int] = mapped_column(Integer)

    editorial: Mapped["EditorialModelo"] = relationship(
        back_populates="libros"
    )
    genero: Mapped["GeneroModelo"] = relationship(back_populates="libros")
    precios: Mapped[List["PrecioModelo"]] = relationship(
        back_populates="libro", cascade="all, delete-orphan"
    )
    stock: Mapped[Optional["StockModelo"]] = relationship(
        back_populates="libro", cascade="all, delete-orphan"
    )


class PrecioModelo(Base):
    """Tabla precios: precio de un libro en una moneda."""

    __tablename__ = "precios"
    __table_args__ = (
        UniqueConstraint("libro_id", "moneda_id"),
        CheckConstraint("monto > 0"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    libro_id: Mapped[int] = mapped_column(
        ForeignKey("libros.id", ondelete="CASCADE")
    )
    moneda_id: Mapped[int] = mapped_column(ForeignKey("monedas.id"))
    monto: Mapped[Decimal] = mapped_column(Numeric(12, 2))

    libro: Mapped["LibroModelo"] = relationship(back_populates="precios")
    moneda: Mapped["MonedaModelo"] = relationship(back_populates="precios")


class StockModelo(Base):
    """Tabla stock: cantidad disponible de cada libro."""

    __tablename__ = "stock"
    __table_args__ = (
        CheckConstraint("cantidad >= 0"),
        CheckConstraint("cantidad_minima >= 0"),
    )

    libro_id: Mapped[int] = mapped_column(
        ForeignKey("libros.id", ondelete="CASCADE"), primary_key=True
    )
    cantidad: Mapped[int] = mapped_column(Integer)
    cantidad_minima: Mapped[int] = mapped_column(Integer, default=5)

    libro: Mapped["LibroModelo"] = relationship(back_populates="stock")


class CotizacionDolarModelo(Base):
    """Tabla cotizaciones: valor del dólar por tipo y fecha."""

    __tablename__ = "cotizaciones"
    __table_args__ = (
        CheckConstraint("compra > 0"),
        CheckConstraint("venta > 0"),
    )

    tipo_id: Mapped[int] = mapped_column(
        ForeignKey("tipos_cotizacion.id"), primary_key=True
    )
    fecha: Mapped[datetime.date] = mapped_column(Date, primary_key=True)
    compra: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    venta: Mapped[Decimal] = mapped_column(Numeric(12, 2))

    tipo: Mapped["TipoCotizacionModelo"] = relationship(
        back_populates="cotizaciones"
    )


def crear_tablas(engine: Engine) -> None:
    """Crea las tablas en la base de datos.

    Args:
        engine (Engine): Motor de la base de datos.
    """
    Base.metadata.create_all(engine)

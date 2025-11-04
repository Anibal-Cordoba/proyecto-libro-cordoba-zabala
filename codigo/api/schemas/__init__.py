"""
Schemas Pydantic para validación de datos
"""
from .capitulo import CapituloCreate, CapituloResponse, CapituloUpdate
from .contenido import ContenidoCreate, ContenidoResponse

__all__ = [
    'CapituloCreate',
    'CapituloResponse',
    'CapituloUpdate',
    'ContenidoCreate',
    'ContenidoResponse',
]

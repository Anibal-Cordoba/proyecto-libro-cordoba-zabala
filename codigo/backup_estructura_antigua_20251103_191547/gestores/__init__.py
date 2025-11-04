"""
Paquete de Gestores
===================
Contiene la lógica de negocio del sistema.
"""

from .gestor_contenido import GestorContenido
from .gestor_capitulo import GestorCapitulo

__all__ = [
    'GestorContenido',
    'GestorCapitulo'
]

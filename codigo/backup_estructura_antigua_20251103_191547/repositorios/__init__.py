"""
Paquete de Repositorios
========================
Contiene las clases de acceso a datos (patrón Repository).
"""

from .repositorio_contenido import RepositorioContenido
from .repositorio_capitulo import RepositorioCapitulo
from .repositorio_union_capitulo_contenido import RepositorioUnionCapituloContenido

__all__ = [
    'RepositorioContenido',
    'RepositorioCapitulo',
    'RepositorioUnionCapituloContenido'
]

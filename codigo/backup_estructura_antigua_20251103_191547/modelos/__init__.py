"""
Paquete de Modelos
==================
Contiene las entidades de datos del sistema de libros interactivos.
"""

from .contenido import Contenido
from .texto import Texto
from .imagen import Imagen
from .video import Video
from .objeto3d import Objeto3D
from .capitulo import Capitulo
from .union_capitulo_contenido import UnionCapituloContenido

__all__ = [
    'Contenido',
    'Texto',
    'Imagen',
    'Video',
    'Objeto3D',
    'Capitulo',
    'UnionCapituloContenido'
]

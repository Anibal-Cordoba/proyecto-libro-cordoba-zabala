"""
Clase Imagen
============
Representa un bloque de contenido de tipo imagen.
"""

from typing import Optional
from .contenido import Contenido


class Imagen(Contenido):
    """
    Clase que representa un contenido de tipo imagen.
    
    Attributes:
        url_archivo (str): URL o ruta del archivo de imagen
        formato (str): Formato de la imagen (jpg, png, svg, etc.)
    """
    
    def __init__(self, url_archivo: str, formato: str, tema: str, id_contenido: Optional[str] = None):
        """
        Inicializa un bloque de imagen.
        
        Args:
            url_archivo: URL o ruta del archivo de imagen
            formato: Formato de la imagen
            tema: Tema del contenido
            id_contenido: ID único (se genera automáticamente si no se proporciona)
        """
        super().__init__(tema=tema, id_contenido=id_contenido)
        self.url_archivo = url_archivo
        self.formato = formato
    
    def __str__(self) -> str:
        """Representación en cadena de la imagen."""
        return f"Imagen(id={self.id_contenido}, tema='{self.tema}', url='{self.url_archivo}', formato='{self.formato}')"

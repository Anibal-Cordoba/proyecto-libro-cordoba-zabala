"""
Clase Video
===========
Representa un bloque de contenido de tipo video.
"""

from typing import Optional
from .contenido import Contenido


class Video(Contenido):
    """
    Clase que representa un contenido de tipo video.
    
    Attributes:
        url_archivo (str): URL o ruta del archivo de video
        duracion (float): Duración del video en segundos
    """
    
    def __init__(self, url_archivo: str, duracion: float, tema: str, id_contenido: Optional[str] = None):
        """
        Inicializa un bloque de video.
        
        Args:
            url_archivo: URL o ruta del archivo de video
            duracion: Duración del video en segundos
            tema: Tema del contenido
            id_contenido: ID único (se genera automáticamente si no se proporciona)
        """
        super().__init__(tema=tema, id_contenido=id_contenido)
        self.url_archivo = url_archivo
        self.duracion = duracion
    
    def __str__(self) -> str:
        """Representación en cadena del video."""
        return f"Video(id={self.id_contenido}, tema='{self.tema}', url='{self.url_archivo}', duracion={self.duracion}s)"

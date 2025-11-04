"""
Clase Objeto3D
==============
Representa un bloque de contenido de tipo objeto 3D.
"""

from typing import Optional
from .contenido import Contenido


class Objeto3D(Contenido):
    """
    Clase que representa un contenido de tipo objeto 3D.
    
    Attributes:
        url_archivo (str): URL o ruta del archivo del objeto 3D
        formato (str): Formato del objeto 3D (obj, fbx, gltf, etc.)
    """
    
    def __init__(self, url_archivo: str, formato: str, tema: str, id_contenido: Optional[str] = None):
        """
        Inicializa un bloque de objeto 3D.
        
        Args:
            url_archivo: URL o ruta del archivo del objeto 3D
            formato: Formato del objeto 3D
            tema: Tema del contenido
            id_contenido: ID único (se genera automáticamente si no se proporciona)
        """
        super().__init__(tema=tema, id_contenido=id_contenido)
        self.url_archivo = url_archivo
        self.formato = formato
    
    def __str__(self) -> str:
        """Representación en cadena del objeto 3D."""
        return f"Objeto3D(id={self.id_contenido}, tema='{self.tema}', url='{self.url_archivo}', formato='{self.formato}')"

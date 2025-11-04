"""
Clase abstracta Contenido
==========================
Representa un bloque de contenido genérico en el sistema.
"""

from abc import ABC, abstractmethod
from typing import Optional
import uuid


class Contenido(ABC):
    """
    Clase abstracta que representa un contenido del libro.
    
    Attributes:
        id_contenido (str): Identificador único del contenido
        tema (str): Tema asociado al contenido
    """
    
    def __init__(self, tema: str, id_contenido: Optional[str] = None):
        """
        Inicializa un contenido.
        
        Args:
            tema: Tema del contenido
            id_contenido: ID único (se genera automáticamente si no se proporciona)
        """
        self.id_contenido = id_contenido or str(uuid.uuid4())
        self.tema = tema
    
    def __str__(self) -> str:
        """Representación en cadena del contenido."""
        return f"{self.__class__.__name__}(id={self.id_contenido}, tema='{self.tema}')"
    
    def __repr__(self) -> str:
        """Representación detallada del contenido."""
        return self.__str__()

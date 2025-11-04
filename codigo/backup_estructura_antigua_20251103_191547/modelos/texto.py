"""
Clase Texto
===========
Representa un bloque de contenido de tipo texto.
"""

from typing import Optional
from .contenido import Contenido


class Texto(Contenido):
    """
    Clase que representa un contenido de tipo texto.
    
    Attributes:
        cuerpo_texto (str): El contenido textual
    """
    
    def __init__(self, cuerpo_texto: str, tema: str, id_contenido: Optional[str] = None):
        """
        Inicializa un bloque de texto.
        
        Args:
            cuerpo_texto: El contenido del texto
            tema: Tema del contenido
            id_contenido: ID único (se genera automáticamente si no se proporciona)
        """
        super().__init__(tema=tema, id_contenido=id_contenido)
        self.cuerpo_texto = cuerpo_texto
    
    def __str__(self) -> str:
        """Representación en cadena del texto."""
        preview = self.cuerpo_texto[:50] + "..." if len(self.cuerpo_texto) > 50 else self.cuerpo_texto
        return f"Texto(id={self.id_contenido}, tema='{self.tema}', texto='{preview}')"

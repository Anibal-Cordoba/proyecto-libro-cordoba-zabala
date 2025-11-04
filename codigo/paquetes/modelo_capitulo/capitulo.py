"""
Clase Capitulo
==============
Representa un capítulo del libro.
"""

from typing import Optional
import uuid


class Capitulo:
    """
    Clase que representa un capítulo del libro.
    
    Attributes:
        id_capitulo (str): Identificador único del capítulo
        titulo (str): Título del capítulo
        numero (int): Número del capítulo en el libro
        introduccion (str): Texto de introducción del capítulo
        tema (str): Tema principal del capítulo
    """
    
    def __init__(
        self,
        titulo: str,
        numero: int,
        introduccion: str,
        tema: str,
        id_capitulo: Optional[str] = None
    ):
        """
        Inicializa un capítulo.
        
        Args:
            titulo: Título del capítulo
            numero: Número del capítulo
            introduccion: Texto de introducción
            tema: Tema del capítulo
            id_capitulo: ID único (se genera automáticamente si no se proporciona)
        """
        self.id_capitulo = id_capitulo or str(uuid.uuid4())
        self.titulo = titulo
        self.numero = numero
        self.introduccion = introduccion
        self.tema = tema
    
    def __str__(self) -> str:
        """Representación en cadena del capítulo."""
        return f"Capitulo(id={self.id_capitulo}, num={self.numero}, titulo='{self.titulo}', tema='{self.tema}')"
    
    def __repr__(self) -> str:
        """Representación detallada del capítulo."""
        return self.__str__()

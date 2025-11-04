"""
Clase UnionCapituloContenido
=============================
Representa la relación muchos a muchos entre capítulos y contenidos.
"""

from typing import Optional


class UnionCapituloContenido:
    """
    Clase que representa la unión entre un capítulo y un contenido.
    Implementa la relación muchos a muchos con información de orden.
    
    Attributes:
        id_capitulo (str): ID del capítulo
        id_contenido (str): ID del contenido
        orden (int): Orden del contenido dentro del capítulo
    """
    
    def __init__(self, id_capitulo: str, id_contenido: str, orden: int):
        """
        Inicializa una unión capítulo-contenido.
        
        Args:
            id_capitulo: Identificador del capítulo
            id_contenido: Identificador del contenido
            orden: Orden del contenido en el capítulo (empezando en 1)
        """
        self.id_capitulo = id_capitulo
        self.id_contenido = id_contenido
        self.orden = orden
    
    def __str__(self) -> str:
        """Representación en cadena de la unión."""
        return f"UnionCapituloContenido(capitulo={self.id_capitulo}, contenido={self.id_contenido}, orden={self.orden})"
    
    def __repr__(self) -> str:
        """Representación detallada de la unión."""
        return self.__str__()

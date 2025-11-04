"""
Gestor de Capítulo
===================
Implementa la lógica de negocio para la gestión de capítulos.
"""

from typing import List, Tuple, Dict, Any
import sys
sys.path.append('..')
from modelos import Capitulo, Contenido
from repositorios import RepositorioCapitulo, RepositorioContenido, RepositorioUnionCapituloContenido


class GestorCapitulo:
    """
    Gestor de la lógica de negocio para capítulos.
    
    Attributes:
        repositorio_capitulo: Repositorio de capítulos
        repositorio_contenido: Repositorio de contenidos
        repositorio_union: Repositorio de uniones capítulo-contenido
    """
    
    def __init__(
        self,
        repositorio_capitulo: RepositorioCapitulo,
        repositorio_contenido: RepositorioContenido,
        repositorio_union: RepositorioUnionCapituloContenido
    ):
        """
        Inicializa el gestor de capítulos.
        
        Args:
            repositorio_capitulo: Repositorio de capítulos
            repositorio_contenido: Repositorio de contenidos
            repositorio_union: Repositorio de uniones
        """
        self.repositorio_capitulo = repositorio_capitulo
        self.repositorio_contenido = repositorio_contenido
        self.repositorio_union = repositorio_union
    
    def crear_capitulo(self, titulo: str, numero: int, introduccion: str, tema: str) -> Capitulo:
        """
        Crea un nuevo capítulo.
        
        Args:
            titulo: Título del capítulo
            numero: Número del capítulo
            introduccion: Texto de introducción
            tema: Tema del capítulo
            
        Returns:
            El capítulo creado y guardado
        """
        capitulo = Capitulo(
            titulo=titulo,
            numero=numero,
            introduccion=introduccion,
            tema=tema
        )
        return self.repositorio_capitulo.guardar(capitulo)
    
    def eliminar_capitulo(self, id_capitulo: str) -> None:
        """
        Elimina un capítulo y sus relaciones con contenidos.
        
        Args:
            id_capitulo: ID del capítulo a eliminar
        """
        # Primero eliminar todas las uniones
        self.repositorio_union.borrar_por_capitulo(id_capitulo)
        # Luego eliminar el capítulo
        self.repositorio_capitulo.eliminar(id_capitulo)
    
    def actualizar_metadatos_capitulo(self, id_capitulo: str, datos_nuevos: Dict[str, Any]) -> Capitulo:
        """
        Actualiza los metadatos de un capítulo.
        
        Args:
            id_capitulo: ID del capítulo a actualizar
            datos_nuevos: Diccionario con los campos a actualizar
                          Puede contener: titulo, numero, introduccion, tema
            
        Returns:
            El capítulo actualizado
            
        Raises:
            ValueError: Si el capítulo no existe
        """
        capitulo = self.repositorio_capitulo.buscar_por_id(id_capitulo)
        if capitulo is None:
            raise ValueError(f"No se encontró capítulo con ID {id_capitulo}")
        
        # Actualizar solo los campos proporcionados
        if 'titulo' in datos_nuevos:
            capitulo.titulo = datos_nuevos['titulo']
        if 'numero' in datos_nuevos:
            capitulo.numero = datos_nuevos['numero']
        if 'introduccion' in datos_nuevos:
            capitulo.introduccion = datos_nuevos['introduccion']
        if 'tema' in datos_nuevos:
            capitulo.tema = datos_nuevos['tema']
        
        return self.repositorio_capitulo.guardar(capitulo)
    
    def obtener_capitulo_completo(self, id_capitulo: str) -> Tuple[Capitulo, List[Contenido]]:
        """
        Obtiene un capítulo con todos sus contenidos ordenados.
        
        Args:
            id_capitulo: ID del capítulo
            
        Returns:
            Tupla con el capítulo y la lista de contenidos ordenados
            
        Raises:
            ValueError: Si el capítulo no existe
        """
        capitulo = self.repositorio_capitulo.buscar_por_id(id_capitulo)
        if capitulo is None:
            raise ValueError(f"No se encontró capítulo con ID {id_capitulo}")
        
        # Obtener las uniones ordenadas
        uniones = self.repositorio_union.obtener_uniones_por_capitulo_ordenadas(id_capitulo)
        
        # Obtener los contenidos en el orden correcto
        contenidos = []
        for union in uniones:
            contenido = self.repositorio_contenido.buscar_por_id(union.id_contenido)
            if contenido:
                contenidos.append(contenido)
        
        return capitulo, contenidos
    
    def guardar_orden_contenido(self, id_capitulo: str, lista_ids_contenido: List[str]) -> None:
        """
        Guarda el orden de los contenidos en un capítulo.
        Elimina las uniones existentes y crea nuevas con el orden especificado.
        
        Args:
            id_capitulo: ID del capítulo
            lista_ids_contenido: Lista ordenada de IDs de contenidos
            
        Raises:
            ValueError: Si el capítulo no existe
        """
        capitulo = self.repositorio_capitulo.buscar_por_id(id_capitulo)
        if capitulo is None:
            raise ValueError(f"No se encontró capítulo con ID {id_capitulo}")
        
        # Eliminar uniones existentes del capítulo
        self.repositorio_union.borrar_por_capitulo(id_capitulo)
        
        # Crear nuevas uniones con el orden especificado
        for orden, id_contenido in enumerate(lista_ids_contenido, start=1):
            # Verificar que el contenido existe
            contenido = self.repositorio_contenido.buscar_por_id(id_contenido)
            if contenido is None:
                raise ValueError(f"No se encontró contenido con ID {id_contenido}")
            
            self.repositorio_union.crear_union(id_capitulo, id_contenido, orden)

"""
Repositorio de Unión Capítulo-Contenido
========================================
Maneja la persistencia de las relaciones entre capítulos y contenidos usando SQLAlchemy.
"""

from typing import List
from sqlalchemy.orm import Session
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from db.contenido.models import UnionCapituloContenido


class RepositorioUnionCapituloContenido:
    """
    Repositorio para gestionar las relaciones entre capítulos y contenidos.
    
    Attributes:
        db_session: Sesión de SQLAlchemy para la BD de Contenido
    """
    
    def __init__(self, db_session: Session):
        """
        Inicializa el repositorio.
        
        Args:
            db_session: Sesión de conexión a la base de datos de Contenido
        """
        self.db_session = db_session
    
    def crear_union(self, id_capitulo: str, id_contenido: str, orden: int) -> UnionCapituloContenido:
        """
        Crea una nueva unión entre capítulo y contenido.
        
        Args:
            id_capitulo: ID del capítulo
            id_contenido: ID del contenido
            orden: Orden del contenido en el capítulo
            
        Returns:
            La unión creada
        """
        try:
            union = UnionCapituloContenido(
                id_capitulo=id_capitulo,
                id_contenido=id_contenido,
                orden=orden
            )
            self.db_session.add(union)
            self.db_session.commit()
            self.db_session.refresh(union)
            return union
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Error al crear unión: {str(e)}")
    
    def borrar_por_capitulo(self, id_capitulo: str) -> None:
        """
        Elimina todas las uniones de un capítulo.
        
        Args:
            id_capitulo: ID del capítulo
        """
        try:
            self.db_session.query(UnionCapituloContenido)\
                .filter_by(id_capitulo=id_capitulo)\
                .delete()
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Error al eliminar uniones del capítulo: {str(e)}")
    
    def borrar_por_contenido(self, id_contenido: str) -> None:
        """
        Elimina todas las uniones de un contenido.
        
        Args:
            id_contenido: ID del contenido
        """
        try:
            self.db_session.query(UnionCapituloContenido)\
                .filter_by(id_contenido=id_contenido)\
                .delete()
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Error al eliminar uniones del contenido: {str(e)}")
    
    def obtener_uniones_por_capitulo_ordenadas(self, id_capitulo: str) -> List[UnionCapituloContenido]:
        """
        Obtiene todas las uniones de un capítulo ordenadas por su orden.
        
        Args:
            id_capitulo: ID del capítulo
            
        Returns:
            Lista de uniones ordenadas
        """
        return self.db_session.query(UnionCapituloContenido)\
            .filter_by(id_capitulo=id_capitulo)\
            .order_by(UnionCapituloContenido.orden)\
            .all()
    
    def obtener_uniones_por_contenido(self, id_contenido: str) -> List[UnionCapituloContenido]:
        """
        Obtiene todas las uniones de un contenido.
        
        Args:
            id_contenido: ID del contenido
            
        Returns:
            Lista de uniones
        """
        return self.db_session.query(UnionCapituloContenido)\
            .filter_by(id_contenido=id_contenido)\
            .all()

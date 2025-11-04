"""
Repositorio de Contenido
=========================
Maneja la persistencia de los objetos Contenido usando SQLAlchemy.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from db.contenido.models import Contenido, Texto, Imagen, Video, Objeto3D


class RepositorioContenido:
    """
    Repositorio para gestionar la persistencia de contenidos.
    
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
    
    def guardar(self, contenido: Contenido) -> Contenido:
        """
        Guarda o actualiza un contenido en la base de datos.
        
        Args:
            contenido: El contenido a guardar
            
        Returns:
            El contenido guardado
        """
        try:
            self.db_session.add(contenido)
            self.db_session.commit()
            self.db_session.refresh(contenido)
            return contenido
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Error al guardar contenido: {str(e)}")
    
    def buscar_por_id(self, id_contenido: str) -> Optional[Contenido]:
        """
        Busca un contenido por su ID.
        
        Args:
            id_contenido: ID del contenido a buscar
            
        Returns:
            El contenido encontrado o None si no existe
        """
        return self.db_session.query(Contenido).filter_by(id_contenido=id_contenido).first()
    
    def buscar_por_tema(self, tema: str) -> List[Contenido]:
        """
        Busca contenidos por tema.
        
        Args:
            tema: Tema a buscar
            
        Returns:
            Lista de contenidos con ese tema
        """
        return self.db_session.query(Contenido).filter_by(tema=tema).all()
    
    def listar_todos(self) -> List[Contenido]:
        """
        Lista todos los contenidos.
        
        Returns:
            Lista de todos los contenidos
        """
        return self.db_session.query(Contenido).all()
    
    def buscar_por_tipo(self, tipo: str) -> List[Contenido]:
        """
        Busca contenidos por tipo (texto, imagen, video, objeto3d).
        
        Args:
            tipo: Tipo de contenido a buscar
            
        Returns:
            Lista de contenidos del tipo especificado
        """
        return self.db_session.query(Contenido).filter_by(tipo=tipo).all()
    
    def eliminar(self, id_contenido: str) -> None:
        """
        Elimina un contenido de la base de datos.
        
        Args:
            id_contenido: ID del contenido a eliminar
        """
        try:
            contenido = self.buscar_por_id(id_contenido)
            if contenido:
                self.db_session.delete(contenido)
                self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Error al eliminar contenido: {str(e)}")

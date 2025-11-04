"""
Repositorio de Capítulo
========================
Maneja la persistencia de los objetos Capítulo usando SQLAlchemy.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from db.contenido.models import Capitulo


class RepositorioCapitulo:
    """
    Repositorio para gestionar la persistencia de capítulos.
    
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
    
    def guardar(self, capitulo: Capitulo) -> Capitulo:
        """
        Guarda o actualiza un capítulo en la base de datos.
        
        Args:
            capitulo: El capítulo a guardar
            
        Returns:
            El capítulo guardado
        """
        try:
            self.db_session.add(capitulo)
            self.db_session.commit()
            self.db_session.refresh(capitulo)
            return capitulo
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Error al guardar capítulo: {str(e)}")
    
    def buscar_por_id(self, id_capitulo: str) -> Optional[Capitulo]:
        """
        Busca un capítulo por su ID.
        
        Args:
            id_capitulo: ID del capítulo a buscar
            
        Returns:
            El capítulo encontrado o None si no existe
        """
        return self.db_session.query(Capitulo).filter_by(id_capitulo=id_capitulo).first()
    
    def buscar_por_numero(self, numero: int) -> Optional[Capitulo]:
        """
        Busca un capítulo por su número.
        
        Args:
            numero: Número del capítulo
            
        Returns:
            El capítulo encontrado o None si no existe
        """
        return self.db_session.query(Capitulo).filter_by(numero=numero).first()
    
    def buscar_por_tema(self, tema: str) -> List[Capitulo]:
        """
        Busca capítulos por tema.
        
        Args:
            tema: Tema a buscar
            
        Returns:
            Lista de capítulos con ese tema
        """
        return self.db_session.query(Capitulo).filter_by(tema=tema).all()
    
    def listar_todos(self, orden: str = "numero", ascendente: bool = True) -> List[Capitulo]:
        """
        Lista todos los capítulos ordenados.
        
        Args:
            orden: Campo por el cual ordenar (por defecto 'numero')
            ascendente: Si es True ordena ascendente, si no descendente
            
        Returns:
            Lista de todos los capítulos ordenados
        """
        query = self.db_session.query(Capitulo)
        campo_orden = getattr(Capitulo, orden, Capitulo.numero)
        
        if ascendente:
            return query.order_by(asc(campo_orden)).all()
        else:
            return query.order_by(desc(campo_orden)).all()
    
    def eliminar(self, id_capitulo: str) -> None:
        """
        Elimina un capítulo de la base de datos.
        
        Args:
            id_capitulo: ID del capítulo a eliminar
        """
        try:
            capitulo = self.buscar_por_id(id_capitulo)
            if capitulo:
                self.db_session.delete(capitulo)
                self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Error al eliminar capítulo: {str(e)}")

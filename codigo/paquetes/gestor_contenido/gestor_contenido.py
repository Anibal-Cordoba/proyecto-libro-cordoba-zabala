"""
Gestor de Contenido
====================
Implementa la lógica de negocio para la gestión de contenidos.
Versión actualizada para FastAPI con SQLAlchemy directamente.
Maneja 4 tipos de contenido: Texto, Imagen, Video, Objeto3D.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


class GestorContenido:
    """
    Gestor de la lógica de negocio para contenidos.
    Encapsula operaciones CRUD y validaciones para los 4 tipos de contenido.
    
    Attributes:
        db: Sesión de base de datos SQLAlchemy
        modelos: Diccionario con las clases de modelos
    """
    
    def __init__(self, db: Session, modelos: Dict[str, Any]):
        """
        Inicializa el gestor de contenidos.
        
        Args:
            db: Sesión de SQLAlchemy
            modelos: Dict con claves: 'Contenido', 'Texto', 'Imagen', 'Video', 'Objeto3D',
                    'Capitulo', 'UnionCapituloContenido'
        """
        self.db = db
        self.Contenido = modelos.get('Contenido')
        self.Texto = modelos.get('Texto')
        self.Imagen = modelos.get('Imagen')
        self.Video = modelos.get('Video')
        self.Objeto3D = modelos.get('Objeto3D')
        self.Capitulo = modelos.get('Capitulo')
        self.UnionCapituloContenido = modelos.get('UnionCapituloContenido')
    
    def crear_contenido(
        self,
        tipo: str,
        tema: str,
        cuerpo_texto: Optional[str] = None,
        url_archivo: Optional[str] = None,
        formato: Optional[str] = None,
        duracion: Optional[float] = None
    ) -> tuple:
        """
        Crea un nuevo contenido del tipo especificado con validaciones.
        
        Args:
            tipo: Tipo de contenido ('texto', 'imagen', 'video', 'objeto3d')
            tema: Tema del contenido
            cuerpo_texto: Contenido del texto (requerido si tipo='texto')
            url_archivo: URL del archivo (requerido para imagen, video, objeto3d)
            formato: Formato del archivo (requerido para imagen y objeto3d)
            duracion: Duración en segundos (opcional para video)
            
        Returns:
            Tupla (contenido_creado, None) si éxito
            Tupla (None, mensaje_error) si falla
        """
        try:
            if tipo == "texto":
                if not cuerpo_texto:
                    return None, "El campo 'cuerpo_texto' es requerido para contenido de tipo texto"
                
                nuevo_contenido = self.Texto(
                    tema=tema,
                    cuerpo_texto=cuerpo_texto
                )
            
            elif tipo == "imagen":
                if not url_archivo or not formato:
                    return None, "Los campos 'url_archivo' y 'formato' son requeridos para contenido de tipo imagen"
                
                nuevo_contenido = self.Imagen(
                    tema=tema,
                    url_archivo=url_archivo,
                    formato=formato
                )
            
            elif tipo == "video":
                if not url_archivo:
                    return None, "El campo 'url_archivo' es requerido para contenido de tipo video"
                
                nuevo_contenido = self.Video(
                    tema=tema,
                    url_archivo=url_archivo,
                    formato=formato,
                    duracion=duracion
                )
            
            elif tipo == "objeto3d":
                if not url_archivo or not formato:
                    return None, "Los campos 'url_archivo' y 'formato' son requeridos para contenido de tipo objeto3d"
                
                nuevo_contenido = self.Objeto3D(
                    tema=tema,
                    url_archivo=url_archivo,
                    formato=formato
                )
            
            else:
                return None, f"Tipo de contenido no válido: {tipo}"
            
            self.db.add(nuevo_contenido)
            self.db.commit()
            self.db.refresh(nuevo_contenido)
            
            return nuevo_contenido, None
            
        except IntegrityError as e:
            self.db.rollback()
            return None, f"Error de integridad: {str(e)}"
        except Exception as e:
            self.db.rollback()
            return None, f"Error al crear contenido: {str(e)}"
    
    def listar_contenidos(
        self,
        skip: int = 0,
        limit: int = 100,
        tipo: Optional[str] = None,
        tema: Optional[str] = None
    ) -> List:
        """
        Lista contenidos con filtros opcionales.
        
        Args:
            skip: Número de registros a saltar
            limit: Máximo de registros a retornar
            tipo: Filtrar por tipo de contenido
            tema: Filtrar por tema (búsqueda parcial)
            
        Returns:
            Lista de contenidos
        """
        query = self.db.query(self.Contenido)
        
        if tipo:
            query = query.filter(self.Contenido.tipo == tipo)
        
        if tema:
            query = query.filter(self.Contenido.tema.ilike(f"%{tema}%"))
        
        contenidos = query.offset(skip).limit(limit).all()
        return contenidos
    
    def obtener_contenido_por_id(self, id_contenido: str) -> tuple:
        """
        Obtiene un contenido por su ID.
        
        Args:
            id_contenido: UUID del contenido
            
        Returns:
            Tupla (contenido, None) si lo encuentra
            Tupla (None, mensaje_error) si no existe
        """
        contenido = self.db.query(self.Contenido).filter(
            self.Contenido.id_contenido == id_contenido
        ).first()
        
        if not contenido:
            return None, f"Contenido con ID {id_contenido} no encontrado"
        
        return contenido, None
    
    def eliminar_contenido(self, id_contenido: str) -> tuple:
        """
        Elimina un contenido.
        
        Args:
            id_contenido: UUID del contenido a eliminar
            
        Returns:
            Tupla (True, None) si éxito
            Tupla (False, mensaje_error) si falla
        """
        contenido = self.db.query(self.Contenido).filter(
            self.Contenido.id_contenido == id_contenido
        ).first()
        
        if not contenido:
            return False, f"Contenido con ID {id_contenido} no encontrado"
        
        try:
            self.db.delete(contenido)
            self.db.commit()
            return True, None
            
        except IntegrityError as e:
            self.db.rollback()
            return False, f"No se puede eliminar: el contenido está asignado a capítulos. Error: {str(e)}"
        except Exception as e:
            self.db.rollback()
            return False, f"Error al eliminar contenido: {str(e)}"
    
    def asignar_contenido_a_capitulo(
        self,
        id_capitulo: str,
        id_contenido: str,
        orden: int
    ) -> tuple:
        """
        Asigna un contenido a un capítulo con un orden específico.
        
        Args:
            id_capitulo: UUID del capítulo
            id_contenido: UUID del contenido
            orden: Orden del contenido dentro del capítulo
            
        Returns:
            Tupla (union_creada, None) si éxito
            Tupla (None, mensaje_error) si falla
        """
        # Verificar que el capítulo existe
        capitulo = self.db.query(self.Capitulo).filter(
            self.Capitulo.id_capitulo == id_capitulo
        ).first()
        
        if not capitulo:
            return None, f"Capítulo con ID {id_capitulo} no encontrado"
        
        # Verificar que el contenido existe
        contenido = self.db.query(self.Contenido).filter(
            self.Contenido.id_contenido == id_contenido
        ).first()
        
        if not contenido:
            return None, f"Contenido con ID {id_contenido} no encontrado"
        
        # Verificar si ya existe la asignación
        existe = self.db.query(self.UnionCapituloContenido).filter(
            self.UnionCapituloContenido.id_capitulo == id_capitulo,
            self.UnionCapituloContenido.id_contenido == id_contenido
        ).first()
        
        if existe:
            return None, "Este contenido ya está asignado a este capítulo"
        
        # Crear la unión
        try:
            union = self.UnionCapituloContenido(
                id_capitulo=id_capitulo,
                id_contenido=id_contenido,
                orden=orden
            )
            
            self.db.add(union)
            self.db.commit()
            self.db.refresh(union)
            
            return union, None
            
        except IntegrityError as e:
            self.db.rollback()
            return None, f"Error de integridad: {str(e)}"
        except Exception as e:
            self.db.rollback()
            return None, f"Error al asignar contenido: {str(e)}"
    
    def listar_contenidos_de_capitulo(self, id_capitulo: str) -> tuple:
        """
        Lista todos los contenidos de un capítulo específico, ordenados.
        
        Args:
            id_capitulo: UUID del capítulo
            
        Returns:
            Tupla (lista_contenidos, None) si éxito
            Tupla (None, mensaje_error) si falla
        """
        # Verificar que el capítulo existe
        capitulo = self.db.query(self.Capitulo).filter(
            self.Capitulo.id_capitulo == id_capitulo
        ).first()
        
        if not capitulo:
            return None, f"Capítulo con ID {id_capitulo} no encontrado"
        
        # Obtener contenidos ordenados
        uniones = self.db.query(self.UnionCapituloContenido).filter(
            self.UnionCapituloContenido.id_capitulo == id_capitulo
        ).order_by(self.UnionCapituloContenido.orden).all()
        
        contenidos = [union.contenido for union in uniones]
        return contenidos, None
    
    def desasignar_contenido_de_capitulo(
        self,
        id_capitulo: str,
        id_contenido: str
    ) -> tuple:
        """
        Desasigna un contenido de un capítulo.
        
        Args:
            id_capitulo: UUID del capítulo
            id_contenido: UUID del contenido
            
        Returns:
            Tupla (True, None) si éxito
            Tupla (False, mensaje_error) si falla
        """
        union = self.db.query(self.UnionCapituloContenido).filter(
            self.UnionCapituloContenido.id_capitulo == id_capitulo,
            self.UnionCapituloContenido.id_contenido == id_contenido
        ).first()
        
        if not union:
            return False, "Esta asignación no existe"
        
        try:
            self.db.delete(union)
            self.db.commit()
            return True, None
            
        except Exception as e:
            self.db.rollback()
            return False, f"Error al desasignar contenido: {str(e)}"

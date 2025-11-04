"""
Gestor de Capítulo
===================
Implementa la lógica de negocio para la gestión de capítulos.
Versión actualizada para FastAPI con SQLAlchemy directamente.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


class GestorCapitulo:
    """
    Gestor de la lógica de negocio para capítulos.
    Encapsula todas las operaciones CRUD y validaciones.
    
    Attributes:
        db: Sesión de base de datos SQLAlchemy
        modelo_capitulo: Clase del modelo Capitulo
    """
    
    def __init__(self, db: Session, modelo_capitulo):
        """
        Inicializa el gestor de capítulos.
        
        Args:
            db: Sesión de SQLAlchemy
            modelo_capitulo: Clase del modelo Capitulo (de db.contenido.models)
        """
        self.db = db
        self.Capitulo = modelo_capitulo
    
    def crear_capitulo(
        self, 
        numero: int, 
        titulo: str, 
        tema: str, 
        introduccion: str = "",
        estado: str = "BORRADOR"
    ) -> tuple:
        """
        Crea un nuevo capítulo con validaciones.
        
        Args:
            numero: Número del capítulo (debe ser único)
            titulo: Título del capítulo
            tema: Tema del capítulo
            introduccion: Texto de introducción (opcional)
            estado: Estado inicial (BORRADOR, PUBLICADO, ARCHIVADO)
            
        Returns:
            Tupla (capitulo_creado, None) si éxito
            Tupla (None, mensaje_error) si falla
        """
        # Validar que no exista ya un capítulo con ese número
        existe = self.db.query(self.Capitulo).filter(
            self.Capitulo.numero == numero
        ).first()
        
        if existe:
            return None, f"Ya existe un capítulo con el número {numero}"
        
        # Validar estado
        estados_validos = ["BORRADOR", "PUBLICADO", "ARCHIVADO"]
        if estado not in estados_validos:
            return None, f"Estado '{estado}' no válido. Debe ser uno de: {', '.join(estados_validos)}"
        
        # Crear nuevo capítulo
        try:
            nuevo_capitulo = self.Capitulo(
                numero=numero,
                titulo=titulo,
                tema=tema,
                introduccion=introduccion,
                estado=estado
            )
            
            self.db.add(nuevo_capitulo)
            self.db.commit()
            self.db.refresh(nuevo_capitulo)
            
            return nuevo_capitulo, None
            
        except IntegrityError as e:
            self.db.rollback()
            return None, f"Error de integridad en la base de datos: {str(e)}"
        except Exception as e:
            self.db.rollback()
            return None, f"Error inesperado al crear capítulo: {str(e)}"
    
    def listar_capitulos(
        self,
        skip: int = 0,
        limit: int = 100,
        tema: Optional[str] = None,
        estado: Optional[str] = None,
        solo_publicados: bool = False
    ) -> List:
        """
        Lista capítulos con filtros opcionales.
        
        Args:
            skip: Número de registros a saltar (paginación)
            limit: Máximo número de registros a retornar
            tema: Filtrar por tema (búsqueda parcial)
            estado: Filtrar por estado exacto
            solo_publicados: Si True, solo retorna capítulos PUBLICADOS
            
        Returns:
            Lista de capítulos que cumplen los filtros
        """
        query = self.db.query(self.Capitulo)
        
        if solo_publicados:
            query = query.filter(self.Capitulo.estado == "PUBLICADO")
        elif estado:
            query = query.filter(self.Capitulo.estado == estado)
        
        if tema:
            query = query.filter(self.Capitulo.tema.ilike(f"%{tema}%"))
        
        capitulos = query.order_by(self.Capitulo.numero).offset(skip).limit(limit).all()
        return capitulos
    
    def obtener_capitulo_por_id(self, id_capitulo: str) -> tuple:
        """
        Obtiene un capítulo por su ID.
        
        Args:
            id_capitulo: UUID del capítulo
            
        Returns:
            Tupla (capitulo, None) si lo encuentra
            Tupla (None, mensaje_error) si no existe
        """
        capitulo = self.db.query(self.Capitulo).filter(
            self.Capitulo.id_capitulo == id_capitulo
        ).first()
        
        if not capitulo:
            return None, f"Capítulo con ID {id_capitulo} no encontrado"
        
        return capitulo, None
    
    def obtener_capitulo_publicado(self, id_capitulo: str) -> tuple:
        """
        Obtiene un capítulo solo si está PUBLICADO.
        Usado para endpoints públicos.
        
        Args:
            id_capitulo: UUID del capítulo
            
        Returns:
            Tupla (capitulo, None) si está publicado
            Tupla (None, mensaje_error) si no existe o no está publicado
        """
        capitulo = self.db.query(self.Capitulo).filter(
            self.Capitulo.id_capitulo == id_capitulo,
            self.Capitulo.estado == "PUBLICADO"
        ).first()
        
        if not capitulo:
            return None, f"Capítulo con ID {id_capitulo} no encontrado"
        
        return capitulo, None
    
    def actualizar_capitulo(
        self, 
        id_capitulo: str, 
        datos_actualizacion: Dict[str, Any]
    ) -> tuple:
        """
        Actualiza un capítulo existente.
        
        Args:
            id_capitulo: UUID del capítulo a actualizar
            datos_actualizacion: Diccionario con campos a actualizar
                                 Puede incluir: numero, titulo, tema, introduccion, estado
            
        Returns:
            Tupla (capitulo_actualizado, None) si éxito
            Tupla (None, mensaje_error) si falla
        """
        # Buscar el capítulo
        capitulo = self.db.query(self.Capitulo).filter(
            self.Capitulo.id_capitulo == id_capitulo
        ).first()
        
        if not capitulo:
            return None, f"Capítulo con ID {id_capitulo} no encontrado"
        
        # Validar estado si se está actualizando
        if 'estado' in datos_actualizacion:
            estados_validos = ["BORRADOR", "PUBLICADO", "ARCHIVADO"]
            if datos_actualizacion['estado'] not in estados_validos:
                return None, f"Estado no válido. Debe ser uno de: {', '.join(estados_validos)}"
        
        # Validar número único si se está actualizando
        if 'numero' in datos_actualizacion:
            existe_otro = self.db.query(self.Capitulo).filter(
                self.Capitulo.numero == datos_actualizacion['numero'],
                self.Capitulo.id_capitulo != id_capitulo
            ).first()
            
            if existe_otro:
                return None, f"Ya existe otro capítulo con el número {datos_actualizacion['numero']}"
        
        # Actualizar campos
        try:
            for campo, valor in datos_actualizacion.items():
                if hasattr(capitulo, campo):
                    setattr(capitulo, campo, valor)
            
            self.db.commit()
            self.db.refresh(capitulo)
            
            return capitulo, None
            
        except IntegrityError as e:
            self.db.rollback()
            return None, f"Error de integridad: {str(e)}"
        except Exception as e:
            self.db.rollback()
            return None, f"Error al actualizar capítulo: {str(e)}"
    
    def eliminar_capitulo(self, id_capitulo: str) -> tuple:
        """
        Elimina un capítulo.
        
        Args:
            id_capitulo: UUID del capítulo a eliminar
            
        Returns:
            Tupla (True, None) si éxito
            Tupla (False, mensaje_error) si falla
        """
        capitulo = self.db.query(self.Capitulo).filter(
            self.Capitulo.id_capitulo == id_capitulo
        ).first()
        
        if not capitulo:
            return False, f"Capítulo con ID {id_capitulo} no encontrado"
        
        try:
            self.db.delete(capitulo)
            self.db.commit()
            return True, None
            
        except IntegrityError as e:
            self.db.rollback()
            return False, f"No se puede eliminar: el capítulo tiene contenidos asignados. Error: {str(e)}"
        except Exception as e:
            self.db.rollback()
            return False, f"Error al eliminar capítulo: {str(e)}"
    
    def cambiar_estado(self, id_capitulo: str, nuevo_estado: str) -> tuple:
        """
        Cambia el estado de un capítulo.
        
        Args:
            id_capitulo: UUID del capítulo
            nuevo_estado: Nuevo estado (BORRADOR, PUBLICADO, ARCHIVADO)
            
        Returns:
            Tupla (capitulo_actualizado, None) si éxito
            Tupla (None, mensaje_error) si falla
        """
        return self.actualizar_capitulo(id_capitulo, {'estado': nuevo_estado})
    
    def contar_capitulos(self, estado: Optional[str] = None) -> int:
        """
        Cuenta el número total de capítulos.
        
        Args:
            estado: Filtrar por estado (opcional)
            
        Returns:
            Número de capítulos
        """
        query = self.db.query(self.Capitulo)
        
        if estado:
            query = query.filter(self.Capitulo.estado == estado)
        
        return query.count()

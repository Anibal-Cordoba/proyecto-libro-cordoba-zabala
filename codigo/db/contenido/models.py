"""
Modelos SQLAlchemy para la Base de Datos de Contenido
======================================================
Tablas: capitulos, contenidos, union_capitulo_contenido
"""

from sqlalchemy import Column, String, Integer, Text, Float, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import DateTime
import uuid

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import BaseContenido


class Capitulo(BaseContenido):
    """
    Tabla: capitulos
    Almacena información de los capítulos del libro.
    """
    __tablename__ = 'capitulos'
    
    id_capitulo = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    titulo = Column(String(255), nullable=False)
    numero = Column(Integer, nullable=False, unique=True)
    introduccion = Column(Text, nullable=True)
    tema = Column(String(100), nullable=False, index=True)
    estado = Column(String(20), nullable=False, default='BORRADOR', index=True)  # BORRADOR, PUBLICADO, ARCHIVADO
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    uniones = relationship("UnionCapituloContenido", back_populates="capitulo", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Capitulo(id={self.id_capitulo}, num={self.numero}, titulo='{self.titulo}')>"


class Contenido(BaseContenido):
    """
    Tabla: contenidos
    Tabla base para todos los tipos de contenido (herencia Single Table).
    """
    __tablename__ = 'contenidos'
    
    id_contenido = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tipo = Column(String(20), nullable=False)  # 'texto', 'imagen', 'video', 'objeto3d'
    tema = Column(String(100), nullable=False, index=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Campos específicos por tipo (Single Table Inheritance)
    # Para Texto
    cuerpo_texto = Column(Text, nullable=True)
    
    # Para Imagen
    url_archivo = Column(String(500), nullable=True)  # URL de S3
    formato = Column(String(20), nullable=True)
    
    # Para Video
    duracion = Column(Float, nullable=True)  # En segundos
    
    # Relaciones
    uniones = relationship("UnionCapituloContenido", back_populates="contenido", cascade="all, delete-orphan")
    
    __mapper_args__ = {
        'polymorphic_on': tipo,
        'polymorphic_identity': 'contenido'
    }
    
    def __repr__(self):
        return f"<Contenido(id={self.id_contenido}, tipo='{self.tipo}', tema='{self.tema}')>"


class Texto(Contenido):
    """Subclase para contenido de tipo texto."""
    __mapper_args__ = {
        'polymorphic_identity': 'texto'
    }
    
    def __repr__(self):
        preview = self.cuerpo_texto[:50] if self.cuerpo_texto else ""
        return f"<Texto(id={self.id_contenido}, preview='{preview}...')>"


class Imagen(Contenido):
    """Subclase para contenido de tipo imagen."""
    __mapper_args__ = {
        'polymorphic_identity': 'imagen'
    }
    
    def __repr__(self):
        return f"<Imagen(id={self.id_contenido}, url='{self.url_archivo}', formato='{self.formato}')>"


class Video(Contenido):
    """Subclase para contenido de tipo video."""
    __mapper_args__ = {
        'polymorphic_identity': 'video'
    }
    
    def __repr__(self):
        return f"<Video(id={self.id_contenido}, url='{self.url_archivo}', duracion={self.duracion}s)>"


class Objeto3D(Contenido):
    """Subclase para contenido de tipo objeto 3D."""
    __mapper_args__ = {
        'polymorphic_identity': 'objeto3d'
    }
    
    def __repr__(self):
        return f"<Objeto3D(id={self.id_contenido}, url='{self.url_archivo}', formato='{self.formato}')>"


class UnionCapituloContenido(BaseContenido):
    """
    Tabla: union_capitulo_contenido
    Tabla de unión N:M entre capítulos y contenidos con orden.
    """
    __tablename__ = 'union_capitulo_contenido'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_capitulo = Column(String(36), ForeignKey('capitulos.id_capitulo', ondelete='CASCADE'), nullable=False)
    id_contenido = Column(String(36), ForeignKey('contenidos.id_contenido', ondelete='CASCADE'), nullable=False)
    orden = Column(Integer, nullable=False)
    
    # Relaciones
    capitulo = relationship("Capitulo", back_populates="uniones")
    contenido = relationship("Contenido", back_populates="uniones")
    
    # Índices compuestos
    __table_args__ = (
        Index('idx_capitulo_orden', 'id_capitulo', 'orden'),
        Index('idx_contenido', 'id_contenido'),
    )
    
    def __repr__(self):
        return f"<UnionCapituloContenido(capitulo={self.id_capitulo}, contenido={self.id_contenido}, orden={self.orden})>"

"""
Schemas para Capítulo
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CapituloBase(BaseModel):
    """Campos base de Capítulo"""
    titulo: str = Field(..., min_length=1, max_length=255, description="Título del capítulo")
    numero: int = Field(..., ge=1, description="Número del capítulo")
    introduccion: Optional[str] = Field(None, description="Introducción del capítulo")
    tema: str = Field(..., min_length=1, max_length=100, description="Tema principal")
    estado: str = Field(default="BORRADOR", description="Estado del capítulo: BORRADOR, PUBLICADO, ARCHIVADO")


class CapituloCreate(CapituloBase):
    """Schema para crear un capítulo"""
    pass


class CapituloUpdate(BaseModel):
    """Schema para actualizar un capítulo"""
    titulo: Optional[str] = Field(None, min_length=1, max_length=255)
    introduccion: Optional[str] = None
    tema: Optional[str] = Field(None, min_length=1, max_length=100)
    estado: Optional[str] = Field(None, description="Estado del capítulo")


class CapituloResponse(CapituloBase):
    """Schema de respuesta de capítulo"""
    id_capitulo: str
    fecha_creacion: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None
    
    class Config:
        from_attributes = True  # Permite crear desde objetos ORM

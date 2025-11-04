"""
Schemas para Contenido
"""
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class ContenidoBase(BaseModel):
    """Campos base de Contenido"""
    tipo: Literal['texto', 'imagen', 'video', 'objeto3d'] = Field(..., description="Tipo de contenido")
    tema: str = Field(..., min_length=1, max_length=100, description="Tema del contenido")


class ContenidoCreate(ContenidoBase):
    """Schema para crear contenido"""
    # Campos específicos por tipo
    cuerpo_texto: Optional[str] = None  # Para texto
    url_archivo: Optional[str] = None   # Para imagen/video/objeto3d
    formato: Optional[str] = None       # Para imagen/objeto3d
    duracion: Optional[float] = None    # Para video


class ContenidoResponse(ContenidoBase):
    """Schema de respuesta de contenido"""
    id_contenido: str
    cuerpo_texto: Optional[str] = None
    url_archivo: Optional[str] = None
    formato: Optional[str] = None
    duracion: Optional[float] = None
    fecha_creacion: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None
    
    class Config:
        from_attributes = True

"""
Router para endpoints de Contenidos (Texto, Imagen, Video, Objeto3D)
Versión refactorizada: Usa el GestorContenido para toda la lógica de negocio
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Union
import sys
from pathlib import Path

# Añadir el directorio padre al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from api.dependencies import get_db
from api.schemas.contenido import (
    ContenidoCreate, 
    ContenidoResponse,
)
from db.contenido.models import (
    Contenido, 
    Texto, 
    Imagen, 
    Video, 
    Objeto3D,
    Capitulo,
    UnionCapituloContenido
)

# Importar el gestor
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "paquetes" / "gestor_contenido"))
from gestor_contenido import GestorContenido

router = APIRouter(
    prefix="/contenidos",
    tags=["Contenidos"]
)


@router.post("/", response_model=ContenidoResponse, status_code=status.HTTP_201_CREATED)
def crear_contenido(contenido: ContenidoCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo contenido (texto, imagen, video u objeto 3D) usando el GestorContenido
    """
    modelos = {
        'Contenido': Contenido,
        'Texto': Texto,
        'Imagen': Imagen,
        'Video': Video,
        'Objeto3D': Objeto3D,
        'Capitulo': Capitulo,
        'UnionCapituloContenido': UnionCapituloContenido
    }
    
    gestor = GestorContenido(db, modelos)
    
    resultado, error = gestor.crear_contenido(
        tipo=contenido.tipo,
        tema=contenido.tema,
        cuerpo_texto=contenido.cuerpo_texto,
        url_archivo=contenido.url_archivo,
        formato=contenido.formato,
        duracion=contenido.duracion
    )
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    return resultado


@router.get("/", response_model=List[ContenidoResponse])
def listar_contenidos(
    skip: int = 0, 
    limit: int = 100,
    tipo: str = None,
    tema: str = None,
    db: Session = Depends(get_db)
):
    """
    Listar todos los contenidos con filtros opcionales usando el GestorContenido
    """
    modelos = {
        'Contenido': Contenido,
        'Texto': Texto,
        'Imagen': Imagen,
        'Video': Video,
        'Objeto3D': Objeto3D,
        'Capitulo': Capitulo,
        'UnionCapituloContenido': UnionCapituloContenido
    }
    
    gestor = GestorContenido(db, modelos)
    contenidos = gestor.listar_contenidos(skip=skip, limit=limit, tipo=tipo, tema=tema)
    return contenidos


@router.get("/{id_contenido}", response_model=ContenidoResponse)
def obtener_contenido(id_contenido: str, db: Session = Depends(get_db)):
    """
    Obtener un contenido por su ID usando el GestorContenido
    """
    modelos = {
        'Contenido': Contenido,
        'Texto': Texto,
        'Imagen': Imagen,
        'Video': Video,
        'Objeto3D': Objeto3D,
        'Capitulo': Capitulo,
        'UnionCapituloContenido': UnionCapituloContenido
    }
    
    gestor = GestorContenido(db, modelos)
    contenido, error = gestor.obtener_contenido_por_id(id_contenido)
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error
        )
    
    return contenido


@router.delete("/{id_contenido}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_contenido(id_contenido: str, db: Session = Depends(get_db)):
    """
    Eliminar un contenido usando el GestorContenido
    """
    modelos = {
        'Contenido': Contenido,
        'Texto': Texto,
        'Imagen': Imagen,
        'Video': Video,
        'Objeto3D': Objeto3D,
        'Capitulo': Capitulo,
        'UnionCapituloContenido': UnionCapituloContenido
    }
    
    gestor = GestorContenido(db, modelos)
    exito, error = gestor.eliminar_contenido(id_contenido)
    
    if not exito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if "no encontrado" in error else status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    return None


# Endpoints para asignar contenidos a capítulos
@router.post("/asignar", status_code=status.HTTP_201_CREATED)
def asignar_contenido_a_capitulo(
    id_capitulo: str,
    id_contenido: str,
    orden: int,
    db: Session = Depends(get_db)
):
    """
    Asignar un contenido a un capítulo con un orden específico usando el GestorContenido
    """
    modelos = {
        'Contenido': Contenido,
        'Texto': Texto,
        'Imagen': Imagen,
        'Video': Video,
        'Objeto3D': Objeto3D,
        'Capitulo': Capitulo,
        'UnionCapituloContenido': UnionCapituloContenido
    }
    
    gestor = GestorContenido(db, modelos)
    union, error = gestor.asignar_contenido_a_capitulo(id_capitulo, id_contenido, orden)
    
    if error:
        status_code = status.HTTP_404_NOT_FOUND if "no encontrado" in error else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=error)
    
    return {
        "message": "Contenido asignado exitosamente",
        "id": union.id,
        "id_capitulo": union.id_capitulo,
        "id_contenido": union.id_contenido,
        "orden": union.orden
    }


@router.get("/capitulo/{id_capitulo}", response_model=List[ContenidoResponse])
def listar_contenidos_de_capitulo(id_capitulo: str, db: Session = Depends(get_db)):
    """
    Listar todos los contenidos de un capítulo específico, ordenados usando el GestorContenido
    """
    modelos = {
        'Contenido': Contenido,
        'Texto': Texto,
        'Imagen': Imagen,
        'Video': Video,
        'Objeto3D': Objeto3D,
        'Capitulo': Capitulo,
        'UnionCapituloContenido': UnionCapituloContenido
    }
    
    gestor = GestorContenido(db, modelos)
    contenidos, error = gestor.listar_contenidos_de_capitulo(id_capitulo)
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error
        )
    
    return contenidos


@router.delete("/desasignar/{id_capitulo}/{id_contenido}", status_code=status.HTTP_204_NO_CONTENT)
def desasignar_contenido_de_capitulo(
    id_capitulo: str,
    id_contenido: str,
    db: Session = Depends(get_db)
):
    """
    Desasignar un contenido de un capítulo usando el GestorContenido
    """
    modelos = {
        'Contenido': Contenido,
        'Texto': Texto,
        'Imagen': Imagen,
        'Video': Video,
        'Objeto3D': Objeto3D,
        'Capitulo': Capitulo,
        'UnionCapituloContenido': UnionCapituloContenido
    }
    
    gestor = GestorContenido(db, modelos)
    exito, error = gestor.desasignar_contenido_de_capitulo(id_capitulo, id_contenido)
    
    if not exito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error
        )
    
    return None

"""
Router para endpoints de Capítulos
Versión refactorizada: Usa el GestorCapitulo para toda la lógica de negocio
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import sys
from pathlib import Path

# Añadir el directorio padre al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from api.dependencies import get_db
from api.schemas.capitulo import CapituloCreate, CapituloResponse, CapituloUpdate
from db.contenido.models import Capitulo

# Importar el gestor
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "paquetes" / "gestor_capitulo"))
from gestor_capitulo import GestorCapitulo

router = APIRouter(
    prefix="/capitulos",
    tags=["Capítulos"]
)


@router.post("/", response_model=CapituloResponse, status_code=status.HTTP_201_CREATED)
def crear_capitulo(capitulo: CapituloCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo capítulo usando el GestorCapitulo
    """
    gestor = GestorCapitulo(db, Capitulo)
    
    resultado, error = gestor.crear_capitulo(
        numero=capitulo.numero,
        titulo=capitulo.titulo,
        tema=capitulo.tema,
        introduccion=capitulo.introduccion,
        estado=capitulo.estado
    )
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    return resultado


@router.get("/", response_model=List[CapituloResponse])
def listar_capitulos(
    skip: int = 0,
    limit: int = 100,
    tema: str = None,
    db: Session = Depends(get_db)
):
    """
    Listar todos los capítulos usando el GestorCapitulo
    """
    gestor = GestorCapitulo(db, Capitulo)
    capitulos = gestor.listar_capitulos(skip=skip, limit=limit, tema=tema)
    return capitulos


@router.get("/{capitulo_id}", response_model=CapituloResponse)
def obtener_capitulo(capitulo_id: str, db: Session = Depends(get_db)):
    """
    Obtener un capítulo por ID usando el GestorCapitulo
    """
    gestor = GestorCapitulo(db, Capitulo)
    capitulo, error = gestor.obtener_capitulo_por_id(capitulo_id)
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error
        )
    
    return capitulo


@router.put("/{capitulo_id}", response_model=CapituloResponse)
def actualizar_capitulo(
    capitulo_id: str,
    capitulo_update: CapituloUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar un capítulo usando el GestorCapitulo
    """
    gestor = GestorCapitulo(db, Capitulo)
    
    # Convertir a diccionario solo los campos proporcionados
    update_data = capitulo_update.model_dump(exclude_unset=True)
    
    resultado, error = gestor.actualizar_capitulo(capitulo_id, update_data)
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if "no encontrado" in error else status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    return resultado


@router.delete("/{capitulo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_capitulo(capitulo_id: str, db: Session = Depends(get_db)):
    """
    Eliminar un capítulo usando el GestorCapitulo
    """
    gestor = GestorCapitulo(db, Capitulo)
    exito, error = gestor.eliminar_capitulo(capitulo_id)
    
    if not exito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if "no encontrado" in error else status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    return None

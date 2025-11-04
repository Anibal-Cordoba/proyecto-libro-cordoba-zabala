"""
Router para endpoints de Capítulos
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

router = APIRouter(
    prefix="/capitulos",
    tags=["Capítulos"]
)


@router.post("/", response_model=CapituloResponse, status_code=status.HTTP_201_CREATED)
def crear_capitulo(capitulo: CapituloCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo capítulo
    """
    # Verificar que no exista ya un capítulo con ese número
    existe = db.query(Capitulo).filter(Capitulo.numero == capitulo.numero).first()
    if existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un capítulo con el número {capitulo.numero}"
        )
    
    # Crear nuevo capítulo
    db_capitulo = Capitulo(**capitulo.model_dump())
    db.add(db_capitulo)
    db.commit()
    db.refresh(db_capitulo)
    
    return db_capitulo


@router.get("/", response_model=List[CapituloResponse])
def listar_capitulos(
    skip: int = 0,
    limit: int = 100,
    tema: str = None,
    db: Session = Depends(get_db)
):
    """
    Listar todos los capítulos
    """
    query = db.query(Capitulo)
    
    if tema:
        query = query.filter(Capitulo.tema.ilike(f"%{tema}%"))
    
    capitulos = query.order_by(Capitulo.numero).offset(skip).limit(limit).all()
    return capitulos


@router.get("/{capitulo_id}", response_model=CapituloResponse)
def obtener_capitulo(capitulo_id: str, db: Session = Depends(get_db)):
    """
    Obtener un capítulo por ID
    """
    capitulo = db.query(Capitulo).filter(Capitulo.id_capitulo == capitulo_id).first()
    
    if not capitulo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Capítulo con ID {capitulo_id} no encontrado"
        )
    
    return capitulo


@router.put("/{capitulo_id}", response_model=CapituloResponse)
def actualizar_capitulo(
    capitulo_id: str,
    capitulo_update: CapituloUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar un capítulo
    """
    db_capitulo = db.query(Capitulo).filter(Capitulo.id_capitulo == capitulo_id).first()
    
    if not db_capitulo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Capítulo con ID {capitulo_id} no encontrado"
        )
    
    # Actualizar solo los campos proporcionados
    update_data = capitulo_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_capitulo, field, value)
    
    db.commit()
    db.refresh(db_capitulo)
    
    return db_capitulo


@router.delete("/{capitulo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_capitulo(capitulo_id: str, db: Session = Depends(get_db)):
    """
    Eliminar un capítulo
    """
    db_capitulo = db.query(Capitulo).filter(Capitulo.id_capitulo == capitulo_id).first()
    
    if not db_capitulo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Capítulo con ID {capitulo_id} no encontrado"
        )
    
    db.delete(db_capitulo)
    db.commit()
    
    return None

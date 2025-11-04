"""
Configuración de Pytest y Fixtures Compartidos
===============================================
Configuración central para todos los tests.
"""

import pytest
import sys
import os
from pathlib import Path

# IMPORTANTE: Establecer variable de entorno ANTES de importar módulos
os.environ["TESTING"] = "true"

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

# Agregar el directorio api al path
api_path = Path(__file__).parent.parent / "api"
sys.path.insert(0, str(api_path))

# Importar modelos y configuración
from db.config import BaseContenido
from db.contenido.models import Capitulo, Contenido, UnionCapituloContenido

# Importar API (ya usará BD en memoria por TESTING=true)
import main as api_main
from dependencies import get_db, engine as test_engine

app = api_main.app


def pytest_configure(config):
    """Hook que se ejecuta al iniciar pytest, antes de cualquier test."""
    # Crear todas las tablas en la BD de test
    BaseContenido.metadata.create_all(bind=test_engine)
    print(f"\n✅ Tablas creadas en BD de test")


def pytest_unconfigure(config):
    """Hook que se ejecuta al finalizar todos los tests."""
    # Eliminar la base de datos temporal
    import os
    test_db_path = Path(__file__).parent.parent / "data" / "test_contenido.db"
    if test_db_path.exists():
        os.remove(test_db_path)
        print(f"\n🗑️  BD de test eliminada")


# ===== FIXTURES DE BASE DE DATOS =====

@pytest.fixture(scope="function", autouse=True)
def clean_db():
    """
    Limpia la base de datos antes de cada test.
    Se ejecuta automáticamente para todos los tests.
    """
    # Limpiar datos antes del test
    from dependencies import SessionLocal
    db = SessionLocal()
    try:
        db.query(UnionCapituloContenido).delete()
        db.query(Contenido).delete()
        db.query(Capitulo).delete()
        db.commit()
    except:
        db.rollback()
    finally:
        db.close()
    
    yield
    
    # Limpiar datos después del test
    db = SessionLocal()
    try:
        db.query(UnionCapituloContenido).delete()
        db.query(Contenido).delete()
        db.query(Capitulo).delete()
        db.commit()
    except:
        db.rollback()
    finally:
        db.close()


@pytest.fixture(scope="function")
def test_db_session():
    """
    Crea una sesión de base de datos para tests.
    Usa la misma configuración que la API (BD en memoria por TESTING=true).
    """
    from dependencies import SessionLocal
    
    session = SessionLocal()
    
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client():
    """
    Cliente de prueba de FastAPI.
    Ya usa automáticamente la BD en memoria por TESTING=true.
    """
    with TestClient(app) as test_client:
        yield test_client


# ===== FIXTURES DE DATOS DE PRUEBA =====

@pytest.fixture
def capitulo_borrador(test_db_session):
    """Crea un capítulo en estado BORRADOR para pruebas."""
    capitulo = Capitulo(
        titulo="Capítulo de Prueba - Borrador",
        numero=1,
        tema="Testing",
        introduccion="Este es un capítulo de prueba en estado borrador.",
        estado="BORRADOR"
    )
    test_db_session.add(capitulo)
    test_db_session.commit()
    test_db_session.refresh(capitulo)
    return capitulo


@pytest.fixture
def capitulo_publicado(test_db_session):
    """
    Crea un capítulo en estado PUBLICADO para pruebas.
    Este es el caso principal para CP01_01.
    """
    capitulo = Capitulo(
        titulo="Introducción a las Estructuras de Datos",
        numero=2,
        tema="Algoritmos y Estructuras",
        introduccion="En este capítulo exploraremos los fundamentos de las estructuras de datos más importantes.",
        estado="PUBLICADO"
    )
    test_db_session.add(capitulo)
    test_db_session.commit()
    test_db_session.refresh(capitulo)
    return capitulo


@pytest.fixture
def capitulo_archivado(test_db_session):
    """Crea un capítulo en estado ARCHIVADO para pruebas."""
    capitulo = Capitulo(
        titulo="Capítulo Archivado",
        numero=3,
        tema="Contenido Antiguo",
        introduccion="Este capítulo ha sido archivado.",
        estado="ARCHIVADO"
    )
    test_db_session.add(capitulo)
    test_db_session.commit()
    test_db_session.refresh(capitulo)
    return capitulo


@pytest.fixture
def multiples_capitulos(test_db_session):
    """Crea varios capítulos en diferentes estados."""
    capitulos = [
        Capitulo(
            titulo=f"Capítulo {i}",
            numero=i,
            tema="Testing Multiple",
            introduccion=f"Introducción del capítulo {i}",
            estado=estado
        )
        for i, estado in enumerate([
            "PUBLICADO", "PUBLICADO", "BORRADOR", 
            "PUBLICADO", "ARCHIVADO"
        ], start=10)
    ]
    
    for cap in capitulos:
        test_db_session.add(cap)
    
    test_db_session.commit()
    
    for cap in capitulos:
        test_db_session.refresh(cap)
    
    return capitulos


@pytest.fixture
def contenido_texto(test_db_session):
    """Crea contenido de tipo texto."""
    contenido = Contenido(
        tipo="texto",
        tema="Testing",
        cuerpo_texto="Este es un texto de prueba para el capítulo."
    )
    test_db_session.add(contenido)
    test_db_session.commit()
    test_db_session.refresh(contenido)
    return contenido


@pytest.fixture
def capitulo_con_contenido(test_db_session, capitulo_publicado, contenido_texto):
    """Crea un capítulo publicado con contenido asociado."""
    union = UnionCapituloContenido(
        id_capitulo=capitulo_publicado.id_capitulo,
        id_contenido=contenido_texto.id_contenido,
        orden=1
    )
    test_db_session.add(union)
    test_db_session.commit()
    test_db_session.refresh(capitulo_publicado)
    return capitulo_publicado


# ===== FIXTURES DE UTILIDADES =====

@pytest.fixture
def sample_capitulo_data():
    """Datos de ejemplo para crear un capítulo."""
    return {
        "titulo": "Nuevo Capítulo",
        "numero": 99,
        "tema": "Testing",
        "introduccion": "Introducción de prueba",
        "estado": "BORRADOR"
    }


@pytest.fixture
def capitulo_publicado_data():
    """Datos de ejemplo para un capítulo publicado."""
    return {
        "titulo": "Capítulo Publicado de Prueba",
        "numero": 100,
        "tema": "Testing Publicación",
        "introduccion": "Este capítulo está listo para ser visualizado.",
        "estado": "PUBLICADO"
    }

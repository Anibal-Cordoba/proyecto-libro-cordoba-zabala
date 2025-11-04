"""
Dependencias de la API
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Configuración de base de datos
# Para desarrollo usamos SQLite, para producción MySQL
USE_SQLITE = os.getenv("USE_SQLITE", "true").lower() == "true"

if USE_SQLITE:
    # Base de datos SQLite en el directorio del proyecto
    db_path = Path(__file__).parent.parent / "data" / "contenido.db"
    db_path.parent.mkdir(exist_ok=True)
    DATABASE_URL = f"sqlite:///{db_path}"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # Base de datos MySQL
    DATABASE_URL = os.getenv(
        "DATABASE_URL_CONTENIDO",
        "mysql+pymysql://user:password@localhost:3306/contenido_db"
    )
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency para obtener una sesión de base de datos.
    Se cierra automáticamente al finalizar.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

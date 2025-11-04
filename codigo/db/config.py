"""
Configuración de Bases de Datos
================================
Configuración de conexiones a las 3 bases de datos MySQL en AWS RDS.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Optional


class DatabaseConfig:
    """Configuración centralizada de las 3 bases de datos."""
    
    # Base de Datos de Contenido
    CONTENIDO_DB_USER = os.getenv('CONTENIDO_DB_USER', 'admin')
    CONTENIDO_DB_PASSWORD = os.getenv('CONTENIDO_DB_PASSWORD', 'password')
    CONTENIDO_DB_HOST = os.getenv('CONTENIDO_DB_HOST', 'localhost')
    CONTENIDO_DB_PORT = os.getenv('CONTENIDO_DB_PORT', '3306')
    CONTENIDO_DB_NAME = os.getenv('CONTENIDO_DB_NAME', 'contenido_db')
    
    # Base de Datos de Usuarios
    USUARIOS_DB_USER = os.getenv('USUARIOS_DB_USER', 'admin')
    USUARIOS_DB_PASSWORD = os.getenv('USUARIOS_DB_PASSWORD', 'password')
    USUARIOS_DB_HOST = os.getenv('USUARIOS_DB_HOST', 'localhost')
    USUARIOS_DB_PORT = os.getenv('USUARIOS_DB_PORT', '3306')
    USUARIOS_DB_NAME = os.getenv('USUARIOS_DB_NAME', 'usuarios_db')
    
    # Base de Datos de Evaluaciones
    EVALUACIONES_DB_USER = os.getenv('EVALUACIONES_DB_USER', 'admin')
    EVALUACIONES_DB_PASSWORD = os.getenv('EVALUACIONES_DB_PASSWORD', 'password')
    EVALUACIONES_DB_HOST = os.getenv('EVALUACIONES_DB_HOST', 'localhost')
    EVALUACIONES_DB_PORT = os.getenv('EVALUACIONES_DB_PORT', '3306')
    EVALUACIONES_DB_NAME = os.getenv('EVALUACIONES_DB_NAME', 'evaluaciones_db')
    
    @classmethod
    def get_contenido_url(cls) -> str:
        """Construye URL de conexión para BD de Contenido."""
        return f"mysql+pymysql://{cls.CONTENIDO_DB_USER}:{cls.CONTENIDO_DB_PASSWORD}@{cls.CONTENIDO_DB_HOST}:{cls.CONTENIDO_DB_PORT}/{cls.CONTENIDO_DB_NAME}?charset=utf8mb4"
    
    @classmethod
    def get_usuarios_url(cls) -> str:
        """Construye URL de conexión para BD de Usuarios."""
        return f"mysql+pymysql://{cls.USUARIOS_DB_USER}:{cls.USUARIOS_DB_PASSWORD}@{cls.USUARIOS_DB_HOST}:{cls.USUARIOS_DB_PORT}/{cls.USUARIOS_DB_NAME}?charset=utf8mb4"
    
    @classmethod
    def get_evaluaciones_url(cls) -> str:
        """Construye URL de conexión para BD de Evaluaciones."""
        return f"mysql+pymysql://{cls.EVALUACIONES_DB_USER}:{cls.EVALUACIONES_DB_PASSWORD}@{cls.EVALUACIONES_DB_HOST}:{cls.EVALUACIONES_DB_PORT}/{cls.EVALUACIONES_DB_NAME}?charset=utf8mb4"


# Bases declarativas para cada BD
BaseContenido = declarative_base()
BaseUsuarios = declarative_base()
BaseEvaluaciones = declarative_base()

# Engines y SessionMakers
contenido_engine = None
usuarios_engine = None
evaluaciones_engine = None

ContenidoSession = None
UsuariosSession = None
EvaluacionesSession = None


def init_contenido_db(echo: bool = False):
    """Inicializa la base de datos de Contenido."""
    global contenido_engine, ContenidoSession
    
    contenido_engine = create_engine(
        DatabaseConfig.get_contenido_url(),
        echo=echo,
        pool_pre_ping=True,
        pool_recycle=3600
    )
    ContenidoSession = sessionmaker(bind=contenido_engine)
    return contenido_engine


def init_usuarios_db(echo: bool = False):
    """Inicializa la base de datos de Usuarios."""
    global usuarios_engine, UsuariosSession
    
    usuarios_engine = create_engine(
        DatabaseConfig.get_usuarios_url(),
        echo=echo,
        pool_pre_ping=True,
        pool_recycle=3600
    )
    UsuariosSession = sessionmaker(bind=usuarios_engine)
    return usuarios_engine


def init_evaluaciones_db(echo: bool = False):
    """Inicializa la base de datos de Evaluaciones."""
    global evaluaciones_engine, EvaluacionesSession
    
    evaluaciones_engine = create_engine(
        DatabaseConfig.get_evaluaciones_url(),
        echo=echo,
        pool_pre_ping=True,
        pool_recycle=3600
    )
    EvaluacionesSession = sessionmaker(bind=evaluaciones_engine)
    return evaluaciones_engine


def get_contenido_session():
    """Obtiene una sesión de la BD de Contenido."""
    if ContenidoSession is None:
        init_contenido_db()
    return ContenidoSession()


def get_usuarios_session():
    """Obtiene una sesión de la BD de Usuarios."""
    if UsuariosSession is None:
        init_usuarios_db()
    return UsuariosSession()


def get_evaluaciones_session():
    """Obtiene una sesión de la BD de Evaluaciones."""
    if EvaluacionesSession is None:
        init_evaluaciones_db()
    return EvaluacionesSession()


def create_all_tables():
    """Crea todas las tablas en las 3 bases de datos."""
    # Importar modelos para registrarlos
    from .contenido import models as contenido_models
    from .usuarios import models as usuarios_models
    from .evaluaciones import models as evaluaciones_models
    
    # Crear tablas
    if contenido_engine:
        BaseContenido.metadata.create_all(contenido_engine)
    if usuarios_engine:
        BaseUsuarios.metadata.create_all(usuarios_engine)
    if evaluaciones_engine:
        BaseEvaluaciones.metadata.create_all(evaluaciones_engine)

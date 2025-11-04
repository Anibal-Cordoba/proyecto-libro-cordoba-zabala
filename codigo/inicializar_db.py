"""
Script para crear las tablas de la base de datos
"""
import sys
from pathlib import Path

# Agregar el directorio padre al path
sys.path.insert(0, str(Path(__file__).parent))

# IMPORTANTE: Importar los modelos ANTES del engine para que se registren
from db.contenido.models import Capitulo, Contenido, UnionCapituloContenido, BaseContenido
from api.dependencies import engine

def crear_tablas():
    """Crea todas las tablas en la base de datos"""
    print("🔨 Creando tablas en la base de datos...")
    print(f"📍 Base de datos: {engine.url}")
    print(f"📦 Modelos registrados: Capitulo, Contenido, UnionCapituloContenido")
    
    # Crear todas las tablas
    BaseContenido.metadata.create_all(bind=engine)
    print("✅ Tablas creadas exitosamente!")
    
    # Mostrar las tablas creadas
    print("\n📋 Tablas creadas:")
    for table_name in BaseContenido.metadata.tables.keys():
        print(f"  - {table_name}")
    
    # Verificar que las tablas existen
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables_in_db = inspector.get_table_names()
    print(f"\n✓ Tablas en la base de datos: {tables_in_db}")

if __name__ == "__main__":
    crear_tablas()

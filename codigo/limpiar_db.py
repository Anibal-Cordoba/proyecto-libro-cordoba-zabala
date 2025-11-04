"""
Script para limpiar la base de datos de desarrollo
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.contenido.models import Capitulo, Contenido, UnionCapituloContenido

# Conexión a la BD de desarrollo
DATABASE_URL = "sqlite:///./data/contenido.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def limpiar_todo():
    """Elimina todos los datos de todas las tablas"""
    db = SessionLocal()
    try:
        # Contar antes
        count_caps = db.query(Capitulo).count()
        count_conts = db.query(Contenido).count()
        count_unions = db.query(UnionCapituloContenido).count()
        
        print(f"📊 Estado actual:")
        print(f"   - Capítulos: {count_caps}")
        print(f"   - Contenidos: {count_conts}")
        print(f"   - Asignaciones: {count_unions}")
        print()
        
        # Eliminar todo
        db.query(UnionCapituloContenido).delete()
        db.query(Contenido).delete()
        db.query(Capitulo).delete()
        db.commit()
        
        print("✅ Base de datos limpiada exitosamente")
        print("   - Todos los capítulos eliminados")
        print("   - Todos los contenidos eliminados")
        print("   - Todas las asignaciones eliminadas")
        
    except Exception as e:
        print(f"❌ Error al limpiar: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    respuesta = input("⚠️  ¿Eliminar TODOS los datos? (escribe 'SI' para confirmar): ")
    if respuesta.upper() == "SI":
        limpiar_todo()
    else:
        print("❌ Operación cancelada")

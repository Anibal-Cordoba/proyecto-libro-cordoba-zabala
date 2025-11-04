"""
Script para eliminar solo capítulos de prueba
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.contenido.models import Capitulo

# Conexión a la BD de desarrollo
DATABASE_URL = "sqlite:///./data/contenido.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def limpiar_tests():
    """Elimina capítulos que parecen de prueba"""
    db = SessionLocal()
    try:
        # Contar antes
        total = db.query(Capitulo).count()
        print(f"📊 Total de capítulos: {total}")
        
        # Capítulos con número > 100 (probablemente de tests)
        caps_test = db.query(Capitulo).filter(Capitulo.numero > 100).all()
        print(f"   - Con número > 100: {len(caps_test)}")
        
        # Capítulos con tema "Testing" o "Test"
        caps_testing = db.query(Capitulo).filter(
            (Capitulo.tema.like('%Test%')) | 
            (Capitulo.titulo.like('%Test%')) |
            (Capitulo.titulo.like('%Prueba%'))
        ).all()
        print(f"   - Con 'Test' o 'Prueba': {len(caps_testing)}")
        print()
        
        respuesta = input("¿Eliminar estos capítulos? (SI para confirmar): ")
        
        if respuesta.upper() == "SI":
            # Eliminar capítulos con número > 100
            deleted = db.query(Capitulo).filter(Capitulo.numero > 100).delete()
            
            # Eliminar capítulos de testing
            deleted += db.query(Capitulo).filter(
                (Capitulo.tema.like('%Test%')) | 
                (Capitulo.titulo.like('%Test%')) |
                (Capitulo.titulo.like('%Prueba%'))
            ).delete()
            
            db.commit()
            
            print(f"✅ Eliminados {deleted} capítulos de prueba")
            print(f"📊 Capítulos restantes: {db.query(Capitulo).count()}")
        else:
            print("❌ Operación cancelada")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    limpiar_tests()

#!/usr/bin/env python3
"""
Migración: Agregar columna 'estado' a la tabla capitulos
=========================================================
Agrega la columna estado con valores: BORRADOR, PUBLICADO, ARCHIVADO
"""

import sys
import os
from pathlib import Path

# Agregar el directorio padre al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import pymysql

load_dotenv()

def migrar_agregar_estado():
    """Agrega la columna estado a la tabla capitulos si no existe."""
    
    print("=" * 60)
    print("  MIGRACIÓN: Agregar columna 'estado' a capitulos")
    print("=" * 60)
    print()
    
    # Obtener URL de BD
    database_url = os.getenv(
        "DATABASE_URL_CONTENIDO",
        "mysql+pymysql://admin:LibroInteractivo2024@contenido-db.cxj9cqxample.us-east-1.rds.amazonaws.com:3306/contenido_db"
    )
    
    print(f"📦 Conectando a base de datos...")
    
    try:
        # Crear engine
        engine = create_engine(database_url, pool_pre_ping=True)
        
        with engine.connect() as conn:
            # Verificar si la columna ya existe
            check_query = text("""
                SELECT COUNT(*) as count
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'capitulos'
                AND COLUMN_NAME = 'estado'
            """)
            
            result = conn.execute(check_query)
            existe = result.scalar()
            
            if existe:
                print("⚠️  La columna 'estado' ya existe en la tabla capitulos")
                print("✅ No se requiere migración")
                return True
            
            print("➕ Agregando columna 'estado' a tabla capitulos...")
            
            # Agregar columna
            alter_query = text("""
                ALTER TABLE capitulos
                ADD COLUMN estado VARCHAR(20) NOT NULL DEFAULT 'BORRADOR'
                AFTER tema
            """)
            
            conn.execute(alter_query)
            conn.commit()
            
            print("✅ Columna agregada exitosamente")
            
            # Agregar índice para mejorar performance
            print("🔍 Agregando índice para columna estado...")
            
            index_query = text("""
                CREATE INDEX idx_estado ON capitulos(estado)
            """)
            
            try:
                conn.execute(index_query)
                conn.commit()
                print("✅ Índice creado exitosamente")
            except Exception as e:
                if "Duplicate key name" in str(e):
                    print("⚠️  El índice ya existe")
                else:
                    print(f"⚠️  No se pudo crear índice: {e}")
            
            # Actualizar capítulos existentes (opcional)
            print("\n📝 Actualizando capítulos existentes...")
            update_query = text("""
                UPDATE capitulos 
                SET estado = 'PUBLICADO' 
                WHERE estado = 'BORRADOR'
            """)
            
            result = conn.execute(update_query)
            conn.commit()
            
            print(f"✅ {result.rowcount} capítulos actualizados a PUBLICADO")
            
        print("\n" + "=" * 60)
        print("  ✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error durante la migración: {e}")
        print("\nDetalles del error:")
        import traceback
        traceback.print_exc()
        return False


def verificar_migracion():
    """Verifica que la migración se haya aplicado correctamente."""
    
    print("\n🔍 Verificando migración...")
    
    database_url = os.getenv("DATABASE_URL_CONTENIDO")
    engine = create_engine(database_url, pool_pre_ping=True)
    
    with engine.connect() as conn:
        # Verificar estructura
        query = text("""
            DESCRIBE capitulos
        """)
        
        result = conn.execute(query)
        columnas = result.fetchall()
        
        print("\n📋 Estructura de tabla capitulos:")
        for col in columnas:
            print(f"   - {col[0]}: {col[1]}")
            if col[0] == 'estado':
                print(f"     ✅ Columna 'estado' encontrada")
        
        # Verificar datos
        query = text("""
            SELECT estado, COUNT(*) as count
            FROM capitulos
            GROUP BY estado
        """)
        
        result = conn.execute(query)
        estados = result.fetchall()
        
        if estados:
            print("\n📊 Distribución de estados:")
            for estado, count in estados:
                print(f"   - {estado}: {count} capítulos")
        else:
            print("\n⚠️  No hay capítulos en la base de datos")


if __name__ == "__main__":
    print()
    
    if migrar_agregar_estado():
        verificar_migracion()
        print("\n✨ Todo listo para ejecutar tests!")
        print("   Ejecuta: ./ejecutar_tests.sh")
    else:
        print("\n❌ La migración falló. Revisa los errores arriba.")
        sys.exit(1)

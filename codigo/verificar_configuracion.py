#!/usr/bin/env python3
"""
Script de Verificación de Configuración
========================================
Verifica que todo esté listo para usar la API
"""
import sys
import os
from pathlib import Path

def check_env_file():
    """Verifica archivo .env"""
    print("1️⃣ Verificando archivo .env...")
    
    if not os.path.exists('.env'):
        print("   ❌ Archivo .env no encontrado")
        print()
        print("   Solución: Copia el archivo de ejemplo")
        print("   $ cp .env.example .env")
        print("   $ nano .env  # Edita con tus credenciales")
        return False
    
    print("   ✅ Archivo .env existe")
    return True


def check_database_config():
    """Verifica configuración de BD"""
    print("\n2️⃣ Verificando configuración de base de datos...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        db_url = os.getenv('DATABASE_URL_CONTENIDO')
        
        if not db_url or 'password' in db_url.lower():
            print("   ⚠️  DATABASE_URL_CONTENIDO necesita configuración")
            print()
            print("   Edita .env y configura:")
            print("   DATABASE_URL_CONTENIDO=mysql+pymysql://user:pass@host:3306/contenido_db")
            return False
        
        print("   ✅ DATABASE_URL_CONTENIDO configurada")
        return True
        
    except ImportError:
        print("   ⚠️  python-dotenv no instalado")
        print("   $ pip install python-dotenv")
        return False


def check_database_connection():
    """Verifica conexión a BD"""
    print("\n3️⃣ Probando conexión a base de datos...")
    
    try:
        from dotenv import load_dotenv
        from sqlalchemy import create_engine, text
        
        load_dotenv()
        db_url = os.getenv('DATABASE_URL_CONTENIDO')
        
        if not db_url:
            print("   ⚠️  DATABASE_URL_CONTENIDO no configurada")
            return False
        
        engine = create_engine(db_url, pool_pre_ping=True)
        
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("   ✅ Conexión a base de datos exitosa")
            return True
            
    except ImportError as e:
        print(f"   ⚠️  Falta instalar dependencias: {e}")
        print("   $ pip install sqlalchemy pymysql python-dotenv")
        return False
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        print()
        print("   Posibles causas:")
        print("   - MySQL no está corriendo")
        print("   - Credenciales incorrectas en .env")
        print("   - Base de datos no existe")
        return False


def check_tables():
    """Verifica que existan las tablas"""
    print("\n4️⃣ Verificando tablas de base de datos...")
    
    try:
        from dotenv import load_dotenv
        from sqlalchemy import create_engine, text
        
        load_dotenv()
        db_url = os.getenv('DATABASE_URL_CONTENIDO')
        
        engine = create_engine(db_url, pool_pre_ping=True)
        
        with engine.connect() as conn:
            result = conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            
            required_tables = ['capitulos', 'contenidos', 'union_capitulo_contenido']
            missing = [t for t in required_tables if t not in tables]
            
            if missing:
                print(f"   ⚠️  Faltan tablas: {', '.join(missing)}")
                print()
                print("   Solución: Crear las tablas")
                print("   $ python db/crear_tablas.py")
                return False
            
            print(f"   ✅ Todas las tablas existen ({len(tables)} tablas)")
            return True
            
    except Exception as e:
        print(f"   ⚠️  No se pudieron verificar las tablas: {e}")
        return False


def check_packages():
    """Verifica que los paquetes estén instalados"""
    print("\n5️⃣ Verificando paquetes instalados...")
    
    try:
        import subprocess
        result = subprocess.run(
            ['pip', 'list'], 
            capture_output=True, 
            text=True
        )
        
        packages = result.stdout
        
        required = [
            'libro-modelo-capitulo',
            'libro-repositorio-capitulo',
            'fastapi',
            'uvicorn',
            'sqlalchemy'
        ]
        
        missing = [p for p in required if p not in packages]
        
        if missing:
            print(f"   ⚠️  Faltan paquetes: {', '.join(missing)}")
            print()
            print("   Solución:")
            print("   $ bash instalar_paquetes.sh")
            return False
        
        print("   ✅ Todos los paquetes instalados")
        return True
        
    except Exception as e:
        print(f"   ⚠️  Error al verificar paquetes: {e}")
        return False


def main():
    """Ejecuta todas las verificaciones"""
    print("=" * 70)
    print("  VERIFICACIÓN DE CONFIGURACIÓN PARA LA API")
    print("=" * 70)
    print()
    
    checks = [
        check_env_file(),
        check_database_config(),
        check_packages(),
        check_database_connection(),
        check_tables(),
    ]
    
    print()
    print("=" * 70)
    
    if all(checks):
        print("  ✅ TODO LISTO - PUEDES INICIAR LA API")
        print("=" * 70)
        print()
        print("Inicia la API con:")
        print("  $ bash iniciar_api.sh")
        print()
        print("Luego visita:")
        print("  http://localhost:8000")
        print()
        return 0
    else:
        print("  ⚠️  HAY PROBLEMAS DE CONFIGURACIÓN")
        print("=" * 70)
        print()
        print("Revisa los mensajes anteriores y corrige los problemas.")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())

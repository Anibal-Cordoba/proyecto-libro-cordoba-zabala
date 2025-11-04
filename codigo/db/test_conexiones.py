"""
Script de Prueba de Conexiones a las 3 Bases de Datos
======================================================
Verifica que las conexiones a RDS MySQL funcionen correctamente.
"""

import sys
import os
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.config import (
    DatabaseConfig,
    init_contenido_db,
    init_usuarios_db,
    init_evaluaciones_db,
    get_contenido_session,
    get_usuarios_session,
    get_evaluaciones_session
)


def test_contenido_db():
    """Prueba la conexión a la BD de Contenido."""
    print("\n" + "="*60)
    print("Probando Base de Datos: CONTENIDO")
    print("="*60)
    
    try:
        print(f"Host: {DatabaseConfig.CONTENIDO_DB_HOST}")
        print(f"Base de datos: {DatabaseConfig.CONTENIDO_DB_NAME}")
        print("\nInicializando conexión...")
        
        engine = init_contenido_db(echo=False)
        print("✓ Engine creado")
        
        session = get_contenido_session()
        print("✓ Sesión obtenida")
        
        # Ejecutar query simple
        result = session.execute("SELECT 1 as test")
        row = result.fetchone()
        print(f"✓ Query ejecutado: {row[0]}")
        
        session.close()
        print("✓ Sesión cerrada")
        
        print("\n✅ Conexión a contenido_db: EXITOSA")
        return True
        
    except Exception as e:
        print(f"\n❌ Error en contenido_db: {str(e)}")
        return False


def test_usuarios_db():
    """Prueba la conexión a la BD de Usuarios."""
    print("\n" + "="*60)
    print("Probando Base de Datos: USUARIOS")
    print("="*60)
    
    try:
        print(f"Host: {DatabaseConfig.USUARIOS_DB_HOST}")
        print(f"Base de datos: {DatabaseConfig.USUARIOS_DB_NAME}")
        print("\nInicializando conexión...")
        
        engine = init_usuarios_db(echo=False)
        print("✓ Engine creado")
        
        session = get_usuarios_session()
        print("✓ Sesión obtenida")
        
        # Ejecutar query simple
        result = session.execute("SELECT 1 as test")
        row = result.fetchone()
        print(f"✓ Query ejecutado: {row[0]}")
        
        session.close()
        print("✓ Sesión cerrada")
        
        print("\n✅ Conexión a usuarios_db: EXITOSA")
        return True
        
    except Exception as e:
        print(f"\n❌ Error en usuarios_db: {str(e)}")
        return False


def test_evaluaciones_db():
    """Prueba la conexión a la BD de Evaluaciones."""
    print("\n" + "="*60)
    print("Probando Base de Datos: EVALUACIONES")
    print("="*60)
    
    try:
        print(f"Host: {DatabaseConfig.EVALUACIONES_DB_HOST}")
        print(f"Base de datos: {DatabaseConfig.EVALUACIONES_DB_NAME}")
        print("\nInicializando conexión...")
        
        engine = init_evaluaciones_db(echo=False)
        print("✓ Engine creado")
        
        session = get_evaluaciones_session()
        print("✓ Sesión obtenida")
        
        # Ejecutar query simple
        result = session.execute("SELECT 1 as test")
        row = result.fetchone()
        print(f"✓ Query ejecutado: {row[0]}")
        
        session.close()
        print("✓ Sesión cerrada")
        
        print("\n✅ Conexión a evaluaciones_db: EXITOSA")
        return True
        
    except Exception as e:
        print(f"\n❌ Error en evaluaciones_db: {str(e)}")
        return False


def main():
    """Función principal."""
    print("\n")
    print("╔" + "═"*58 + "╗")
    print("║" + " "*12 + "PRUEBA DE CONEXIONES A RDS MYSQL" + " "*14 + "║")
    print("╚" + "═"*58 + "╝")
    print()
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    resultados = {
        'contenido': False,
        'usuarios': False,
        'evaluaciones': False
    }
    
    # Probar cada base de datos
    resultados['contenido'] = test_contenido_db()
    resultados['usuarios'] = test_usuarios_db()
    resultados['evaluaciones'] = test_evaluaciones_db()
    
    # Resumen final
    print("\n" + "="*60)
    print("RESUMEN DE PRUEBAS")
    print("="*60)
    
    total = len(resultados)
    exitosas = sum(resultados.values())
    
    print(f"\nBases de datos probadas: {total}")
    print(f"Conexiones exitosas: {exitosas}")
    print(f"Conexiones fallidas: {total - exitosas}")
    print()
    
    for bd, resultado in resultados.items():
        estado = "✅ EXITOSA" if resultado else "❌ FALLIDA"
        print(f"  {bd}_db: {estado}")
    
    print("\n" + "="*60)
    
    if exitosas == total:
        print("✅ TODAS LAS CONEXIONES FUNCIONAN CORRECTAMENTE")
        print("="*60)
        print("\nPuedes proceder a crear las tablas ejecutando:")
        print("  python crear_tablas.py")
        return 0
    else:
        print("⚠️ ALGUNAS CONEXIONES FALLARON")
        print("="*60)
        print("\nVerifica:")
        print("  1. Que las bases de datos existan en RDS")
        print("  2. Que las credenciales en .env sean correctas")
        print("  3. Que los security groups permitan conexión")
        print("  4. Que el servidor MySQL esté en ejecución")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

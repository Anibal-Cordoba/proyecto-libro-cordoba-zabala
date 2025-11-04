"""
Script para crear todas las tablas en las 3 bases de datos
===========================================================
Ejecuta este script para crear el esquema inicial.
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.config import (
    init_contenido_db,
    init_usuarios_db,
    init_evaluaciones_db,
    BaseContenido,
    BaseUsuarios,
    BaseEvaluaciones
)

# Importar modelos para registrarlos
from db.contenido import models as contenido_models
from db.usuarios import models as usuarios_models
from db.evaluaciones import models as evaluaciones_models


def create_contenido_tables():
    """Crea las tablas de la BD de Contenido."""
    print("=" * 60)
    print("Creando tablas en Base de Datos: CONTENIDO")
    print("=" * 60)
    
    engine = init_contenido_db(echo=True)
    BaseContenido.metadata.create_all(engine)
    
    print("\n✓ Tablas creadas:")
    print("  - capitulos")
    print("  - contenidos")
    print("  - union_capitulo_contenido")
    print()


def create_usuarios_tables():
    """Crea las tablas de la BD de Usuarios."""
    print("=" * 60)
    print("Creando tablas en Base de Datos: USUARIOS")
    print("=" * 60)
    
    engine = init_usuarios_db(echo=True)
    BaseUsuarios.metadata.create_all(engine)
    
    print("\n✓ Tablas creadas:")
    print("  - usuarios")
    print("  - estudiantes")
    print("  - docentes")
    print("  - roles")
    print("  - permisos")
    print("  - usuario_rol (asociación)")
    print("  - rol_permiso (asociación)")
    print()


def create_evaluaciones_tables():
    """Crea las tablas de la BD de Evaluaciones."""
    print("=" * 60)
    print("Creando tablas en Base de Datos: EVALUACIONES")
    print("=" * 60)
    
    engine = init_evaluaciones_db(echo=True)
    BaseEvaluaciones.metadata.create_all(engine)
    
    print("\n✓ Tablas creadas:")
    print("  - evaluaciones")
    print("  - preguntas")
    print("  - opciones")
    print("  - intentos")
    print("  - respuestas")
    print()


def main():
    """Función principal para crear todas las tablas."""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "CREACIÓN DE ESQUEMAS DE BASE DE DATOS" + " " * 10 + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    print("Este script creará las tablas en las 3 bases de datos:")
    print("  1. contenido_db")
    print("  2. usuarios_db")
    print("  3. evaluaciones_db")
    print()
    
    respuesta = input("¿Deseas continuar? (s/n): ").lower()
    
    if respuesta != 's':
        print("\nOperación cancelada.")
        return
    
    print()
    
    try:
        # Crear tablas en cada BD
        create_contenido_tables()
        create_usuarios_tables()
        create_evaluaciones_tables()
        
        print("=" * 60)
        print("✓ PROCESO COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        print()
        print("Las 3 bases de datos han sido inicializadas correctamente.")
        print()
        
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ ERROR")
        print("=" * 60)
        print(f"Error al crear las tablas: {str(e)}")
        print()
        print("Verifica:")
        print("  1. Que las bases de datos existan en MySQL")
        print("  2. Que las credenciales en variables de entorno sean correctas")
        print("  3. Que el servidor MySQL esté en ejecución")
        print()


if __name__ == "__main__":
    main()

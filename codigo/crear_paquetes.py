#!/usr/bin/env python3
"""
Script para crear la estructura de paquetes independientes
===========================================================
"""

import os
import shutil
from pathlib import Path

# Directorio base
BASE_DIR = Path(__file__).parent
PAQUETES_DIR = BASE_DIR / "paquetes"
MODELOS_DIR = BASE_DIR / "modelos"
REPOSITORIOS_DIR = BASE_DIR / "repositorios"
GESTORES_DIR = BASE_DIR / "gestores"

# Definición de paquetes
PAQUETES = {
    # Modelos
    "modelo_contenido": {
        "files": ["contenido.py"],
        "name": "libro-modelo-contenido",
        "description": "Modelo base abstracto de Contenido",
        "deps": []
    },
    "modelo_texto": {
        "files": ["texto.py", "contenido.py"],  # Necesita el padre
        "name": "libro-modelo-texto",
        "description": "Modelo de contenido tipo Texto",
        "deps": ["libro-modelo-contenido"]
    },
    "modelo_imagen": {
        "files": ["imagen.py", "contenido.py"],
        "name": "libro-modelo-imagen",
        "description": "Modelo de contenido tipo Imagen",
        "deps": ["libro-modelo-contenido"]
    },
    "modelo_video": {
        "files": ["video.py", "contenido.py"],
        "name": "libro-modelo-video",
        "description": "Modelo de contenido tipo Video",
        "deps": ["libro-modelo-contenido"]
    },
    "modelo_objeto3d": {
        "files": ["objeto3d.py", "contenido.py"],
        "name": "libro-modelo-objeto3d",
        "description": "Modelo de contenido tipo Objeto3D",
        "deps": ["libro-modelo-contenido"]
    },
    "modelo_union": {
        "files": ["union_capitulo_contenido.py"],
        "name": "libro-modelo-union",
        "description": "Modelo de unión Capítulo-Contenido",
        "deps": []
    },
    
    # Repositorios
    "repositorio_contenido": {
        "files": ["repositorio_contenido.py"],
        "name": "libro-repositorio-contenido",
        "description": "Repositorio para gestionar contenidos",
        "deps": ["libro-modelo-contenido", "sqlalchemy>=2.0.0", "pymysql>=1.1.0"]
    },
    "repositorio_capitulo": {
        "files": ["repositorio_capitulo.py"],
        "name": "libro-repositorio-capitulo",
        "description": "Repositorio para gestionar capítulos",
        "deps": ["libro-modelo-capitulo", "sqlalchemy>=2.0.0", "pymysql>=1.1.0"]
    },
    "repositorio_union": {
        "files": ["repositorio_union_capitulo_contenido.py"],
        "name": "libro-repositorio-union",
        "description": "Repositorio para gestionar uniones capítulo-contenido",
        "deps": ["libro-modelo-union", "sqlalchemy>=2.0.0", "pymysql>=1.1.0"]
    },
    
    # Gestores
    "gestor_contenido": {
        "files": ["gestor_contenido.py"],
        "name": "libro-gestor-contenido",
        "description": "Gestor de lógica de negocio para contenidos",
        "deps": ["libro-modelo-contenido", "libro-repositorio-contenido"]
    },
    "gestor_capitulo": {
        "files": ["gestor_capitulo.py"],
        "name": "libro-gestor-capitulo",
        "description": "Gestor de lógica de negocio para capítulos",
        "deps": ["libro-modelo-capitulo", "libro-repositorio-capitulo", "libro-repositorio-union"]
    },
}


def create_init_file(paquete_dir, main_file):
    """Crea el archivo __init__.py para el paquete."""
    main_module = main_file.replace(".py", "")
    class_name = "".join(word.capitalize() for word in main_module.split("_"))
    
    # Casos especiales
    if "repositorio" in main_module:
        class_name = "Repositorio" + class_name.replace("Repositorio", "")
    elif "gestor" in main_module:
        class_name = "Gestor" + class_name.replace("Gestor", "")
    
    content = f'''"""
Paquete {paquete_dir.name}
{"=" * len(paquete_dir.name)}
"""

from .{main_module} import {class_name}

__all__ = ['{class_name}']
__version__ = '0.1.0'
'''
    
    with open(paquete_dir / "__init__.py", "w") as f:
        f.write(content)


def create_setup_file(paquete_dir, pkg_info):
    """Crea el archivo setup.py para el paquete."""
    deps_str = ",\n        ".join(f"'{dep}'" for dep in pkg_info["deps"])
    if deps_str:
        deps_str = f"\n        {deps_str}\n    "
    
    content = f'''"""
Setup para el paquete {paquete_dir.name}
{"=" * (len(paquete_dir.name) + 22)}
"""

from setuptools import setup, find_packages

setup(
    name='{pkg_info["name"]}',
    version='0.1.0',
    description='{pkg_info["description"]}',
    author='Anibal Cordoba & Zabala',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[{deps_str}],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
'''
    
    with open(paquete_dir / "setup.py", "w") as f:
        f.write(content)


def create_readme_file(paquete_dir, pkg_info):
    """Crea el archivo README.md para el paquete."""
    content = f'''# {pkg_info["name"]}

{pkg_info["description"]}

## Instalación

```bash
pip install -e .
```

## Uso

```python
from {paquete_dir.name} import *
```

## Dependencias

{chr(10).join(f"- {dep}" for dep in pkg_info["deps"]) if pkg_info["deps"] else "Sin dependencias externas"}

## Versión

0.1.0
'''
    
    with open(paquete_dir / "README.md", "w") as f:
        f.write(content)


def main():
    """Función principal."""
    print("Creando paquetes independientes...")
    print("=" * 60)
    
    for paquete_nombre, pkg_info in PAQUETES.items():
        paquete_dir = PAQUETES_DIR / paquete_nombre
        print(f"\n📦 Creando paquete: {paquete_nombre}")
        
        # Ya existe el directorio, copiar archivos
        main_file = pkg_info["files"][0]
        
        # Determinar origen
        if paquete_nombre.startswith("modelo_"):
            source_dir = MODELOS_DIR
        elif paquete_nombre.startswith("repositorio_"):
            source_dir = REPOSITORIOS_DIR
        elif paquete_nombre.startswith("gestor_"):
            source_dir = GESTORES_DIR
        else:
            continue
        
        # Copiar archivos
        for file_name in pkg_info["files"]:
            source_file = source_dir / file_name
            dest_file = paquete_dir / file_name
            
            if source_file.exists():
                shutil.copy2(source_file, dest_file)
                print(f"  ✓ Copiado: {file_name}")
            else:
                print(f"  ⚠ No encontrado: {file_name}")
        
        # Crear archivos del paquete
        create_init_file(paquete_dir, main_file)
        print(f"  ✓ Creado: __init__.py")
        
        create_setup_file(paquete_dir, pkg_info)
        print(f"  ✓ Creado: setup.py")
        
        create_readme_file(paquete_dir, pkg_info)
        print(f"  ✓ Creado: README.md")
    
    print("\n" + "=" * 60)
    print("✅ Todos los paquetes creados exitosamente")
    print("\nPara instalar todos los paquetes, ejecuta:")
    print("  bash instalar_paquetes.sh")


if __name__ == "__main__":
    main()

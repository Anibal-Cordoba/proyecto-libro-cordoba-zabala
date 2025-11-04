"""
Setup para el paquete de Repositorios
======================================
"""

from setuptools import setup, find_packages

setup(
    name='libro-interactivo-repositorios',
    version='0.1.0',
    description='Paquete de repositorios (acceso a datos) para el sistema de libros interactivos',
    author='Tu Nombre',
    author_email='tu@email.com',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'libro-interactivo-modelos',  # Depende del paquete de modelos
        # 'sqlalchemy>=2.0.0',  # Descomentar cuando se implemente la persistencia
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)

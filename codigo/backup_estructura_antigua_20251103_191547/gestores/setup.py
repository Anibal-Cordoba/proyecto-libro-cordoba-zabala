"""
Setup para el paquete de Gestores
==================================
"""

from setuptools import setup, find_packages

setup(
    name='libro-interactivo-gestores',
    version='0.1.0',
    description='Paquete de gestores (lógica de negocio) para el sistema de libros interactivos',
    author='Tu Nombre',
    author_email='tu@email.com',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'libro-interactivo-modelos',       # Depende del paquete de modelos
        'libro-interactivo-repositorios',  # Depende del paquete de repositorios
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

"""
Setup para el paquete de Modelos
=================================
"""

from setuptools import setup, find_packages

setup(
    name='libro-interactivo-modelos',
    version='0.1.0',
    description='Paquete de modelos/entidades para el sistema de libros interactivos',
    author='Tu Nombre',
    author_email='tu@email.com',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        # No tiene dependencias externas, solo módulos estándar de Python
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

"""
Setup para el paquete gestor_contenido
======================================
"""

from setuptools import setup, find_packages

setup(
    name='libro-gestor-contenido',
    version='0.1.0',
    description='Gestor de lógica de negocio para contenidos',
    author='Anibal Cordoba & Zabala',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'libro-modelo-contenido',
        'libro-repositorio-contenido'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)

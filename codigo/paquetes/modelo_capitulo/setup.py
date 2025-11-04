"""
Setup para el paquete modelo_capitulo
======================================
"""

from setuptools import setup, find_packages

setup(
    name='libro-modelo-capitulo',
    version='0.1.0',
    description='Modelo de dominio para Capítulo del libro virtual',
    author='Anibal Cordoba & Zabala',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        # Sin dependencias externas
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

"""
Setup para el paquete repositorio_union
=======================================
"""

from setuptools import setup, find_packages

setup(
    name='libro-repositorio-union',
    version='0.1.0',
    description='Repositorio para gestionar uniones capítulo-contenido',
    author='Anibal Cordoba & Zabala',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'libro-modelo-union',
        'sqlalchemy>=2.0.0',
        'pymysql>=1.1.0'
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

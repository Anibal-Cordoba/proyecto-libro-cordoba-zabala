"""
Setup para el paquete modelo_imagen
===================================
"""

from setuptools import setup, find_packages

setup(
    name='libro-modelo-imagen',
    version='0.1.0',
    description='Modelo de contenido tipo Imagen',
    author='Anibal Cordoba & Zabala',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'libro-modelo-contenido'
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

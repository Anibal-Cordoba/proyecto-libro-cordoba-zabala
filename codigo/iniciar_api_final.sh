#!/bin/bash

# Script para iniciar la API REST
# ================================

echo "🚀 Iniciando API REST del Libro Interactivo..."
echo ""

# No activar entorno virtual, usar python directamente
# source ../.venv/bin/activate

# Configurar PYTHONPATH
export PYTHONPATH=/home/anibal/Documentos/proyecto-libro-cordoba-zabala/codigo

# Iniciar servidor
echo "📡 Servidor disponible en: http://localhost:8000"
echo "📚 Documentación API en: http://localhost:8000/docs"
echo "🔍 Health check en: http://localhost:8000/health"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""

/home/anibal/Documentos/proyecto-libro-cordoba-zabala/.venv/bin/python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

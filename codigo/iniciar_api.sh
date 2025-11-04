#!/bin/bash
###############################################################################
# Script para iniciar la API FastAPI
###############################################################################

set -e

echo "=========================================="
echo "  Iniciando API del Libro Interactivo"
echo "=========================================="
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -d "api" ]; then
    echo "❌ Error: Este script debe ejecutarse desde la carpeta 'codigo/'"
    exit 1
fi

# Verificar que los paquetes estén instalados
echo "Verificando paquetes..."
if ! pip list | grep -q "libro-modelo-capitulo"; then
    echo "❌ Los paquetes no están instalados. Ejecuta primero:"
    echo "   bash instalar_paquetes.sh"
    exit 1
fi
echo "✓ Paquetes verificados"
echo ""

# Instalar dependencias de la API si es necesario
echo "Verificando dependencias de la API..."
pip install -q fastapi uvicorn jinja2 python-dotenv pydantic
echo "✓ Dependencias instaladas"
echo ""

# Iniciar el servidor
echo "=========================================="
echo "  Servidor iniciando en:"
echo "  http://localhost:8000"
echo "=========================================="
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""

cd api
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

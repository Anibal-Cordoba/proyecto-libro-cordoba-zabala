#!/bin/bash
set -e

echo "================================================"
echo "📦 Instalando paquetes del Libro Interactivo"
echo "================================================"
echo ""

if [ ! -d "paquetes" ]; then
    echo "❌ Error: No se encontró el directorio 'paquetes'"
    exit 1
fi

INSTALADOS=0
ERRORES=0

for paquete_dir in paquetes/*/; do
    if [ -f "${paquete_dir}setup.py" ]; then
        paquete_nombre=$(basename "$paquete_dir")
        echo "📦 Instalando: $paquete_nombre"
        
        if pip install -e "$paquete_dir" --quiet 2>&1; then
            echo "   ✅ $paquete_nombre instalado"
            ((INSTALADOS++))
        else
            echo "   ❌ Error al instalar $paquete_nombre"
            ((ERRORES++))
        fi
        echo ""
    fi
done

echo "================================================"
echo "📊 Resumen: $INSTALADOS instalados, $ERRORES errores"
echo "================================================"

if [ $ERRORES -eq 0 ]; then
    echo "🎉 ¡Todos los paquetes instalados!"
    pip list | grep "libro-" || echo "No se encontraron paquetes libro-*"
fi

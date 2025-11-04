#!/bin/bash
# Script para ejecutar tests con coverage
# =========================================

set -e

echo "================================================"
echo "  EJECUTANDO TESTS CON COVERAGE"
echo "  Caso de Prueba: CP01_01"
echo "================================================"
echo ""

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar que estamos en el directorio correcto
if [ ! -f "pytest.ini" ]; then
    echo -e "${RED}❌ Error: Ejecuta este script desde el directorio codigo/${NC}"
    exit 1
fi

# Instalar dependencias de testing si no están instaladas
echo -e "${BLUE}📦 Verificando dependencias de testing...${NC}"
pip install -q pytest pytest-cov pytest-html pytest-xdist 2>/dev/null || {
    echo -e "${YELLOW}⚠️  Instalando dependencias de testing...${NC}"
    pip install pytest pytest-cov pytest-html pytest-xdist
}

echo -e "${GREEN}✅ Dependencias verificadas${NC}"
echo ""

# Crear directorio para reportes si no existe
mkdir -p reports

# Opción 1: Ejecutar solo tests de CP01_01
if [ "$1" == "cp01" ] || [ "$1" == "cp01_01" ]; then
    echo -e "${BLUE}🧪 Ejecutando tests de CP01_01...${NC}"
    pytest tests/test_cp01_01_visualizar_capitulo.py \
        --cov=api \
        --cov=db \
        --cov-report=html \
        --cov-report=term-missing \
        --cov-report=json \
        --html=reports/cp01_01_report.html \
        --self-contained-html

# Opción 1b: Ejecutar solo tests de CP01_02
elif [ "$1" == "cp01_02" ]; then
    echo -e "${BLUE}🧪 Ejecutando tests de CP01_02...${NC}"
    pytest tests/test_cp01_02_capitulo_inexistente.py \
        --cov=api \
        --cov=db \
        --cov-report=html \
        --cov-report=term-missing \
        --cov-report=json \
        --html=reports/cp01_02_report.html \
        --self-contained-html

# Opción 1c: Ejecutar todos los CP01 (CP01_01 + CP01_02)
elif [ "$1" == "cp01_all" ]; then
    echo -e "${BLUE}🧪 Ejecutando todos los tests CP01...${NC}"
    pytest tests/test_cp01_01_visualizar_capitulo.py tests/test_cp01_02_capitulo_inexistente.py \
        --cov=api \
        --cov=db \
        --cov-report=html \
        --cov-report=term-missing \
        --cov-report=json \
        --html=reports/cp01_all_report.html \
        --self-contained-html

# Opción 1d: Ejecutar solo tests de CP02_01
elif [ "$1" == "cp02_01" ]; then
    echo -e "${BLUE}🧪 Ejecutando tests de CP02_01...${NC}"
    pytest tests/test_cp02_01_crear_capitulo.py \
        --cov=api \
        --cov=db \
        --cov-report=html \
        --cov-report=term-missing \
        --cov-report=json \
        --html=reports/cp02_01_report.html \
        --self-contained-html

# Opción 1e: Ejecutar solo tests de CP02_02
elif [ "$1" == "cp02_02" ]; then
    echo -e "${BLUE}🧪 Ejecutando tests de CP02_02...${NC}"
    pytest tests/test_cp02_02_actualizar_capitulo.py \
        --cov=api \
        --cov=db \
        --cov-report=html \
        --cov-report=term-missing \
        --cov-report=json \
        --html=reports/cp02_02_report.html \
        --self-contained-html

# Opción 1f: Ejecutar solo tests de CP02_03
elif [ "$1" == "cp02_03" ]; then
    echo -e "${BLUE}🧪 Ejecutando tests de CP02_03...${NC}"
    pytest tests/test_cp02_03_eliminar_capitulo.py \
        --cov=api \
        --cov=db \
        --cov-report=html \
        --cov-report=term-missing \
        --cov-report=json \
        --html=reports/cp02_03_report.html \
        --self-contained-html

# Opción 1g: Ejecutar solo tests de CP02_04
elif [ "$1" == "cp02_04" ]; then
    echo -e "${BLUE}🧪 Ejecutando tests de CP02_04...${NC}"
    pytest tests/test_cp02_04_listar_capitulos.py \
        --cov=api \
        --cov=db \
        --cov-report=html \
        --cov-report=term-missing \
        --cov-report=json \
        --html=reports/cp02_04_report.html \
        --self-contained-html

# Opción 1h: Ejecutar solo tests de CP02_05
elif [ "$1" == "cp02_05" ]; then
    echo -e "${BLUE}🧪 Ejecutando tests de CP02_05...${NC}"
    pytest tests/test_cp02_05_validaciones_estado.py \
        --cov=api \
        --cov=db \
        --cov-report=html \
        --cov-report=term-missing \
        --cov-report=json \
        --html=reports/cp02_05_report.html \
        --self-contained-html

# Opción 1i: Ejecutar todos los CP02
elif [ "$1" == "cp02_all" ]; then
    echo -e "${BLUE}🧪 Ejecutando todos los tests CP02...${NC}"
    pytest tests/test_cp02_01_crear_capitulo.py \
           tests/test_cp02_02_actualizar_capitulo.py \
           tests/test_cp02_03_eliminar_capitulo.py \
           tests/test_cp02_04_listar_capitulos.py \
           tests/test_cp02_05_validaciones_estado.py \
        --cov=api \
        --cov=db \
        --cov-report=html \
        --cov-report=term-missing \
        --cov-report=json \
        --html=reports/cp02_all_report.html \
        --self-contained-html

# Opción 2: Ejecutar todos los tests
elif [ "$1" == "all" ]; then
    echo -e "${BLUE}🧪 Ejecutando TODOS los tests...${NC}"
    pytest tests/ \
        --cov=api \
        --cov=db \
        --cov-report=html \
        --cov-report=term-missing \
        --cov-report=json \
        --html=reports/full_report.html \
        --self-contained-html

# Opción 3: Ejecutar tests específicos por marker
elif [ "$1" == "unit" ]; then
    echo -e "${BLUE}🧪 Ejecutando tests unitarios...${NC}"
    pytest tests/ -m unit \
        --cov=db.contenido.models \
        --cov-report=term-missing

elif [ "$1" == "integration" ]; then
    echo -e "${BLUE}🧪 Ejecutando tests de integración...${NC}"
    pytest tests/ -m integration \
        --cov=api \
        --cov-report=term-missing

# Opción 4: Ejecución rápida (sin coverage)
elif [ "$1" == "quick" ]; then
    echo -e "${BLUE}⚡ Ejecución rápida (sin coverage)...${NC}"
    pytest tests/ --tb=short

# Opción 5: Tests en paralelo
elif [ "$1" == "parallel" ]; then
    echo -e "${BLUE}🚀 Ejecutando tests en paralelo...${NC}"
    pytest tests/ -n auto \
        --cov=api \
        --cov=db \
        --cov-report=term-missing

# Opción por defecto: CP01_01
else
    echo -e "${BLUE}🧪 Ejecutando tests de CP01_01 (caso de uso principal)...${NC}"
    echo -e "${YELLOW}💡 Usa: ./ejecutar_tests.sh [cp01_01|cp01_02|cp01_all|cp02_01|cp02_02|cp02_03|cp02_04|cp02_05|cp02_all|all|unit|integration|quick|parallel]${NC}"
    echo ""
    
    pytest tests/test_cp01_01_visualizar_capitulo.py \
        --cov=api.routers.capitulos \
        --cov=db.contenido.models \
        --cov-report=html \
        --cov-report=term-missing \
        --cov-report=json \
        --html=reports/cp01_01_report.html \
        --self-contained-html
fi

# Verificar resultado
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ TESTS COMPLETADOS EXITOSAMENTE${NC}"
    echo ""
    echo -e "${BLUE}📊 Reportes generados:${NC}"
    echo "   - HTML Coverage: htmlcov/index.html"
    echo "   - HTML Report: reports/"
    echo "   - JSON Coverage: coverage.json"
    echo ""
    echo -e "${YELLOW}💡 Para ver el reporte HTML:${NC}"
    echo "   xdg-open htmlcov/index.html"
    echo ""
else
    echo ""
    echo -e "${RED}❌ ALGUNOS TESTS FALLARON${NC}"
    echo -e "${YELLOW}Revisa el output arriba para más detalles${NC}"
    exit 1
fi

# Mostrar resumen de coverage si existe
if [ -f "coverage.json" ]; then
    echo -e "${BLUE}📈 Resumen de Coverage:${NC}"
    python3 << EOF
import json
with open('coverage.json', 'r') as f:
    data = json.load(f)
    total = data['totals']['percent_covered']
    print(f"   Cobertura Total: {total:.2f}%")
    
    if total >= 80:
        print("   ✅ Cobertura EXCELENTE (>= 80%)")
    elif total >= 60:
        print("   ⚠️  Cobertura BUENA (>= 60%)")
    else:
        print("   ❌ Cobertura BAJA (< 60%) - Se recomienda más tests")
EOF
fi

echo ""
echo "================================================"

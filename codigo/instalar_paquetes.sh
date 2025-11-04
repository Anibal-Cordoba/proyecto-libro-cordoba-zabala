#!/bin/bash
###############################################################################
# Script de instalación de paquetes del proyecto Libro Interactivo
###############################################################################

set -e  # Salir si hay error

echo "=========================================="
echo "  Instalación de paquetes del proyecto"
echo "=========================================="
echo ""

# Directorio base
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PAQUETES_DIR="$SCRIPT_DIR/paquetes"

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}📦 Instalando paquetes en orden de dependencias...${NC}"
echo ""

# Fase 1: Modelos base (sin dependencias)
echo "Fase 1: Modelos base"
echo "-------------------"
cd "$PAQUETES_DIR/modelo_capitulo" && pip install -e . && echo -e "${GREEN}✓ libro-modelo-capitulo instalado${NC}"
cd "$PAQUETES_DIR/modelo_contenido" && pip install -e . && echo -e "${GREEN}✓ libro-modelo-contenido instalado${NC}"
cd "$PAQUETES_DIR/modelo_union" && pip install -e . && echo -e "${GREEN}✓ libro-modelo-union instalado${NC}"
echo ""

# Fase 2: Modelos derivados (dependen de modelo_contenido)
echo "Fase 2: Modelos derivados"
echo "-------------------------"
cd "$PAQUETES_DIR/modelo_texto" && pip install -e . && echo -e "${GREEN}✓ libro-modelo-texto instalado${NC}"
cd "$PAQUETES_DIR/modelo_imagen" && pip install -e . && echo -e "${GREEN}✓ libro-modelo-imagen instalado${NC}"
cd "$PAQUETES_DIR/modelo_video" && pip install -e . && echo -e "${GREEN}✓ libro-modelo-video instalado${NC}"
cd "$PAQUETES_DIR/modelo_objeto3d" && pip install -e . && echo -e "${GREEN}✓ libro-modelo-objeto3d instalado${NC}"
echo ""

# Fase 3: Repositorios (dependen de modelos)
echo "Fase 3: Repositorios"
echo "--------------------"
cd "$PAQUETES_DIR/repositorio_capitulo" && pip install -e . && echo -e "${GREEN}✓ libro-repositorio-capitulo instalado${NC}"
cd "$PAQUETES_DIR/repositorio_contenido" && pip install -e . && echo -e "${GREEN}✓ libro-repositorio-contenido instalado${NC}"
cd "$PAQUETES_DIR/repositorio_union" && pip install -e . && echo -e "${GREEN}✓ libro-repositorio-union instalado${NC}"
echo ""

# Fase 4: Gestores (dependen de repositorios y modelos)
echo "Fase 4: Gestores"
echo "----------------"
cd "$PAQUETES_DIR/gestor_contenido" && pip install -e . && echo -e "${GREEN}✓ libro-gestor-contenido instalado${NC}"
cd "$PAQUETES_DIR/gestor_capitulo" && pip install -e . && echo -e "${GREEN}✓ libro-gestor-capitulo instalado${NC}"
echo ""

echo "=========================================="
echo -e "${GREEN}✅ Todos los paquetes instalados exitosamente${NC}"
echo "=========================================="
echo ""
echo "Paquetes disponibles:"
echo "  - libro-modelo-capitulo"
echo "  - libro-modelo-contenido"
echo "  - libro-modelo-texto"
echo "  - libro-modelo-imagen"
echo "  - libro-modelo-video"
echo "  - libro-modelo-objeto3d"
echo "  - libro-modelo-union"
echo "  - libro-repositorio-capitulo"
echo "  - libro-repositorio-contenido"
echo "  - libro-repositorio-union"
echo "  - libro-gestor-contenido"
echo "  - libro-gestor-capitulo"
echo ""
echo "Para verificar la instalación:"
echo "  pip list | grep libro"

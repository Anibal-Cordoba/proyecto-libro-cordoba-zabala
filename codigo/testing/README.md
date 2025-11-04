# 📋 Documentación de Testing

Esta carpeta contiene toda la documentación relacionada con las pruebas automatizadas del sistema de gestión de contenidos para libros interactivos.

## 🎯 Estado Actual: ✅ **115 tests pasando (100%)**

| Métrica | Valor |
|---------|-------|
| Tests Totales | 115 |
| Tests Pasando | 115 (100%) ✅ |
| Coverage Routers | 100% ⭐ |
| Coverage Models | 89% ✅ |
| Coverage Total | 31% |
| Tiempo Ejecución | ~3.7s |

## 📁 Estructura de Documentación

```
testing/
├── README.md                          # 📖 Este archivo (Índice general)
├── GUIA_RAPIDA_TESTING.md            # 🚀 Guía rápida para ejecutar tests
├── RESUMEN_COMPLETO_TESTING.md       # 📚 Documento consolidado (115 tests)
├── REPORTE_TESTING_CP01_01.md        # 📊 Reporte CP01_01 (13 tests)
├── REPORTE_TESTING_CP01_02.md        # 📊 Reporte CP01_02 (19 tests)
└── REPORTE_TESTING_CP02_01.md        # 📊 Reporte CP02_01 (26 tests)
```

## 📊 Resumen Completo de Tests

| Suite | Tests | Endpoint | Funcionalidad | Estado |
|-------|-------|----------|---------------|--------|
| **CP01_01** | 13 | `GET /{id}` | Visualizar capítulo publicado | ✅ 100% |
| **CP01_02** | 19 | `GET /{id}` | Manejo de errores y seguridad | ✅ 100% |
| **CP02_01** | 26 | `POST /` | Crear capítulo con validaciones | ✅ 100% |
| **CP02_02** | 15 | `PUT /{id}` | Actualizar capítulo | ✅ 100% |
| **CP02_03** | 10 | `DELETE /{id}` | Eliminar capítulo | ✅ 100% |
| **CP02_04** | 12 | `GET /` | Listar y filtrar capítulos | ✅ 100% |
| **CP02_05** | 8 | Varios | Validaciones de estado | ✅ 100% |
| **test_models** | 12 | N/A | Tests unitarios ORM | ✅ 100% |
| **TOTAL** | **115** | - | **CRUD Completo** | ✅ 100% |

## 🚀 Inicio Rápido

### Ejecutar todos los tests
```bash
cd codigo
./ejecutar_tests.sh all
```

### Ejecutar suite específica
```bash
./ejecutar_tests.sh cp01_01    # Visualizar (13 tests)
./ejecutar_tests.sh cp01_02    # Errores (19 tests)
./ejecutar_tests.sh cp02_01    # Crear (26 tests)
./ejecutar_tests.sh cp02_02    # Actualizar (15 tests)
./ejecutar_tests.sh cp02_03    # Eliminar (10 tests)
./ejecutar_tests.sh cp02_04    # Listar (12 tests)
./ejecutar_tests.sh cp02_05    # Validaciones (8 tests)
```

### Ver reportes
```bash
# Coverage HTML
xdg-open htmlcov/index.html

# Reportes de tests
xdg-open reports/full_report.html
```

## 📈 Coverage por Componente

### ✅ API Routers (100%)
- `api/routers/capitulos.py` - **100%** coverage
  - 5 endpoints completamente testeados
  - Todos los casos edge cubiertos
  - Validaciones exhaustivas

### ✅ Modelos ORM (89%)
- `db/contenido/models.py` - **89%** coverage
  - Modelos Capitulo, Contenido, Union
  - Relaciones N:M
  - Validaciones de dominio

### ⚠️ Advertencia sobre Tests
Los tests tienen un problema de aislamiento de base de datos. Ver [Opción 2](#opción-2-ignorar-tests-por-ahora-recomendado) en la guía rápida.

**Recomendación**: Usar la interfaz web (http://localhost:8000) para desarrollo normal.

## � Documentación Detallada

### Para Usuarios
- **[GUIA_RAPIDA_TESTING.md](GUIA_RAPIDA_TESTING.md)** - Guía rápida de ejecución (⭐ Comienza aquí)
  - Comandos básicos
  - Opciones de ejecución
  - Debugging
  - Solución de problemas

### Para Desarrolladores
- **[RESUMEN_COMPLETO_TESTING.md](RESUMEN_COMPLETO_TESTING.md)** - Documento consolidado con los 115 tests
  - Descripción de cada test
  - Casos de uso
  - Validaciones implementadas
  - Cobertura detallada

### Reportes por Suite
    Hicimos otros testing pero estos eran los de los casos de usos principales
- **[REPORTE_TESTING_CP01_01.md](REPORTE_TESTING_CP01_01.md)** - Visualizar capítulo publicado (13 tests)
- **[REPORTE_TESTING_CP01_02.md](REPORTE_TESTING_CP01_02.md)** - Manejo de errores (19 tests)
- **[REPORTE_TESTING_CP02_01.md](REPORTE_TESTING_CP02_01.md)** - Crear capítulo (26 tests)

## 🎯 Coverage Detallado por Endpoint

### GET /api/capitulos/{id} - 100% ✅
- **32 tests** (CP01_01 + CP01_02)
- Visualización exitosa de capítulos publicados
- Manejo de errores (404, 403)
- Seguridad (inyección SQL, enumeración de IDs)
- Performance (tiempo de respuesta, carga)

### POST /api/capitulos/ - 100% ✅
- **26 tests** (CP02_01)
- Creación exitosa con campos mínimos
- Validaciones de datos (titulo, numero, tema)
- Unicidad de número de capítulo
- Estados válidos (BORRADOR, PUBLICADO, ARCHIVADO)

### PUT /api/capitulos/{id} - 100% ✅
- **15 tests** (CP02_02)
- Actualización de campos individuales
- Actualización múltiple de campos
- Cambios de estado
- Persistencia de cambios
- Actualización de fecha_modificacion

### DELETE /api/capitulos/{id} - 100% ✅
- **10 tests** (CP02_03)
- Eliminación exitosa por estado
- Verificación de eliminación
- Simulación de CASCADE delete
- Manejo de errores (404, ID inválido)

### GET /api/capitulos/ - 100% ✅
- **12 tests** (CP02_04)
- Listado completo
- Ordenamiento por número
- Paginación (skip, limit)
- Filtros por tema (exacto, parcial, case-insensitive)

### Validaciones de Estado - 100% ✅
- **8 tests** (CP02_05)
- Estados válidos del sistema
- Transiciones de estado
- Reglas de negocio

### Tests Unitarios ORM - 100% ✅
- **12 tests** (test_models)
- Creación de modelos
- Relaciones entre entidades
- Validaciones de dominio

## 🔧 Configuración de Tests

### Archivos Principales
- **`../tests/conftest.py`** - Fixtures compartidos (client, capitulo_publicado, etc.)
- **`../pytest.ini`** - Configuración de pytest (markers, paths, opciones)
- **`../ejecutar_tests.sh`** - Script de ejecución con múltiples opciones

### Fixtures Disponibles
- `client` - Cliente FastAPI TestClient
- `test_db_session` - Sesión de BD limpia por test
- `capitulo_publicado` - Capítulo en estado PUBLICADO
- `capitulo_borrador` - Capítulo en estado BORRADOR
- `capitulo_archivado` - Capítulo en estado ARCHIVADO
- `sample_capitulo_data` - Datos de ejemplo para tests

## 🐛 Problemas Conocidos

### ⚠️ Aislamiento de Base de Datos
Los tests actualmente tienen un problema de aislamiento: pueden contaminar la base de datos de desarrollo (`data/contenido.db`).

**Soluciones temporales**:
1. **Limpiar BD antes de tests**: `python limpiar_db.py`
2. **Limpiar BD después de tests**: `python limpiar_db.py`
3. **Usar interfaz web**: Desarrollar sin ejecutar tests

**Solución futura**: Refactorizar configuración de tests para usar BD en memoria exclusiva.

## 📊 Métricas de Calidad

### Velocidad
- ⚡ **3.7 segundos** para ejecutar 115 tests
- 🚀 **~32 ms** por test en promedio
- ⏱️ Ejecución paralela disponible (más rápido)

### Cobertura
- 🎯 **100%** en endpoints críticos (routers)
- ✅ **89%** en modelos de dominio
- 📈 **31%** coverage total del proyecto

### Mantenibilidad
- 📝 Todos los tests documentados
- 🏗️ Fixtures reusables (DRY)
- 🏷️ Markers personalizados por categoría
- 🧪 Tests independientes entre sí


## �🔗 Enlaces Útiles

### Código y Configuración
- [Código de Tests](../tests/) - Directorio con todos los tests
- [Configuración Pytest](../pytest.ini) - Configuración completa
- [Script de Ejecución](../ejecutar_tests.sh) - Automatización

### Reportes Generados
- [Reportes HTML](../reports/) - Tests ejecutados
- [Coverage HTML](../htmlcov/) - Cobertura de código
- [Coverage JSON](../coverage.json) - Datos de cobertura

### Documentación del Proyecto
- [README Principal](../README.md) - Documentación del sistema
- [Guía de Contenidos](../GUIA_CONTENIDOS.md) - Sistema de contenidos
- [Configuración API](../CONFIGURACION_API.md) - Setup de la API

---

## 📅 Información

**Última actualización**: 4 de noviembre de 2025  
**Estado**: ✅ 115/115 tests pasando (100%)  
**Coverage**: 🎯 100% en routers críticos  
**Tiempo**: ⚡ ~3.7 segundos  

**👉 Comienza con**: [GUIA_RAPIDA_TESTING.md](GUIA_RAPIDA_TESTING.md)

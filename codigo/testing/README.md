# 📋 Documentación de Testing

Esta carpeta contiene toda la documentación relacionada con las pruebas del sistema.

## 📁 Estructura

```
testing/
├── README.md                          # Este archivo
├── GUIA_RAPIDA_TESTING.md            # Guía rápida para ejecutar tests
├── REPORTE_TESTING_CP01_01.md        # Reporte CP01_01 - Visualizar capítulo publicado
├── REPORTE_TESTING_CP01_02.md        # Reporte CP01_02 - Capítulo inexistente/no publicado
└── REPORTE_TESTING_CP02_01.md        # Reporte CP02_01 - Crear capítulo
```

## 📊 Resumen de Tests

| Caso de Prueba | Tests | Estado | Coverage Router | Reporte |
|----------------|-------|--------|----------------|---------|
| CP01_01 - Visualizar capítulo publicado | 13 | ✅ 100% | 54% | [Ver](REPORTE_TESTING_CP01_01.md) |
| CP01_02 - Capítulo inexistente/no publicado | 19 | ✅ 100% | 62% | [Ver](REPORTE_TESTING_CP01_02.md) |
| CP02_01 - Crear capítulo | 26 | ✅ 100% | 81% | [Ver](REPORTE_TESTING_CP02_01.md) |
| **TOTAL** | **58** | **✅ 100%** | **81%** | - |

## 🚀 Inicio Rápido

```bash
# Ejecutar todos los tests
./ejecutar_tests.sh all

# Ejecutar un caso específico
./ejecutar_tests.sh cp01_01
./ejecutar_tests.sh cp01_02
./ejecutar_tests.sh cp02_01

# Ver reportes de coverage
xdg-open htmlcov/index.html
```

Para más detalles, consulta la [Guía Rápida de Testing](GUIA_RAPIDA_TESTING.md).

## 📈 Evolución de Coverage

```
CP01_01: 54% → CP01_02: 62% → CP02_01: 81%
```

**Progreso**: +27 puntos porcentuales de coverage en routers.

## 🔗 Enlaces Útiles

- [Código de Tests](../tests/)
- [Configuración Pytest](../pytest.ini)
- [Script de Ejecución](../ejecutar_tests.sh)
- [Reportes HTML](../reports/)
- [Coverage HTML](../htmlcov/)

---

**Última actualización**: 4 de noviembre de 2025

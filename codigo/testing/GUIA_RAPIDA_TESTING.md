# 🧪 Guía Rápida de Testing
## Sistema Completo de Libro Interactivo

---

## 🎯 Resumen Ejecutivo

**Estado Actual**: ✅ **115 tests pasando (100%)**

| Métrica | Valor |
|---------|-------|
| Tests Totales | 115 |
| Tests Pasando | 115 (100%) |
| Coverage Routers | 100% ⭐ |
| Coverage Total | 31% |
| Tiempo Ejecución | ~3.7s |
| Suites | 8 |

---

## 🚀 Inicio Rápido (2 minutos)

### 1. Ejecutar TODOS los Tests
```bash
cd codigo
./ejecutar_tests.sh all
```

### 2. Ver Resultados
```bash
# Abrir reporte HTML de coverage
xdg-open htmlcov/index.html

# Abrir reporte completo de tests
xdg-open reports/full_report.html
```

## ✅ Resultado Esperado

```
🧪 Ejecutando TODOS los tests...
✅ 115/115 TESTS PASADOS
📊 Coverage: 100% en routers, 89% en modelos
⚡ Tiempo: ~3.7 segundos
```

## 📋 Suites de Tests Implementadas

| Suite | Tests | Endpoint | Funcionalidad |
|-------|-------|----------|---------------|
| **CP01_01** | 13 | `GET /{id}` | Visualizar capítulo publicado ✅ |
| **CP01_02** | 19 | `GET /{id}` | Manejo de errores y seguridad ✅ |
| **CP02_01** | 26 | `POST /` | Crear capítulo con validaciones ✅ |
| **CP02_02** | 15 | `PUT /{id}` | Actualizar capítulo ✅ |
| **CP02_03** | 10 | `DELETE /{id}` | Eliminar capítulo ✅ |
| **CP02_04** | 12 | `GET /` | Listar y filtrar capítulos ✅ |
| **CP02_05** | 8 | Varios | Validaciones de estado ✅ |
| **test_models** | 12 | N/A | Tests unitarios ORM ✅ |
| **TOTAL** | **115** | - | **CRUD Completo 100%** |

---

## 🎯 Coverage por Endpoint

### ✅ GET /api/capitulos/{id}
- **Tests**: 32 (CP01_01 + CP01_02)
- **Coverage**: 100%
- Visualización exitosa, errores, seguridad, performance

### ✅ POST /api/capitulos/
- **Tests**: 26 (CP02_01)
- **Coverage**: 100%
- Creación, validaciones, unicidad, estados

### ✅ PUT /api/capitulos/{id}
- **Tests**: 15 (CP02_02)
- **Coverage**: 100%
- Actualización de campos, estados, persistencia

### ✅ DELETE /api/capitulos/{id}
- **Tests**: 10 (CP02_03)
- **Coverage**: 100%
- Eliminación, verificación, CASCADE

### ✅ GET /api/capitulos/
- **Tests**: 12 (CP02_04)
- **Coverage**: 100%
- Listado, paginación, filtros por tema

## 📊 Comandos de Ejecución

### Por Caso de Prueba Individual
```bash
./ejecutar_tests.sh cp01_01    # Visualizar capítulo publicado (13 tests)
./ejecutar_tests.sh cp01_02    # Capítulo inexistente (19 tests)
./ejecutar_tests.sh cp02_01    # Crear capítulo (26 tests)
./ejecutar_tests.sh cp02_02    # Actualizar capítulo (15 tests)
./ejecutar_tests.sh cp02_03    # Eliminar capítulo (10 tests)
./ejecutar_tests.sh cp02_04    # Listar y filtrar (12 tests)
./ejecutar_tests.sh cp02_05    # Validaciones estado (8 tests)
```

### Por Grupo
```bash
./ejecutar_tests.sh cp01_all   # Todos los tests CP01 (lectura)
./ejecutar_tests.sh cp02_all   # Todos los tests CP02 (escritura)
./ejecutar_tests.sh all        # TODOS los tests (115)
```

### Por Tipo
```bash
./ejecutar_tests.sh unit        # Solo tests unitarios
./ejecutar_tests.sh integration # Solo tests de integración
./ejecutar_tests.sh quick       # Rápido sin coverage
./ejecutar_tests.sh parallel    # En paralelo (más rápido)
```

### Test Específico
```bash
# Ejecutar un test individual
pytest tests/test_cp02_01_crear_capitulo.py::TestCP02_01_CrearCapituloExitoso::test_crear_capitulo_campos_minimos -v

# Ejecutar una clase de tests
pytest tests/test_cp02_02_actualizar_capitulo.py::TestCP02_02_ActualizarExitoso -v
```

## 🔍 Debugging

### Ver output detallado
```bash
pytest tests/test_cp01_01_visualizar_capitulo.py -vvs
```

### Detener en primer fallo
```bash
pytest tests/ -x
```

### Modo debug interactivo
```bash
pytest tests/ --pdb
```

## 📈 Coverage

### Ver coverage en terminal
```bash
pytest tests/ --cov=api --cov=db --cov-report=term-missing
```

### Generar reporte HTML
```bash
pytest tests/ --cov=api --cov=db --cov-report=html
xdg-open htmlcov/index.html
```

## 🏗️ Estructura del Proyecto

```
codigo/
├── testing/                                    # Documentación
│   ├── README.md                              # Índice de tests
│   ├── GUIA_RAPIDA_TESTING.md                # Este archivo
│   ├── RESUMEN_COMPLETO_TESTING.md           # Documento consolidado
│   ├── REPORTE_TESTING_CP01_01.md            # Reporte detallado
│   ├── REPORTE_TESTING_CP01_02.md            # Reporte detallado
│   └── REPORTE_TESTING_CP02_01.md            # Reporte detallado
│
├── tests/                                      # Tests
│   ├── conftest.py                            # Fixtures compartidos
│   ├── test_cp01_01_visualizar_capitulo.py   # 13 tests GET /{id}
│   ├── test_cp01_02_capitulo_inexistente.py  # 19 tests errores
│   ├── test_cp02_01_crear_capitulo.py        # 26 tests POST /
│   ├── test_cp02_02_actualizar_capitulo.py   # 15 tests PUT /{id}
│   ├── test_cp02_03_eliminar_capitulo.py     # 10 tests DELETE /{id}
│   ├── test_cp02_04_listar_capitulos.py      # 12 tests GET /
│   ├── test_cp02_05_validaciones_estado.py   # 8 tests estados
│   └── test_models.py                         # 12 tests unitarios
│
├── ejecutar_tests.sh                          # Script de ejecución
├── pytest.ini                                 # Configuración pytest
├── htmlcov/                                   # Reportes coverage HTML
└── reports/                                   # Reportes tests HTML
```

## ⚙️ Configuración

### pytest.ini
- Configuración de pytest
- Paths de tests
- Markers personalizados
- Opciones de coverage

### Fixtures Principales
- `client`: Cliente de prueba FastAPI
- `capitulo_publicado`: Capítulo listo para visualizar
- `test_db_session`: BD limpia por test

## 🐛 Solución de Problemas

### Error: "No module named pytest"
```bash
pip install -r requirements.txt
```

### Tests fallan
```bash
# Ver detalles del fallo
pytest tests/ -vvs
```

### Coverage bajo
```bash
# Ver líneas no cubiertas
xdg-open htmlcov/index.html
```

## 📚 Documentación Completa

- **README de Tests**: `tests/README.md`
- **Reporte CP01_01**: `REPORTE_TESTING_CP01_01.md`
- **Configuración API**: `CONFIGURACION_API.md`

## ✨ Características del Sistema de Testing

- ✅ **115 tests exhaustivos** - Cobertura completa CRUD
- ✅ **Base de datos en memoria** - SQLite sin persistencia
- ✅ **No afecta BD producción** - Aislamiento total
- ✅ **Ejecución rápida** - 3.7s para 115 tests
- ✅ **Reportes HTML interactivos** - Visualización clara
- ✅ **Coverage 100% routers** - Endpoints críticos cubiertos
- ✅ **Fixtures reusables** - DRY en tests
- ✅ **Markers personalizados** - Ejecución selectiva
- ✅ **CI/CD ready** - Listo para integración continua

## 🎓 Tips y Mejores Prácticas

1. **Ejecuta tests antes de commit**: Garantiza calidad
2. **Usa coverage para identificar gaps**: HTML interactivo ayuda
3. **Lee los reportes detallados**: Entiende qué valida cada test
4. **Ejecuta suite específica durante desarrollo**: Más rápido
5. **Revisa warnings**: Pueden indicar problemas futuros
6. **Mantén tests independientes**: Cada test debe funcionar solo
7. **Usa fixtures**: Evita duplicación de código setup
8. **Documenta tests complejos**: Facilita mantenimiento

## ✅ Estado del Proyecto

### ✅ Completado (100%)
- [x] Tests CP01_01 - Visualizar capítulo publicado (13)
- [x] Tests CP01_02 - Capítulo inexistente/no publicado (19)
- [x] Tests CP02_01 - Crear capítulo (26)
- [x] Tests CP02_02 - Actualizar capítulo (15)
- [x] Tests CP02_03 - Eliminar capítulo (10)
- [x] Tests CP02_04 - Listar y filtrar (12)
- [x] Tests CP02_05 - Validaciones estado (8)
- [x] Tests unitarios modelos (12)
- [x] Coverage 100% en routers
- [x] Documentación completa
- [x] Scripts automatización

### 🔮 Futuras Mejoras (Opcional)
- [ ] Tests CP03_01 - Gestión de contenidos (20 tests)
- [ ] Tests CP03_02 - Relación capítulo-contenido (15 tests)
- [ ] Tests CP04_01 - Seguridad avanzada (10 tests)
- [ ] Tests CP05_01 - Performance y carga (10 tests)
- [ ] Tests E2E - Flujos completos (5 tests)

## 📚 Documentación Relacionada

- **[RESUMEN_COMPLETO_TESTING.md](RESUMEN_COMPLETO_TESTING.md)** - Documento consolidado con todos los 115 tests explicados
- **[REPORTE_TESTING_CP01_01.md](REPORTE_TESTING_CP01_01.md)** - Detalle de tests de visualización
- **[REPORTE_TESTING_CP01_02.md](REPORTE_TESTING_CP01_02.md)** - Detalle de tests de errores
- **[REPORTE_TESTING_CP02_01.md](REPORTE_TESTING_CP02_01.md)** - Detalle de tests de creación
- **[README.md](README.md)** - Índice de toda la documentación de testing

## 🔗 Enlaces Útiles

- **Configuración API**: `../CONFIGURACION_API.md`
- **README Principal**: `../README.md`
- **Tests**: `../tests/`
- **Coverage HTML**: `../htmlcov/index.html`
- **Reportes**: `../reports/`

---

**📅 Última actualización**: 4 de noviembre de 2025  
**📊 Estado**: ✅ 115/115 tests pasando (100%)  
**🎯 Coverage**: 100% en routers críticos

**¿Necesitas ayuda?** Consulta `RESUMEN_COMPLETO_TESTING.md` para información detallada de cada test.

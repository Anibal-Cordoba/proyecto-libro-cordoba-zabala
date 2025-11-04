# 🧪 Guía Rápida de Testing - CP01_01

## 🚀 Inicio Rápido (5 minutos)

### 1. Ejecutar Tests
```bash
cd codigo
./ejecutar_tests.sh cp01
```

### 2. Ver Resultados
```bash
# Abrir reporte HTML de coverage
xdg-open htmlcov/index.html

# Abrir reporte de tests
xdg-open reports/cp01_01_report.html
```

## ✅ Resultado Esperado

```
🧪 Ejecutando tests de CP01_01...
✅ 13/13 TESTS PASADOS
📊 Coverage: 88% en modelos, 54% en routers
⚡ Tiempo: < 1 segundo
```

## 📋 Tests Incluidos

1. ✅ **Visualización exitosa** - Test principal
2. ✅ **Estructura de respuesta** - Validación de datos
3. ✅ **Contenido correcto** - Verificación de valores
4. ✅ **Múltiples capítulos** - Escalabilidad
5. ✅ **Capítulo inexistente** - Error 404
6. ✅ **ID inválido** - Validación de entrada
7. ✅ **Capítulo borrador** - Estados diferentes
8. ✅ **Flujo completo** - Integración
9. ✅ **Con contenido** - Relaciones
10. ✅ **Tiempo de respuesta** - Performance
11. ✅ **Múltiples simultáneas** - Concurrencia
12. ✅ **Retrocompatibilidad** - Estabilidad
13. ✅ **Sin modificación** - Inmutabilidad

## 🎯 Caso de Prueba CP01_01

**Objetivo**: Visualizar un capítulo en estado PUBLICADO

**Endpoint**: `GET /api/capitulos/{id}`

**Entrada**: ID de capítulo publicado

**Salida Esperada**:
```json
{
  "id_capitulo": "uuid-del-capitulo",
  "titulo": "Título del Capítulo",
  "numero": 1,
  "tema": "Tema Principal",
  "introduccion": "Introducción del capítulo",
  "estado": "PUBLICADO",
  "fecha_creacion": "2025-11-03T...",
  "fecha_modificacion": "2025-11-03T..."
}
```

## 📊 Comandos Útiles

### Ejecutar todos los tests
```bash
./ejecutar_tests.sh all
```

### Ejecutar solo tests unitarios
```bash
./ejecutar_tests.sh unit
```

### Ejecución rápida (sin coverage)
```bash
./ejecutar_tests.sh quick
```

### Tests en paralelo (más rápido)
```bash
./ejecutar_tests.sh parallel
```

### Test específico
```bash
pytest tests/test_cp01_01_visualizar_capitulo.py::TestCP01_01_VisualizarCapituloPublicado::test_visualizar_capitulo_publicado_exitoso -v
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

## 🏗️ Estructura

```
tests/
├── conftest.py              # Fixtures (BD de test, cliente API, datos)
├── test_cp01_01_visualizar_capitulo.py  # 13 tests de CP01_01
└── test_models.py           # Tests unitarios de modelos
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

## ✨ Características

- ✅ 13 tests exhaustivos
- ✅ Base de datos en memoria
- ✅ No afecta BD de producción
- ✅ Ejecución rápida (< 1s)
- ✅ Reportes HTML interactivos
- ✅ Coverage detallado

## 🎓 Tips

1. **Ejecuta tests frecuentemente**: Feedback rápido
2. **Usa coverage**: Identifica código no probado
3. **Lee los reportes**: Entiende qué se está probando
4. **Agrega tests**: Para nuevos casos de uso

## ✅ Checklist

- [x] Tests implementados (13)
- [x] Todos pasando (13/13)
- [x] Coverage configurado
- [x] Reportes generando
- [x] Documentación completa
- [x] Scripts de ejecución
- [ ] Tests adicionales (CP01_02, etc.)

---

**¿Necesitas ayuda?** Consulta `tests/README.md` o `REPORTE_TESTING_CP01_01.md`

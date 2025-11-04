# Suite de Testing - Proyecto Libro Interactivo

## 📋 Descripción

Suite completa de testing para el proyecto, con enfoque especial en el caso de prueba **CP01_01 — Visualizar capítulo publicado (éxito)**.

## 🎯 Caso de Prueba Principal: CP01_01

### Información del Caso de Prueba

- **ID**: CP01_01
- **Caso de Uso**: CU_01 Visualizar contenido
- **Descripción**: Accede a un capítulo existente en estado publicado
- **Área Funcional**: Contenidos
- **Funcionalidad**: Lectura de capítulo

### Datos de Entrada
- Abrir `/capitulos/{id}` con ID válido y publicado

### Resultado Esperado
- ✅ Se muestran título, número e introducción (y resto de campos)
- ✅ Status code 200 OK
- ✅ Se registra la visualización si aplica
- ✅ Respuesta con estructura correcta según schema

### Ambiente de Pruebas
- Base de datos con al menos un capítulo en estado `PUBLICADO`

## 🚀 Ejecución Rápida

```bash
# Ejecutar tests de CP01_01 con coverage
cd codigo
./ejecutar_tests.sh

# O directamente con pytest
pytest tests/test_cp01_01_visualizar_capitulo.py -v
```

## 📊 Opciones de Ejecución

### 1. Solo CP01_01 (por defecto)
```bash
./ejecutar_tests.sh
# o
./ejecutar_tests.sh cp01
```

### 2. Todos los tests
```bash
./ejecutar_tests.sh all
```

### 3. Solo tests unitarios
```bash
./ejecutar_tests.sh unit
```

### 4. Solo tests de integración
```bash
./ejecutar_tests.sh integration
```

### 5. Ejecución rápida (sin coverage)
```bash
./ejecutar_tests.sh quick
```

### 6. Tests en paralelo (más rápido)
```bash
./ejecutar_tests.sh parallel
```

## 📁 Estructura de Tests

```
tests/
├── __init__.py                           # Inicialización del paquete
├── conftest.py                           # Fixtures compartidos
├── test_cp01_01_visualizar_capitulo.py  # Tests del caso CP01_01
└── test_models.py                        # Tests unitarios de modelos
```

### Archivos Principales

#### `conftest.py`
Contiene fixtures reutilizables:
- `test_db_engine`: Motor de BD SQLite en memoria
- `test_db_session`: Sesión de BD para cada test
- `client`: Cliente de prueba de FastAPI
- `capitulo_publicado`: Fixture con capítulo en estado PUBLICADO
- `capitulo_borrador`: Fixture con capítulo en BORRADOR
- `multiples_capitulos`: Fixture con varios capítulos en diferentes estados

#### `test_cp01_01_visualizar_capitulo.py`
Clases de test:
1. **TestCP01_01_VisualizarCapituloPublicado**: Tests principales del caso de uso
2. **TestCP01_01_CasosNegativos**: Tests de casos de error
3. **TestCP01_01_Integracion**: Tests de integración
4. **TestCP01_01_Performance**: Tests de rendimiento
5. **TestCP01_01_Regresion**: Tests de regresión

## 📈 Coverage (Cobertura)

### Visualizar Coverage
```bash
# Ejecutar tests con coverage
./ejecutar_tests.sh

# Abrir reporte HTML
xdg-open htmlcov/index.html
```

### Reportes Generados

Después de ejecutar los tests, se generan:

1. **HTML Coverage Report**: `htmlcov/index.html`
   - Reporte visual interactivo
   - Muestra líneas cubiertas y no cubiertas
   - Porcentaje de cobertura por archivo

2. **HTML Test Report**: `reports/cp01_01_report.html`
   - Reporte de resultados de tests
   - Información detallada de cada test
   - Screenshots si aplica

3. **JSON Coverage**: `coverage.json`
   - Datos de coverage en formato JSON
   - Para integración con CI/CD

4. **Terminal Report**
   - Muestra en consola las líneas no cubiertas
   - Resumen por archivo

### Objetivos de Coverage

- ✅ **Excelente**: >= 80%
- ⚠️ **Bueno**: >= 60%
- ❌ **Bajo**: < 60%

## 🧪 Tipos de Tests

### Tests Unitarios
Prueban funcionalidad individual:
- Modelos de base de datos
- Funciones y métodos aislados
- Validaciones de datos

```bash
pytest tests/test_models.py -v
```

### Tests de Integración
Prueban flujos completos:
- Endpoints de API
- Interacción con base de datos
- Flujos de usuario

```bash
pytest tests/test_cp01_01_visualizar_capitulo.py::TestCP01_01_Integracion -v
```

### Tests de Performance
Verifican rendimiento:
- Tiempo de respuesta
- Múltiples requests simultáneas

```bash
pytest tests/test_cp01_01_visualizar_capitulo.py::TestCP01_01_Performance -v
```

### Tests de Regresión
Aseguran que funcionalidades previas sigan funcionando:
- Compatibilidad con versiones anteriores
- Estructura de datos consistente

```bash
pytest tests/test_cp01_01_visualizar_capitulo.py::TestCP01_01_Regresion -v
```

## 🔧 Configuración

### pytest.ini
Configuración de pytest con:
- Paths de tests
- Opciones por defecto
- Markers personalizados
- Configuración de coverage

### Markers Personalizados
```python
@pytest.mark.unit        # Test unitario
@pytest.mark.integration # Test de integración
@pytest.mark.cp01_01     # Específico de CP01_01
@pytest.mark.performance # Test de rendimiento
@pytest.mark.regression  # Test de regresión
@pytest.mark.slow        # Test lento
```

Usar markers:
```bash
pytest -m unit           # Solo tests unitarios
pytest -m cp01_01        # Solo tests de CP01_01
pytest -m "not slow"     # Excluir tests lentos
```

## 📦 Dependencias de Testing

Las siguientes dependencias se instalan automáticamente:

```txt
pytest>=7.4.0                # Framework de testing
pytest-cov>=4.1.0           # Coverage
pytest-html>=3.2.0          # Reportes HTML
pytest-xdist>=3.3.0         # Tests paralelos
fastapi[all]>=0.104.0       # TestClient
httpx>=0.25.0               # Cliente HTTP para tests
```

## 🎨 Estructura de un Test

```python
def test_visualizar_capitulo_publicado_exitoso(self, client, capitulo_publicado):
    """
    Test Principal CP01_01: Visualizar capítulo publicado con éxito.
    
    GIVEN: Existe un capítulo en estado PUBLICADO
    WHEN: Se realiza GET a /capitulos/{id}
    THEN: Retorna 200 OK con datos completos
    """
    # Arrange (Preparar)
    capitulo_id = capitulo_publicado.id_capitulo
    
    # Act (Actuar)
    response = client.get(f"/capitulos/{capitulo_id}")
    
    # Assert (Verificar)
    assert response.status_code == 200
    data = response.json()
    assert data["estado"] == "PUBLICADO"
    assert data["titulo"] == capitulo_publicado.titulo
```

## 🐛 Debugging de Tests

### Ejecutar test específico con output detallado
```bash
pytest tests/test_cp01_01_visualizar_capitulo.py::TestCP01_01_VisualizarCapituloPublicado::test_visualizar_capitulo_publicado_exitoso -vvs
```

### Ver variables locales en fallos
```bash
pytest tests/ -l
```

### Detener en el primer fallo
```bash
pytest tests/ -x
```

### Modo interactivo (PDB)
```bash
pytest tests/ --pdb
```

### Ver prints durante tests
```bash
pytest tests/ -s
```

## 📊 Ejemplo de Output

```
================================================
  EJECUTANDO TESTS CON COVERAGE
  Caso de Prueba: CP01_01
================================================

🧪 Ejecutando tests de CP01_01...

tests/test_cp01_01_visualizar_capitulo.py::TestCP01_01_VisualizarCapituloPublicado::test_visualizar_capitulo_publicado_exitoso PASSED [ 10%]
tests/test_cp01_01_visualizar_capitulo.py::TestCP01_01_VisualizarCapituloPublicado::test_visualizar_capitulo_publicado_estructura_respuesta PASSED [ 20%]
...

---------- coverage: platform linux, python 3.13.x -----------
Name                              Stmts   Miss  Cover   Missing
---------------------------------------------------------------
api/routers/capitulos.py             45      2    95%   23-24
db/contenido/models.py               52      3    94%   145-147
---------------------------------------------------------------
TOTAL                               156      8    95%

✅ TESTS COMPLETADOS EXITOSAMENTE

📊 Reportes generados:
   - HTML Coverage: htmlcov/index.html
   - HTML Report: reports/cp01_01_report.html

📈 Resumen de Coverage:
   Cobertura Total: 95.00%
   ✅ Cobertura EXCELENTE (>= 80%)
```

## 🔄 Integración Continua

Los tests están listos para integrarse con CI/CD:

```yaml
# Ejemplo .github/workflows/tests.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          cd codigo
          pip install -r requirements.txt
          ./ejecutar_tests.sh all
```

## 📝 Notas Importantes

1. **Base de Datos de Test**: Los tests usan SQLite en memoria, NO afectan la BD de producción
2. **Aislamiento**: Cada test tiene su propia sesión de BD
3. **Estado Limpio**: Los fixtures garantizan estado inicial consistente
4. **Fast Feedback**: Tests rápidos para desarrollo ágil

## 🆘 Solución de Problemas

### Error: "No module named pytest"
```bash
pip install -r requirements.txt
```

### Error: "Database connection failed"
- Los tests usan SQLite en memoria, no necesitan MySQL
- Si el error persiste, verifica que SQLAlchemy esté instalado

### Tests lentos
```bash
# Usar ejecución paralela
./ejecutar_tests.sh parallel
```

### Coverage bajo
1. Identificar líneas no cubiertas: `xdg-open htmlcov/index.html`
2. Agregar tests para esas líneas
3. Ejecutar nuevamente: `./ejecutar_tests.sh`

## 📚 Recursos Adicionales

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites)

## ✅ Checklist de Testing

- [x] Fixtures configurados
- [x] Tests de CP01_01 implementados
- [x] Tests unitarios de modelos
- [x] Tests de integración
- [x] Tests de performance
- [x] Tests de regresión
- [x] Coverage configurado
- [x] Script de ejecución
- [x] Documentación completa
- [ ] Tests de casos de uso adicionales
- [ ] Tests de autenticación
- [ ] Tests de autorización

---

**Última actualización**: 3 de noviembre de 2025

# Libro Interactivo - Sistema de Gestión de Contenidos
========================================================

Este proyecto implementa un sistema de gestión de contenidos para libros interactivos en Python, organizado en una **arquitectura modular de paquetes independientes**.

## ⚡ Nueva Arquitectura: Paquetes Independientes

> **Actualización importante**: El proyecto ahora usa **paquetes independientes instalables** para cada componente.

### Estructura Actual

```
codigo/
├── api/                          # 🌐 API REST FastAPI
│   ├── main.py                   # Aplicación principal
│   ├── dependencies.py           # Dependencias inyectadas
│   ├── routers/                  # Endpoints por recurso
│   │   └── capitulos.py          # CRUD capítulos (100% tested)
│   ├── schemas/                  # Validación Pydantic
│   │   ├── capitulo.py
│   │   └── contenido.py
│   └── templates/                # Plantillas HTML
│
├── tests/                        # 🧪 Tests (115 tests - 100% passing)
│   ├── conftest.py               # Fixtures compartidos
│   ├── test_cp01_01_visualizar_capitulo.py   # 13 tests
│   ├── test_cp01_02_capitulo_inexistente.py  # 19 tests
│   ├── test_cp02_01_crear_capitulo.py        # 26 tests
│   ├── test_cp02_02_actualizar_capitulo.py   # 15 tests
│   ├── test_cp02_03_eliminar_capitulo.py     # 10 tests
│   ├── test_cp02_04_listar_capitulos.py      # 12 tests
│   ├── test_cp02_05_validaciones_estado.py   # 8 tests
│   └── test_models.py                         # 12 tests
│
├── testing/                      # 📄 Documentación de tests
│   ├── README.md                 # Índice
│   ├── GUIA_RAPIDA_TESTING.md   # Guía de ejecución
│   ├── RESUMEN_COMPLETO_TESTING.md  # Documento consolidado
│   └── REPORTE_TESTING_*.md      # Reportes detallados
│
├── paquetes/                     # 🎯 Paquetes independientes
│   ├── modelo_capitulo/          → libro-modelo-capitulo
│   ├── modelo_contenido/         → libro-modelo-contenido
│   ├── modelo_texto/             → libro-modelo-texto
│   ├── modelo_imagen/            → libro-modelo-imagen
│   ├── modelo_video/             → libro-modelo-video
│   ├── modelo_objeto3d/          → libro-modelo-objeto3d
│   ├── modelo_union/             → libro-modelo-union
│   ├── repositorio_capitulo/     → libro-repositorio-capitulo
│   ├── repositorio_contenido/    → libro-repositorio-contenido
│   ├── repositorio_union/        → libro-repositorio-union
│   ├── gestor_contenido/         → libro-gestor-contenido
│   ├── gestor_capitulo/          → libro-gestor-capitulo
│   └── README.md                 # Documentación detallada
│
├── db/                           # 💾 Base de datos
│   ├── contenido/models.py       # Modelos SQLAlchemy (89% coverage)
│   ├── usuarios/models.py
│   ├── evaluaciones/models.py
│   ├── config.py                 # Configuración de conexiones
│   ├── crear_tablas.py           # Script de creación
│   └── test_conexiones.py        # Verificar conectividad
│
├── htmlcov/                      # 📊 Reportes de coverage
├── reports/                      # 📈 Reportes de tests
│
├── ejecutar_tests.sh             # 🧪 Script de testing
├── pytest.ini                    # Configuración pytest
├── instalar_paquetes.sh          # 🚀 Instalar paquetes
├── crear_paquetes.py             # Script de creación
├── verificar_paquetes.py         # Verificar instalación
└── requirements.txt              # Dependencias Python
```

### Ver Documentación Completa

📖 **[Ver paquetes/README.md](paquetes/README.md)** para documentación completa de la arquitectura de paquetes.

## Arquitectura

El proyecto sigue una **arquitectura por capas**:

1. **Modelos**: Entidades de dominio (Contenido, Capitulo, etc.)
2. **Repositorios**: Acceso a datos y persistencia
3. **Gestores**: Lógica de negocio y orquestación

## 🚀 Inicio Rápido

### Instalación Completa (Recomendada)

```bash
cd codigo
bash instalar_paquetes.sh
```

Este script instala los 12 paquetes en el orden correcto según sus dependencias.

### Verificar Instalación

```bash
python3 verificar_paquetes.py
```

### Ver Ejemplos

```bash
python3 ejemplo_paquetes.py
```

### Instalación Manual Individual

Si solo necesitas paquetes específicos:

```bash
# Solo modelos (sin dependencias de BD)
cd paquetes/modelo_capitulo && pip install -e .
cd paquetes/modelo_contenido && pip install -e .

# Repositorios (requieren SQLAlchemy + MySQL)
cd paquetes/repositorio_capitulo && pip install -e .

# Gestores (lógica de negocio completa)
cd paquetes/gestor_capitulo && pip install -e .
```

## 💻 Uso

### Ejemplo 1: Solo Modelos (sin base de datos)

```python
from modelo_capitulo import Capitulo
from modelo_texto import Texto
from modelo_imagen import Imagen

# Crear objetos de dominio
capitulo = Capitulo(titulo="Introducción", numero=1)
texto = Texto(titulo="Variables", cuerpo="Las variables son...", formato="markdown")
imagen = Imagen(titulo="Diagrama", url_recurso="https://example.com/img.png")

print(capitulo)  # Capitulo(id=..., titulo='Introducción', numero=1)
print(texto)     # Texto(id=..., titulo='Variables', tipo='texto')
```

### Ejemplo 2: Con Repositorios (requiere MySQL)

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from repositorio_capitulo import RepositorioCapitulo
from modelo_capitulo import Capitulo

# Configurar conexión
engine = create_engine('mysql+pymysql://user:pass@host/contenido_db')
Session = sessionmaker(bind=engine)
session = Session()

# Usar repositorio
repo = RepositorioCapitulo(session)
capitulo = Capitulo(titulo="Capítulo 1", numero=1)
repo.guardar(capitulo)

# Buscar
cap = repo.buscar_por_id(capitulo.id)
print(f"Encontrado: {cap.titulo}")
```

### Ejemplo 3: Capa Completa con Gestores

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from gestor_capitulo import GestorCapitulo
from repositorio_capitulo import RepositorioCapitulo
from repositorio_contenido import RepositorioContenido
from repositorio_union import RepositorioUnionCapituloContenido

# Setup
engine = create_engine('mysql+pymysql://user:pass@host/contenido_db')
Session = sessionmaker(bind=engine)
session = Session()

# Crear repositorios y gestor
repo_cap = RepositorioCapitulo(session)
repo_cont = RepositorioContenido(session)
repo_union = RepositorioUnionCapituloContenido(session)
gestor = GestorCapitulo(repo_cap, repo_cont, repo_union)

# Operaciones de alto nivel
cap_id = gestor.crear_capitulo(titulo="Introducción", numero=1)
texto_id = gestor.agregar_texto_a_capitulo(
    capitulo_id=cap_id,
    titulo="Primer párrafo",
    cuerpo="Contenido...",
    formato="markdown",
    orden=1
)

# Obtener contenidos ordenados
contenidos = gestor.obtener_contenidos_ordenados(cap_id)
for cont in contenidos:
    print(f"- {cont.titulo} (tipo: {cont.tipo})")
```

Para más ejemplos, ejecuta: `python3 ejemplo_paquetes.py`

## Características

### Modelos

- **Contenido**: Clase abstracta base para todos los tipos de contenido
- **Texto**: Bloques de texto
- **Imagen**: Imágenes con formato
- **Video**: Videos con duración
- **Objeto3D**: Modelos 3D
- **Capitulo**: Capítulos del libro
- **UnionCapituloContenido**: Relación N:M entre capítulos y contenidos con orden

### Gestores

- **GestorContenido**:
  - Crear diferentes tipos de contenido
  - Actualizar y eliminar contenido
  - Buscar contenido por ID o tema

- **GestorCapitulo**:
  - Crear y gestionar capítulos
  - Asociar contenidos a capítulos
  - Mantener orden de contenidos
  - Obtener capítulos completos con contenidos

## 🗄️ Base de Datos

El sistema usa **3 bases de datos MySQL en AWS RDS**:

- **contenido_db**: Capítulos, Contenidos, Uniones
- **usuarios_db**: Usuarios, Roles, Permisos
- **evaluaciones_db**: Evaluaciones, Preguntas, Respuestas

### Configuración

1. Edita `db/config.py` con tus credenciales de AWS RDS
2. Verifica conectividad: `python3 db/test_conexiones.py`
3. Crea las tablas: `python3 db/crear_tablas.py`

Ver `db/README.md` para documentación completa de la estructura de bases de datos.

## 🧪 Testing

### Estado Actual: ✅ **115/115 tests pasando (100%)**

| Métrica | Valor |
|---------|-------|
| Tests Totales | 115 |
| Tests Pasando | 115 (100%) ✅ |
| Coverage Routers | 100% ⭐ |
| Coverage Models | 89% ✅ |
| Coverage Total | 31% |
| Tiempo Ejecución | ~3.7s |

### Suites de Tests Implementadas

- ✅ **CP01_01** (13 tests) - Visualizar capítulo publicado
- ✅ **CP01_02** (19 tests) - Manejo de errores y seguridad
- ✅ **CP02_01** (26 tests) - Crear capítulo
- ✅ **CP02_02** (15 tests) - Actualizar capítulo
- ✅ **CP02_03** (10 tests) - Eliminar capítulo
- ✅ **CP02_04** (12 tests) - Listar y filtrar capítulos
- ✅ **CP02_05** (8 tests) - Validaciones de estado
- ✅ **test_models** (12 tests) - Tests unitarios ORM

### Ejecutar Tests

```bash
# Todos los tests
./ejecutar_tests.sh all

# Por caso de prueba
./ejecutar_tests.sh cp02_01    # Crear capítulo
./ejecutar_tests.sh cp02_02    # Actualizar capítulo
./ejecutar_tests.sh cp02_03    # Eliminar capítulo

# Ver reportes
xdg-open htmlcov/index.html
```

### Documentación de Testing

- **[testing/GUIA_RAPIDA_TESTING.md](testing/GUIA_RAPIDA_TESTING.md)** - Guía rápida de ejecución
- **[testing/RESUMEN_COMPLETO_TESTING.md](testing/RESUMEN_COMPLETO_TESTING.md)** - Documento consolidado (115 tests)
- **[testing/](testing/)** - Todos los reportes detallados

---

## 📊 Estado del Proyecto

✅ **Completado**:
- 12 paquetes independientes instalables
- Modelos de dominio (7 clases)
- Repositorios con SQLAlchemy ORM
- Gestores de lógica de negocio
- Modelos SQLAlchemy para 3 bases de datos (15 tablas)
- Scripts de instalación y verificación
- **API REST FastAPI con CRUD completo**
- **115 tests con 100% coverage en endpoints**
- Documentación completa

🔄 **En Desarrollo**:
- Tests de contenidos y relaciones N:M
- Validaciones de negocio adicionales
- Frontend (React/Vue)

## 📦 Paquetes Disponibles

| Paquete | Descripción | Dependencias |
|---------|-------------|--------------|
| `libro-modelo-capitulo` | Modelo Capítulo | - |
| `libro-modelo-contenido` | Modelo base Contenido | - |
| `libro-modelo-texto` | Modelo Texto | modelo-contenido |
| `libro-modelo-imagen` | Modelo Imagen | modelo-contenido |
| `libro-modelo-video` | Modelo Video | modelo-contenido |
| `libro-modelo-objeto3d` | Modelo Objeto3D | modelo-contenido |
| `libro-modelo-union` | Modelo Unión | - |
| `libro-repositorio-capitulo` | Repositorio Capítulo | modelo-capitulo, SQLAlchemy |
| `libro-repositorio-contenido` | Repositorio Contenido | modelo-contenido, SQLAlchemy |
| `libro-repositorio-union` | Repositorio Unión | modelo-union, SQLAlchemy |
| `libro-gestor-contenido` | Gestor Contenido | repositorio-contenido |
| `libro-gestor-capitulo` | Gestor Capítulo | repositorio-capitulo, repositorio-union |

## 🎯 Ventajas de esta Arquitectura

1. **Modularidad**: Cada componente es independiente
2. **Reutilización**: Usa solo lo que necesites
3. **Versionado**: Cada paquete tiene su propia versión
4. **Testing**: Fácil testear componentes aislados
5. **Mantenibilidad**: Cambios localizados no afectan otros paquetes
6. **Despliegue**: Instala solo lo necesario por ambiente

## 📋 Requisitos

- Python >= 3.8
- SQLAlchemy >= 2.0.0
- PyMySQL >= 1.1.0
- MySQL 8.0 (AWS RDS)

## 📚 Documentación

- **[paquetes/README.md](paquetes/README.md)**: Arquitectura de paquetes completa
- **[db/README.md](db/README.md)**: Estructura de bases de datos
- **[db/ESQUEMAS.md](db/ESQUEMAS.md)**: Esquemas detallados de tablas
- **[db/DIAGRAMAS.md](db/DIAGRAMAS.md)**: Diagramas de relaciones
- **[ARQUITECTURA.md](ARQUITECTURA.md)**: Visión general del sistema

## 🔧 Scripts Útiles

| Script | Descripción |
|--------|-------------|
| `instalar_paquetes.sh` | Instala todos los paquetes |
| `verificar_paquetes.py` | Verifica instalación correcta |
| `ejemplo_paquetes.py` | Ejemplos de uso |
| `crear_paquetes.py` | Regenera estructura de paquetes |
| `db/crear_tablas.py` | Crea tablas en MySQL |
| `db/test_conexiones.py` | Verifica conexión a BD |

## 👥 Autores

Anibal Cordoba & Zabala

## 📄 Licencia

Proyecto educativo - Universidad [Nombre]

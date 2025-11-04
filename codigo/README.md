# 📚 Libro Interactivo - Sistema de Gestión de Contenidos

> Sistema web completo para la gestión y visualización de libros educativos interactivos con capítulos y contenidos multimedia.

## 🚀 Estado del Proyecto: **Funcional y Operativo** ✅

- ✅ **API REST** completa con FastAPI
- ✅ **Interfaz Web** para gestión de contenidos
- ✅ **Base de datos** SQLite configurada
- ✅ **Sistema de contenidos** con 4 tipos multimedia
- ✅ **Tests automatizados** (115 tests implementados)

---

## ⚡ Inicio Rápido

### 1. Iniciar el servidor

```bash
cd codigo
./iniciar_api_final.sh
```

El servidor estará disponible en:
- 🌐 **Aplicación**: http://localhost:8000
- 📚 **Documentación API**: http://localhost:8000/docs
- 🔍 **Health Check**: http://localhost:8000/health

### 2. Acceder a la interfaz web

1. **Página principal**: http://localhost:8000
2. **Crear capítulos**: http://localhost:8000/crear-capitulo
3. **Ver capítulos**: http://localhost:8000/ver-capitulos (con contenidos expandibles)
4. **Gestionar contenidos**: http://localhost:8000/gestionar-contenidos

---

## 📁 Estructura del Proyecto

```
codigo/
├── api/                              # 🌐 API REST FastAPI
│   ├── main.py                       # Aplicación principal
│   ├── dependencies.py               # Gestión de BD (SQLite/MySQL)
│   ├── routers/                      # Endpoints por recurso
│   │   ├── capitulos.py              # CRUD capítulos
│   │   └── contenidos.py             # CRUD contenidos + asignaciones
│   ├── schemas/                      # Validación Pydantic
│   │   ├── capitulo.py               # Schemas de capítulos
│   │   └── contenido.py              # Schemas de contenidos
│   └── templates/                    # Plantillas HTML
│       ├── index.html                # Página principal
│       ├── crear_capitulo.html       # Formulario de capítulos
│       ├── ver_capitulos.html        # Vista con contenidos expandibles
│       └── gestionar_contenidos.html # CRUD de contenidos
│
├── db/                               # 💾 Base de datos
│   ├── config.py                     # Configuración base SQLAlchemy
│   └── contenido/                    # Modelos de contenido
│       ├── models.py                 # Capitulo, Contenido, Union
│       └── __init__.py
│
├── data/                             # 📊 Datos persistentes
│   └── contenido.db                  # Base de datos SQLite
│
├── tests/                            # 🧪 Tests automatizados
│   ├── conftest.py                   # Fixtures compartidos
│   ├── test_cp01_01_*.py             # Tests de visualización
│   ├── test_cp02_01_*.py             # Tests de creación
│   ├── test_cp02_02_*.py             # Tests de actualización
│   ├── test_cp02_03_*.py             # Tests de eliminación
│   ├── test_cp02_04_*.py             # Tests de listado
│   ├── test_cp02_05_*.py             # Tests de validaciones
│   └── test_models.py                # Tests de modelos ORM
│
├── testing/                          # � Documentación de testing
│   ├── GUIA_RAPIDA_TESTING.md        # Guía de ejecución
│   └── RESUMEN_COMPLETO_TESTING.md   # Documento consolidado
│
├── iniciar_api_final.sh              # 🚀 Script para iniciar servidor
├── inicializar_db.py                 # 🗄️ Crear tablas en BD
├── limpiar_db.py                     # 🧹 Limpiar datos de desarrollo
├── limpiar_tests.py                  # 🧹 Limpiar datos de tests
├── ejecutar_tests.sh                 # 🧪 Script de testing
├── pytest.ini                        # ⚙️ Configuración pytest
├── requirements.txt                  # 📦 Dependencias Python
└── README.md                         # 📖 Este archivo
```

---

## 📦 Arquitectura de Paquetes Modulares

El proyecto utiliza una **arquitectura de paquetes descargables e instalables** que permite:
- ✅ **Reutilizar código** en otros proyectos
- ✅ **Instalar solo lo necesario** (modular)
- ✅ **Desarrollar en modo editable** (cambios instantáneos)
- ✅ **Separación clara** de responsabilidades

### Estructura de Paquetes

```
paquetes/
├── gestor_capitulo/          # 🎯 Lógica de negocio para capítulos
│   ├── gestor_capitulo.py    #    - Validaciones y reglas de negocio
│   ├── setup.py              #    - CRUD completo con manejo de errores
│   └── __init__.py           #    - Estados (BORRADOR, PUBLICADO, ARCHIVADO)
│
├── gestor_contenido/         # 🎯 Lógica de negocio para contenidos
│   ├── gestor_contenido.py   #    - 4 tipos: texto, imagen, video, objeto3d
│   ├── setup.py              #    - Asignación a capítulos con orden
│   └── __init__.py           #    - Validaciones por tipo de contenido
│
├── modelo_capitulo/          # 📊 Modelo ORM del Capítulo
├── modelo_contenido/         # 📊 Modelo ORM base de Contenido
├── modelo_texto/             # 📊 Modelo ORM de Texto
├── modelo_imagen/            # 📊 Modelo ORM de Imagen
├── modelo_video/             # 📊 Modelo ORM de Video
├── modelo_objeto3d/          # 📊 Modelo ORM de Objeto3D
├── repositorio_capitulo/     # 💾 Acceso a datos de capítulos
├── repositorio_contenido/    # 💾 Acceso a datos de contenidos
└── repositorio_union/        # 💾 Relaciones capítulo-contenido
```

### 🚀 Instalar Paquetes

#### Opción 1: Instalar todos los paquetes (Recomendado)

```bash
# Desde el directorio codigo/
./instalar_paquetes.sh
```

Este script instalará todos los paquetes en **modo desarrollo** (`pip install -e`), lo que significa:
- Los cambios se reflejan inmediatamente sin reinstalar
- Puedes editar el código y usar los cambios al instante
- Perfecto para desarrollo activo

#### Opción 2: Instalar paquetes individualmente

```bash
# Instalar solo el gestor de capítulos
pip install -e paquetes/gestor_capitulo/

# Instalar solo el gestor de contenidos
pip install -e paquetes/gestor_contenido/

# Verificar instalación
pip list | grep "libro-"
```

### 📚 Uso de los Gestores

Los **routers** de la API ahora son simples **adaptadores** que delegan toda la lógica a los gestores:

```python
# api/routers/capitulos.py
from gestor_capitulo import GestorCapitulo

@router.post("/")
def crear_capitulo(capitulo: CapituloCreate, db: Session = Depends(get_db)):
    gestor = GestorCapitulo(db, Capitulo)
    resultado, error = gestor.crear_capitulo(
        numero=capitulo.numero,
        titulo=capitulo.titulo,
        tema=capitulo.tema
    )
    if error:
        raise HTTPException(status_code=400, detail=error)
    return resultado
```

**Beneficios**:
- 🧪 **Testeable**: Puedes probar los gestores sin FastAPI
- 🔄 **Reutilizable**: Usa los gestores en otros proyectos
- 📦 **Modular**: Instala solo lo que necesitas
- 🛡️ **Separación**: Router ≠ Lógica de negocio

---

## 🗄️ Base de Datos

El sistema utiliza **SQLite** para desarrollo (fácil de configurar) con soporte para **MySQL** en producción.

### Tablas Principales

1. **capitulos**
   - id_capitulo (UUID)
   - titulo, numero, introduccion, tema
   - estado (BORRADOR, PUBLICADO, ARCHIVADO)
   - fecha_creacion, fecha_modificacion

2. **contenidos**
   - id_contenido (UUID)
   - tipo (texto, imagen, video, objeto3d)
   - tema, cuerpo_texto, url_archivo
   - formato, duracion
   - fecha_creacion, fecha_modificacion

3. **union_capitulo_contenido**
   - id, id_capitulo, id_contenido
   - orden (para ordenar contenidos)

### Configuración

#### Desarrollo (SQLite - Por defecto)
```bash
# Ya está configurado, solo ejecuta:
python inicializar_db.py
```

#### Producción (MySQL)
```bash
# 1. Configura las variables de entorno
export USE_SQLITE=false
export DATABASE_URL_CONTENIDO="mysql+pymysql://user:pass@host/contenido_db"

# 2. Crea las tablas
python db/crear_tablas.py
```

### Scripts de Utilidad

```bash
# Limpiar todos los datos
python limpiar_db.py

# Limpiar solo datos de prueba
python limpiar_tests.py

# Inicializar/Recrear tablas
python inicializar_db.py
```

## 🧪 Testing

## 🌐 API REST

### Endpoints Disponibles

#### Capítulos
- `POST   /api/capitulos/` - Crear capítulo
- `GET    /api/capitulos/` - Listar capítulos (con filtros)
- `GET    /api/capitulos/{id}` - Obtener capítulo específico
- `PUT    /api/capitulos/{id}` - Actualizar capítulo
- `DELETE /api/capitulos/{id}` - Eliminar capítulo

#### Contenidos
- `POST   /api/contenidos/` - Crear contenido (texto/imagen/video/objeto3d)
- `GET    /api/contenidos/` - Listar contenidos (con filtros)
- `GET    /api/contenidos/{id}` - Obtener contenido específico
- `DELETE /api/contenidos/{id}` - Eliminar contenido
- `POST   /api/contenidos/asignar` - Asignar contenido a capítulo
- `GET    /api/contenidos/capitulo/{id}` - Listar contenidos de un capítulo
- `DELETE /api/contenidos/desasignar` - Desasignar contenido de capítulo

### Documentación Interactiva

Una vez iniciado el servidor, accede a:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Puedes probar todos los endpoints directamente desde la interfaz.

## 🧪 Testing

### Estado Actual: ⚠️ **115 tests implementados**

> **Nota**: Los tests tienen problemas de aislamiento de BD. Se recomienda usar la aplicación web directamente. Ver [Opción 2](#opción-2-ignorar-tests-por-ahora-recomendado).

| Suite | Tests | Descripción |
|-------|-------|-------------|
| **CP01_01** | 13 | Visualizar capítulo publicado |
| **CP01_02** | 19 | Manejo de errores y seguridad |
| **CP02_01** | 26 | Crear capítulo |
| **CP02_02** | 15 | Actualizar capítulo |
| **CP02_03** | 10 | Eliminar capítulo |
| **CP02_04** | 12 | Listar y filtrar capítulos |
| **CP02_05** | 8 | Validaciones de estado |
| **test_models** | 12 | Tests unitarios ORM |

### Opción 1: Ejecutar tests (requiere limpieza manual)

```bash
# 1. Limpiar BD antes de tests
python limpiar_db.py

# 2. Ejecutar tests
./ejecutar_tests.sh all

# 3. Limpiar BD después de tests
python limpiar_db.py
```

### Opción 2: Ignorar tests por ahora (Recomendado)

Los tests funcionan pero contaminan la BD de desarrollo. **Usa la interfaz web** para trabajar sin problemas.

### Documentación de Testing

- **[testing/GUIA_RAPIDA_TESTING.md](testing/GUIA_RAPIDA_TESTING.md)** - Guía de ejecución
- **[testing/RESUMEN_COMPLETO_TESTING.md](testing/RESUMEN_COMPLETO_TESTING.md)** - Documento consolidado (115 tests)
- **[GUIA_CONTENIDOS.md](GUIA_CONTENIDOS.md)** - Guía del sistema de contenidos

---

## 💻 Uso Avanzado

### Ejemplo: Crear capítulo via API

```bash
curl -X POST "http://localhost:8000/api/capitulos/" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Introducción a Python",
    "numero": 1,
    "tema": "Programación",
    "introduccion": "En este capítulo aprenderemos...",
    "estado": "BORRADOR"
  }'
```

### Ejemplo: Crear contenido de texto

```bash
curl -X POST "http://localhost:8000/api/contenidos/" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "texto",
    "tema": "Variables",
    "cuerpo_texto": "Las variables son espacios de memoria...",
    "formato": "markdown"
  }'
```

### Ejemplo: Asignar contenido a capítulo

```bash
curl -X POST "http://localhost:8000/api/contenidos/asignar?id_capitulo=<UUID>&id_contenido=<UUID>&orden=1"
```

## 📋 Requisitos

### Dependencias Principales
- Python >= 3.13
- FastAPI >= 0.115.0
- SQLAlchemy >= 2.0.0
- Uvicorn >= 0.32.0
- Pydantic >= 2.10.0

### Instalación de Dependencias

```bash
# 1. Instalar dependencias externas (FastAPI, SQLAlchemy, etc.)
pip install -r requirements.txt

# 2. Instalar paquetes modulares del proyecto
./instalar_paquetes.sh
```

**Nota**: El paso 2 instala los paquetes locales (`gestor_capitulo`, `gestor_contenido`, etc.) en modo desarrollo, permitiendo que los cambios se reflejen inmediatamente.

## 📚 Documentación Adicional

- **[GUIA_CONTENIDOS.md](GUIA_CONTENIDOS.md)** - Guía completa del sistema de contenidos
- **[CONFIGURACION_API.md](CONFIGURACION_API.md)** - Configuración avanzada de la API
- **[db/README.md](db/README.md)** - Documentación de la base de datos (si existe)

## 🔧 Scripts Disponibles

| Script | Descripción | Uso |
|--------|-------------|-----|
| `instalar_paquetes.sh` | **NUEVO**: Instala paquetes modulares | `./instalar_paquetes.sh` |
| `iniciar_api_final.sh` | Inicia el servidor web | `./iniciar_api_final.sh` |
| `inicializar_db.py` | Crea las tablas en la BD | `python inicializar_db.py` |
| `limpiar_db.py` | Limpia todos los datos | `python limpiar_db.py` |
| `limpiar_tests.py` | Limpia datos de prueba | `python limpiar_tests.py` |
| `ejecutar_tests.sh` | Ejecuta tests automatizados | `./ejecutar_tests.sh all` |

## 🐛 Solución de Problemas

### Error: "Address already in use"
```bash
pkill -f "uvicorn"
./iniciar_api_final.sh
```

### Error: "No such table"
```bash
python inicializar_db.py
./iniciar_api_final.sh
```

### BD con muchos datos de prueba
```bash
python limpiar_db.py  # Ingresa "SI" para confirmar
```

## 👥 Autores

Aníbal Córdoba & Zabala

## 📄 Licencia

Proyecto educativo

---

**🚀 ¡Listo para usar! Ejecuta `./iniciar_api_final.sh` y abre http://localhost:8000**

---

## 📄 Licencia

Proyecto educativo - Universidad [UNER]

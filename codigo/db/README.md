# Base de Datos - Libro Virtual Interactivo
============================================

Este directorio contiene los modelos SQLAlchemy y la configuración para las **3 bases de datos MySQL** desplegadas en Amazon RDS.

## Estructura

```
db/
├── config.py              # Configuración de conexiones a las 3 BDs
├── crear_tablas.py        # Script para crear todas las tablas
├── ESQUEMAS.md            # Documentación SQL de todas las tablas
├── contenido/             # BD 1: Contenido del libro
│   ├── __init__.py
│   └── models.py          # Modelos: Capitulo, Contenido, UnionCapituloContenido
├── usuarios/              # BD 2: Usuarios y permisos
│   ├── __init__.py
│   └── models.py          # Modelos: Usuario, Estudiante, Docente, Rol, Permiso
└── evaluaciones/          # BD 3: Evaluaciones y resultados
    ├── __init__.py
    └── models.py          # Modelos: Evaluacion, Pregunta, Intento, Respuesta
```

## Bases de Datos

### 1. contenido_db
Almacena el contenido del libro virtual:
- **capitulos**: Capítulos del libro
- **contenidos**: Texto, imágenes, videos, objetos 3D
- **union_capitulo_contenido**: Relación N:M con orden

### 2. usuarios_db
Gestiona usuarios y permisos:
- **usuarios**: Información base de usuarios
- **estudiantes**: Datos específicos de estudiantes
- **docentes**: Datos específicos de docentes
- **roles**: Roles del sistema
- **permisos**: Permisos granulares
- **usuario_rol**: Asignación de roles
- **rol_permiso**: Asignación de permisos a roles

### 3. evaluaciones_db
Maneja evaluaciones y resultados:
- **evaluaciones**: Evaluaciones por capítulo
- **preguntas**: Preguntas de evaluaciones
- **opciones**: Opciones de respuesta
- **intentos**: Intentos de estudiantes
- **respuestas**: Respuestas individuales

## Configuración

### 1. Variables de Entorno

Copia `.env.example` a `.env` y configura las credenciales de RDS:

```bash
cp ../.env.example ../.env
```

Edita `.env` con tus credenciales:

```env
# Contenido
CONTENIDO_DB_HOST=contenido-rds.xxx.rds.amazonaws.com
CONTENIDO_DB_USER=admin
CONTENIDO_DB_PASSWORD=tu_password

# Usuarios
USUARIOS_DB_HOST=usuarios-rds.xxx.rds.amazonaws.com
USUARIOS_DB_USER=admin
USUARIOS_DB_PASSWORD=tu_password

# Evaluaciones
EVALUACIONES_DB_HOST=evaluaciones-rds.xxx.rds.amazonaws.com
EVALUACIONES_DB_USER=admin
EVALUACIONES_DB_PASSWORD=tu_password
```

### 2. Crear Bases de Datos en MySQL

Primero, crea las 3 bases de datos en tus instancias RDS:

```sql
-- En cada instancia RDS:
CREATE DATABASE contenido_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE usuarios_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE evaluaciones_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Crear Tablas

Ejecuta el script para crear todas las tablas:

```bash
cd db/
python crear_tablas.py
```

Este script:
1. Se conecta a las 3 bases de datos
2. Crea todas las tablas con sus relaciones
3. Crea los índices necesarios

## Uso de los Modelos

### Ejemplo: Base de Datos de Contenido

```python
from db.config import get_contenido_session
from db.contenido.models import Capitulo, Texto

# Obtener sesión
session = get_contenido_session()

# Crear un capítulo
capitulo = Capitulo(
    titulo="Introducción a Python",
    numero=1,
    introduccion="Este capítulo cubre los fundamentos...",
    tema="Python Básico"
)
session.add(capitulo)
session.commit()

# Crear contenido de texto
texto = Texto(
    cuerpo_texto="Python es un lenguaje de programación...",
    tema="Python Básico"
)
session.add(texto)
session.commit()

# Cerrar sesión
session.close()
```

### Ejemplo: Base de Datos de Usuarios

```python
from db.config import get_usuarios_session
from db.usuarios.models import Usuario, Estudiante, TipoUsuario

session = get_usuarios_session()

# Crear usuario estudiante
usuario = Usuario(
    email="estudiante@universidad.edu",
    password_hash="hash_bcrypt_aqui",
    nombre="Juan",
    apellido="Pérez",
    tipo_usuario=TipoUsuario.ESTUDIANTE
)
session.add(usuario)
session.commit()

# Crear perfil de estudiante
estudiante = Estudiante(
    id_usuario=usuario.id_usuario,
    matricula="2024001",
    carrera="Ingeniería en Sistemas",
    semestre=3
)
session.add(estudiante)
session.commit()

session.close()
```

### Ejemplo: Base de Datos de Evaluaciones

```python
from db.config import get_evaluaciones_session
from db.evaluaciones.models import Evaluacion, Pregunta, TipoPregunta

session = get_evaluaciones_session()

# Crear evaluación
evaluacion = Evaluacion(
    id_capitulo="uuid-del-capitulo",
    titulo="Evaluación Capítulo 1",
    descripcion="Evalúa conceptos básicos",
    duracion_minutos=30,
    id_docente_creador="uuid-del-docente"
)
session.add(evaluacion)
session.commit()

# Agregar pregunta
pregunta = Pregunta(
    id_evaluacion=evaluacion.id_evaluacion,
    tipo=TipoPregunta.OPCION_MULTIPLE,
    enunciado="¿Qué es Python?",
    orden=1,
    puntos=10.0
)
session.add(pregunta)
session.commit()

session.close()
```

## Migraciones con Alembic

Para gestionar cambios en el esquema, usa Alembic:

```bash
# Inicializar Alembic (ya configurado)
alembic init alembic

# Crear migración
alembic revision --autogenerate -m "Descripción del cambio"

# Aplicar migración
alembic upgrade head

# Revertir migración
alembic downgrade -1
```

## Características de los Modelos

### Single Table Inheritance (Contenido)
Los tipos de contenido (Texto, Imagen, Video, Objeto3D) usan herencia de tabla única:
- Una sola tabla `contenidos` con campo `tipo`
- Cada subclase mapea al mismo esquema
- Eficiente para consultas polimórficas

### Relaciones Configuradas
- **Cascade Delete**: Al eliminar un padre, se eliminan hijos automáticamente
- **Back References**: Navegación bidireccional entre entidades
- **Lazy Loading**: Relaciones se cargan bajo demanda

### Auditoría Automática
Todos los modelos tienen:
- `fecha_creacion`: Timestamp de creación
- `fecha_modificacion`: Timestamp de última actualización (auto-update)

### UUIDs como Primary Keys
Se usan UUIDs (VARCHAR 36) para:
- IDs únicos globalmente
- Compatibilidad entre sistemas distribuidos
- Seguridad (no se pueden inferir secuencias)

## Seguridad

⚠️ **IMPORTANTE**:
1. Nunca subas el archivo `.env` al repositorio
2. Usa usuarios de BD con permisos mínimos necesarios
3. Habilita SSL/TLS para conexiones a RDS
4. Implementa rate limiting en la API
5. Usa prepared statements (SQLAlchemy lo hace automáticamente)

## Monitoreo

Considera implementar:
- Logs de queries lentas
- Métricas de conexiones activas
- Alertas de errores de BD
- Backups automáticos (RDS lo hace nativamente)

## Documentación Adicional

- Ver `ESQUEMAS.md` para DDL completo de todas las tablas
- Ver `../ARQUITECTURA.md` para arquitectura general del sistema
- Consulta SQLAlchemy docs: https://docs.sqlalchemy.org/

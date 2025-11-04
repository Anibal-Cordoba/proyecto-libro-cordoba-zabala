# Arquitectura de Paquetes Independientes

## Descripción

Este proyecto implementa un sistema de libro virtual interactivo con una arquitectura modular basada en **paquetes independientes e instalables**. Cada componente (modelo, repositorio, gestor) es un paquete Python separado que puede instalarse de forma independiente.

## Estructura de Paquetes

```
paquetes/
├── modelo_capitulo/          → libro-modelo-capitulo
├── modelo_contenido/         → libro-modelo-contenido
├── modelo_texto/             → libro-modelo-texto
├── modelo_imagen/            → libro-modelo-imagen
├── modelo_video/             → libro-modelo-video
├── modelo_objeto3d/          → libro-modelo-objeto3d
├── modelo_union/             → libro-modelo-union
├── repositorio_capitulo/     → libro-repositorio-capitulo
├── repositorio_contenido/    → libro-repositorio-contenido
├── repositorio_union/        → libro-repositorio-union
├── gestor_contenido/         → libro-gestor-contenido
└── gestor_capitulo/          → libro-gestor-capitulo
```

## Capas de la Arquitectura

### 1️⃣ Capa de Modelos (Domain Layer)
Clases de dominio sin dependencias externas:

- **libro-modelo-capitulo**: Modelo Capítulo
- **libro-modelo-contenido**: Modelo abstracto Contenido (base)
- **libro-modelo-texto**: Modelo Texto (hereda de Contenido)
- **libro-modelo-imagen**: Modelo Imagen (hereda de Contenido)
- **libro-modelo-video**: Modelo Video (hereda de Contenido)
- **libro-modelo-objeto3d**: Modelo Objeto3D (hereda de Contenido)
- **libro-modelo-union**: Modelo UnionCapituloContenido

### 2️⃣ Capa de Repositorios (Data Access Layer)
Gestión de persistencia con SQLAlchemy:

- **libro-repositorio-capitulo**: CRUD para Capítulos
  - Depende de: `libro-modelo-capitulo`, `sqlalchemy`, `pymysql`
  
- **libro-repositorio-contenido**: CRUD para Contenidos
  - Depende de: `libro-modelo-contenido`, `sqlalchemy`, `pymysql`
  
- **libro-repositorio-union**: CRUD para Uniones Capítulo-Contenido
  - Depende de: `libro-modelo-union`, `sqlalchemy`, `pymysql`

### 3️⃣ Capa de Gestores (Business Logic Layer)
Lógica de negocio de alto nivel:

- **libro-gestor-contenido**: Gestión de contenidos
  - Depende de: `libro-modelo-contenido`, `libro-repositorio-contenido`
  
- **libro-gestor-capitulo**: Gestión de capítulos
  - Depende de: `libro-modelo-capitulo`, `libro-repositorio-capitulo`, `libro-repositorio-union`

## Instalación

### Opción 1: Instalación Completa (Recomendada)

```bash
cd codigo
bash instalar_paquetes.sh
```

Este script instala todos los paquetes en el orden correcto según sus dependencias.

### Opción 2: Instalación Manual Individual

Si solo necesitas paquetes específicos:

```bash
# Instalar solo modelos
cd paquetes/modelo_capitulo && pip install -e .
cd paquetes/modelo_contenido && pip install -e .

# Instalar repositorios (requieren modelos instalados)
cd paquetes/repositorio_capitulo && pip install -e .

# Instalar gestores (requieren modelos y repositorios)
cd paquetes/gestor_capitulo && pip install -e .
```

### Verificar Instalación

```bash
pip list | grep libro
```

Deberías ver los 12 paquetes instalados:
```
libro-gestor-capitulo      0.1.0
libro-gestor-contenido     0.1.0
libro-modelo-capitulo      0.1.0
libro-modelo-contenido     0.1.0
libro-modelo-imagen        0.1.0
libro-modelo-objeto3d      0.1.0
libro-modelo-texto         0.1.0
libro-modelo-union         0.1.0
libro-modelo-video         0.1.0
libro-repositorio-capitulo 0.1.0
libro-repositorio-contenido 0.1.0
libro-repositorio-union    0.1.0
```

## Uso

### Ejemplo 1: Usar Solo Modelos

```python
from modelo_capitulo import Capitulo
from modelo_texto import Texto

# Crear objetos de dominio
capitulo = Capitulo(titulo="Introducción", numero=1)
texto = Texto(
    titulo="Párrafo 1",
    cuerpo="Este es el contenido del texto...",
    formato="markdown"
)

print(capitulo)
print(texto)
```

### Ejemplo 2: Usar Repositorios

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from repositorio_capitulo import RepositorioCapitulo
from modelo_capitulo import Capitulo

# Configurar conexión a base de datos
engine = create_engine('mysql+pymysql://user:pass@host/contenido_db')
Session = sessionmaker(bind=engine)
session = Session()

# Usar repositorio
repo = RepositorioCapitulo(session)
capitulo = Capitulo(titulo="Capítulo 1", numero=1)
repo.guardar(capitulo)

# Buscar
cap_encontrado = repo.buscar_por_id(capitulo.id)
print(cap_encontrado.titulo)
```

### Ejemplo 3: Usar Gestores (Capa Completa)

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

# Crear gestores
repo_capitulo = RepositorioCapitulo(session)
repo_contenido = RepositorioContenido(session)
repo_union = RepositorioUnionCapituloContenido(session)

gestor = GestorCapitulo(repo_capitulo, repo_contenido, repo_union)

# Operaciones de alto nivel
capitulo_id = gestor.crear_capitulo(
    titulo="Introducción a Python",
    numero=1,
    descripcion="Conceptos básicos"
)

texto_id = gestor.agregar_texto_a_capitulo(
    capitulo_id=capitulo_id,
    titulo="Variables",
    cuerpo="Las variables en Python...",
    formato="markdown",
    orden=1
)
```

## Grafo de Dependencias

```mermaid
graph TD
    MC[modelo_capitulo]
    MCO[modelo_contenido]
    MT[modelo_texto]
    MI[modelo_imagen]
    MV[modelo_video]
    MO[modelo_objeto3d]
    MU[modelo_union]
    
    RC[repositorio_capitulo]
    RCO[repositorio_contenido]
    RU[repositorio_union]
    
    GC[gestor_capitulo]
    GCO[gestor_contenido]
    
    MCO --> MT
    MCO --> MI
    MCO --> MV
    MCO --> MO
    
    MC --> RC
    MCO --> RCO
    MU --> RU
    
    RC --> GC
    RCO --> GC
    RU --> GC
    
    RCO --> GCO
    MCO --> GCO
```

## Ventajas de esta Arquitectura

1. **Modularidad**: Cada paquete puede desarrollarse, testearse y desplegarse independientemente
2. **Reutilización**: Los modelos pueden usarse sin necesidad de los repositorios
3. **Versionado**: Cada paquete tiene su propia versión semántica
4. **Mantenibilidad**: Cambios en un paquete no afectan a otros (si se respeta la interfaz)
5. **Testing**: Más fácil testear componentes aislados
6. **Despliegue Flexible**: Instalar solo lo necesario en cada ambiente

## Orden de Instalación (Importante)

```
1. Modelos base (sin dependencias)
   ├── modelo_capitulo
   ├── modelo_contenido
   └── modelo_union

2. Modelos derivados (dependen de modelo_contenido)
   ├── modelo_texto
   ├── modelo_imagen
   ├── modelo_video
   └── modelo_objeto3d

3. Repositorios (dependen de modelos + SQLAlchemy)
   ├── repositorio_capitulo
   ├── repositorio_contenido
   └── repositorio_union

4. Gestores (dependen de repositorios + modelos)
   ├── gestor_contenido
   └── gestor_capitulo
```

## Desarrollo

### Crear un nuevo paquete

1. Crear directorio en `paquetes/nombre_paquete/`
2. Agregar `__init__.py`, `setup.py`, `README.md`
3. Definir dependencias en `setup.py`
4. Instalar en modo desarrollo: `pip install -e .`

### Actualizar un paquete existente

```bash
cd paquetes/nombre_paquete
# Hacer cambios en el código
# No es necesario reinstalar si usas -e (editable)
```

### Desinstalar paquetes

```bash
pip uninstall libro-modelo-capitulo
# O desinstalar todos
pip uninstall $(pip list | grep libro | awk '{print $1}')
```

## Bases de Datos

Los repositorios se conectan a 3 bases de datos MySQL en AWS RDS:

- **contenido_db**: Capítulos, Contenidos (Texto, Imagen, Video, Objeto3D), Uniones
- **usuarios_db**: Usuarios, Estudiantes, Docentes, Roles, Permisos
- **evaluaciones_db**: Evaluaciones, Preguntas, Opciones, Intentos, Respuestas

Ver `db/README.md` para más detalles sobre la estructura de las bases de datos.



## Scripts Útiles

- `crear_paquetes.py`: Automatiza la creación de la estructura de paquetes
- `instalar_paquetes.sh`: Instala todos los paquetes en orden
- `db/crear_tablas.py`: Crea todas las tablas en las 3 bases de datos
- `db/test_conexiones.py`: Verifica conectividad con las bases de datos

## Licencia

Propiedad de Anibal Cordoba & Zabala

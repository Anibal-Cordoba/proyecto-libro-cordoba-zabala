# Diagrama Visual de Bases de Datos
====================================

## BASE DE DATOS 1: contenido_db

```
┌─────────────────────────────────────┐
│           CAPITULOS                 │
├─────────────────────────────────────┤
│ PK │ id_capitulo      VARCHAR(36)   │
│    │ titulo           VARCHAR(255)  │
│ UQ │ numero           INT            │
│    │ introduccion     TEXT           │
│ IX │ tema             VARCHAR(100)   │
│    │ fecha_creacion   DATETIME       │
│    │ fecha_modificacion DATETIME     │
└─────────────────────────────────────┘
              │ 1
              │
              │ N
┌─────────────▼─────────────────────────────┐
│      UNION_CAPITULO_CONTENIDO             │
├───────────────────────────────────────────┤
│ PK │ id                  INT (AI)         │
│ FK │ id_capitulo         VARCHAR(36) ────┐
│ FK │ id_contenido        VARCHAR(36)     │
│    │ orden               INT              │
└───────────────────────────────────────────┘
              │ N                           │
              │                             │
              │ 1                           │
┌─────────────▼─────────────────────────────┤
│             CONTENIDOS                     │
│         (Single Table Inheritance)         │
├────────────────────────────────────────────┤
│ PK │ id_contenido     VARCHAR(36)         │
│ IX │ tipo             ENUM(texto,imagen,  │
│    │                       video,objeto3d)│
│ IX │ tema             VARCHAR(100)        │
│    │ fecha_creacion   DATETIME            │
│    │ fecha_modificacion DATETIME          │
│    ├──────────────────────────────────────┤
│    │ Campos específicos por tipo:         │
│    │ cuerpo_texto     TEXT (texto)        │
│    │ url_archivo      VARCHAR(500)        │
│    │                  (imagen,video,3d)   │
│    │ formato          VARCHAR(20)         │
│    │                  (imagen,3d)         │
│    │ duracion         FLOAT (video)       │
└────────────────────────────────────────────┘
        ▲         ▲         ▲         ▲
        │         │         │         │
    ┌───┴──┐  ┌──┴───┐  ┌──┴────┐ ┌─┴──────┐
    │Texto │  │Imagen│  │Video  │ │Objeto3D│
    └──────┘  └──────┘  └───────┘ └────────┘
```

---

## BASE DE DATOS 2: usuarios_db

```
┌────────────────────────────────────────┐
│              USUARIOS                  │
├────────────────────────────────────────┤
│ PK │ id_usuario       VARCHAR(36)      │
│ UQ │ email            VARCHAR(255)     │
│ IX │ tipo_usuario     ENUM(estudiante, │
│    │                       docente,    │
│    │                       admin)      │
│    │ password_hash    VARCHAR(255)     │
│    │ nombre           VARCHAR(100)     │
│    │ apellido         VARCHAR(100)     │
│    │ activo           BOOLEAN           │
│    │ email_verificado BOOLEAN           │
│    │ fecha_registro   DATETIME          │
│    │ ultimo_acceso    DATETIME          │
└────────────────────────────────────────┘
       │ 1                  │ 1
       │                    │
       ├────────────┬───────┘
       │ 1          │ 1
       │            │
┌──────▼──────┐ ┌──▼────────────┐
│ ESTUDIANTES │ │   DOCENTES    │
├─────────────┤ ├───────────────┤
│PK│id_estu..│ │PK│id_docente  │
│FK│id_usuario│ │FK│id_usuario  │
│UQ│matricula│ │UQ│num_empleado│
│  │carrera  │ │  │departamento│
│  │nivel    │ │  │titulo_acad.│
│  │semestre │ │  │especialidad│
│  │capitulos│ │  │biografia   │
│  │_completo│ │  │oficina     │
│  │progreso │ │  │tel_ext     │
└─────────────┘ └───────────────┘

┌────────────────────────────────┐
│         USUARIO_ROL            │
│         (N:M)                  │
├────────────────────────────────┤
│ PK,FK │ id_usuario VARCHAR(36)│◄───┐
│ PK,FK │ id_rol     INT        │    │
└────────────────────────────────┘    │
         │ N                          │
         │                            │
         │ 1                          │
┌────────▼─────────────────┐          │
│         ROLES            │          │
├──────────────────────────┤          │
│ PK │ id_rol    INT (AI)  │──────────┘
│    │ nombre    VARCHAR(50)│
│    │ descripcion TEXT     │
│    │ activo    BOOLEAN    │
└──────────────────────────┘
         │ 1
         │
         │ N
┌────────▼─────────────────┐
│       ROL_PERMISO        │
│         (N:M)            │
├──────────────────────────┤
│ PK,FK │ id_rol INT       │
│ PK,FK │ id_permiso INT   │
└──────────────────────────┘
         │ N
         │
         │ 1
┌────────▼─────────────────┐
│        PERMISOS          │
├──────────────────────────┤
│ PK │ id_permiso INT (AI)│
│    │ nombre     VARCHAR │
│    │ descripcion TEXT   │
│    │ recurso    VARCHAR │
│    │ accion     VARCHAR │
└──────────────────────────┘
```

---

## BASE DE DATOS 3: evaluaciones_db

```
┌────────────────────────────────────────┐
│            EVALUACIONES                │
├────────────────────────────────────────┤
│ PK │ id_evaluacion    VARCHAR(36)      │
│ IX │ id_capitulo      VARCHAR(36)      │ (ref a contenido_db)
│ IX │ id_docente_      VARCHAR(36)      │ (ref a usuarios_db)
│    │   creador                          │
│    │ titulo           VARCHAR(255)     │
│    │ descripcion      TEXT              │
│    │ instrucciones    TEXT              │
│    │ duracion_minutos INT               │
│    │ intentos_maximos INT               │
│    │ calif_min_aprob  FLOAT             │
│    │ mostrar_respuestas BOOLEAN         │
│    │ puntos_totales   FLOAT             │
│    │ activa           BOOLEAN           │
│    │ fecha_disponible_desde DATETIME    │
│    │ fecha_disponible_hasta DATETIME    │
└────────────────────────────────────────┘
       │ 1                  │ 1
       │                    │
       │ N                  │ N
┌──────▼──────────┐    ┌────▼─────────────┐
│   PREGUNTAS     │    │    INTENTOS      │
├─────────────────┤    ├──────────────────┤
│PK│id_pregunta  │    │PK│id_intento     │
│FK│id_evaluacion│    │FK│id_evaluacion  │
│  │tipo ENUM    │    │IX│id_estudiante  │ (ref a usuarios_db)
│  │  (opcion_   │    │  │estado ENUM    │
│  │   multiple, │    │  │numero_intento │
│  │   v/f,      │    │  │puntos_        │
│  │   corta,    │    │  │  obtenidos    │
│  │   ensayo)   │    │  │porcentaje     │
│  │enunciado    │    │  │aprobado       │
│  │explicacion  │    │  │fecha_inicio   │
│  │orden        │    │  │fecha_final    │
│  │puntos       │    │  │tiempo_        │
│  │obligatoria  │    │  │  transcurrido │
│  │respuesta_   │    └──────────────────┘
│  │ correcta_txt│          │ 1
└─────────────────┘          │
       │ 1                   │ N
       │                     │
       │ N            ┌──────▼──────────┐
┌──────▼──────────┐  │   RESPUESTAS    │
│    OPCIONES     │  ├─────────────────┤
├─────────────────┤  │PK│id_respuesta  │
│PK│id_opcion    │  │FK│id_intento    │
│FK│id_pregunta  │◄─┼──┤id_pregunta   │
│  │texto        │  │  │id_opcion_    │
│  │es_correcta  │  │  │  seleccionada│
│  │orden        │  │  │respuesta_    │
│  │retroalimen- │  │  │  texto       │
│  │  tacion     │  │  │es_correcta   │
└─────────────────┘  │  │puntos_       │
                     │  │  obtenidos   │
                     │  │retroalimen-  │
                     │  │  tacion_doc  │
                     └─────────────────┘
```

---

## Leyenda

```
PK = Primary Key
FK = Foreign Key
UQ = Unique
IX = Index
AI = Auto Increment

Tipos de relaciones:
  1  = Uno
  N  = Muchos
  │  = Relación
  ◄─ = Referencia
```

---

## Referencias entre Bases de Datos

⚠️ **Nota**: Las referencias entre bases de datos NO son claves foráneas SQL,
sino referencias lógicas a nivel de aplicación.

### De evaluaciones_db → contenido_db
- `evaluaciones.id_capitulo` → `capitulos.id_capitulo`

### De evaluaciones_db → usuarios_db
- `evaluaciones.id_docente_creador` → `usuarios.id_usuario`
- `intentos.id_estudiante` → `usuarios.id_usuario` (estudiante)

### Implementación
Se validan estas referencias en la capa de aplicación (gestores/repositorios).

---

## Índices Compuestos

### contenido_db
- `union_capitulo_contenido(id_capitulo, orden)` - Para ordenamiento eficiente

### evaluaciones_db
- `preguntas(id_evaluacion, orden)` - Para ordenamiento de preguntas
- `intentos(id_estudiante, id_evaluacion)` - Para historial de estudiante

---

## Características de Diseño

### 1. Single Table Inheritance (contenidos)
✅ Una tabla para 4 tipos de contenido
✅ Consultas polimórficas eficientes
✅ Fácil extensión a nuevos tipos

### 2. Soft Deletes
✅ Campos `activo` permiten desactivar sin eliminar
✅ Permite auditoría y recuperación

### 3. Timestamps Automáticos
✅ `fecha_creacion` - Automático al insertar
✅ `fecha_modificacion` - Automático al actualizar

### 4. Enums para Integridad
✅ `tipo_usuario`, `tipo_pregunta`, `estado_intento`
✅ Valida valores a nivel de BD

### 5. Cascadas Configuradas
✅ ON DELETE CASCADE en relaciones padre-hijo
✅ Mantiene integridad referencial

---

## Métricas de Diseño

| BD | Tablas | Columnas | Relaciones | Índices |
|----|--------|----------|------------|---------|
| contenido_db | 3 | 22 | 2 | 4 |
| usuarios_db | 7 | 45 | 6 | 8 |
| evaluaciones_db | 5 | 47 | 5 | 7 |
| **TOTAL** | **15** | **114** | **13** | **19** |

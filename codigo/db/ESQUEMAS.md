# Esquemas de Base de Datos
===========================

Este documento describe las tablas de las 3 bases de datos MySQL en AWS RDS.

## 1. Base de Datos: contenido_db

### Tabla: capitulos
Almacena los capítulos del libro virtual.

```sql
CREATE TABLE capitulos (
    id_capitulo VARCHAR(36) PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    numero INT NOT NULL UNIQUE,
    introduccion TEXT,
    tema VARCHAR(100) NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_tema (tema)
);
```

### Tabla: contenidos
Almacena todos los tipos de contenido (Single Table Inheritance).

```sql
CREATE TABLE contenidos (
    id_contenido VARCHAR(36) PRIMARY KEY,
    tipo ENUM('texto', 'imagen', 'video', 'objeto3d') NOT NULL,
    tema VARCHAR(100) NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Campos específicos por tipo
    cuerpo_texto TEXT,              -- Para tipo 'texto'
    url_archivo VARCHAR(500),       -- Para 'imagen', 'video', 'objeto3d' (URL de S3)
    formato VARCHAR(20),            -- Para 'imagen', 'objeto3d'
    duracion FLOAT,                 -- Para 'video' (en segundos)
    
    INDEX idx_tema (tema),
    INDEX idx_tipo (tipo)
);
```

### Tabla: union_capitulo_contenido
Relación N:M entre capítulos y contenidos con orden.

```sql
CREATE TABLE union_capitulo_contenido (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_capitulo VARCHAR(36) NOT NULL,
    id_contenido VARCHAR(36) NOT NULL,
    orden INT NOT NULL,
    
    FOREIGN KEY (id_capitulo) REFERENCES capitulos(id_capitulo) ON DELETE CASCADE,
    FOREIGN KEY (id_contenido) REFERENCES contenidos(id_contenido) ON DELETE CASCADE,
    INDEX idx_capitulo_orden (id_capitulo, orden),
    INDEX idx_contenido (id_contenido)
);
```

---

## 2. Base de Datos: usuarios_db

### Tabla: usuarios
Información base de todos los usuarios.

```sql
CREATE TABLE usuarios (
    id_usuario VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    tipo_usuario ENUM('estudiante', 'docente', 'administrador') NOT NULL,
    
    activo BOOLEAN DEFAULT TRUE,
    email_verificado BOOLEAN DEFAULT FALSE,
    
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    ultimo_acceso DATETIME,
    fecha_modificacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_email (email),
    INDEX idx_tipo (tipo_usuario)
);
```

### Tabla: estudiantes
Información específica de estudiantes.

```sql
CREATE TABLE estudiantes (
    id_estudiante VARCHAR(36) PRIMARY KEY,
    id_usuario VARCHAR(36) UNIQUE NOT NULL,
    
    matricula VARCHAR(50) UNIQUE,
    carrera VARCHAR(200),
    nivel VARCHAR(50),
    semestre INT,
    
    capitulos_completados INT DEFAULT 0,
    tiempo_estudio_total INT DEFAULT 0,
    ultimo_capitulo_visto VARCHAR(36),
    progreso_general INT DEFAULT 0,
    
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    INDEX idx_matricula (matricula)
);
```

### Tabla: docentes
Información específica de docentes.

```sql
CREATE TABLE docentes (
    id_docente VARCHAR(36) PRIMARY KEY,
    id_usuario VARCHAR(36) UNIQUE NOT NULL,
    
    numero_empleado VARCHAR(50) UNIQUE,
    departamento VARCHAR(200),
    titulo_academico VARCHAR(100),
    especialidad VARCHAR(200),
    
    biografia TEXT,
    oficina VARCHAR(100),
    telefono_extension VARCHAR(20),
    horario_atencion TEXT,
    
    capitulos_creados INT DEFAULT 0,
    evaluaciones_creadas INT DEFAULT 0,
    
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    INDEX idx_numero_empleado (numero_empleado)
);
```

### Tabla: roles
Define los roles del sistema.

```sql
CREATE TABLE roles (
    id_rol INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Tabla: permisos
Define los permisos granulares.

```sql
CREATE TABLE permisos (
    id_permiso INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT,
    recurso VARCHAR(50) NOT NULL,
    accion VARCHAR(50) NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Tabla: usuario_rol
Asociación N:M entre usuarios y roles.

```sql
CREATE TABLE usuario_rol (
    id_usuario VARCHAR(36) NOT NULL,
    id_rol INT NOT NULL,
    
    PRIMARY KEY (id_usuario, id_rol),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_rol) REFERENCES roles(id_rol) ON DELETE CASCADE
);
```

### Tabla: rol_permiso
Asociación N:M entre roles y permisos.

```sql
CREATE TABLE rol_permiso (
    id_rol INT NOT NULL,
    id_permiso INT NOT NULL,
    
    PRIMARY KEY (id_rol, id_permiso),
    FOREIGN KEY (id_rol) REFERENCES roles(id_rol) ON DELETE CASCADE,
    FOREIGN KEY (id_permiso) REFERENCES permisos(id_permiso) ON DELETE CASCADE
);
```

---

## 3. Base de Datos: evaluaciones_db

### Tabla: evaluaciones
Define las evaluaciones asociadas a capítulos.

```sql
CREATE TABLE evaluaciones (
    id_evaluacion VARCHAR(36) PRIMARY KEY,
    id_capitulo VARCHAR(36) NOT NULL,
    
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    instrucciones TEXT,
    
    duracion_minutos INT,
    intentos_maximos INT DEFAULT 1,
    calificacion_minima_aprobacion FLOAT DEFAULT 60.0,
    mostrar_respuestas_correctas BOOLEAN DEFAULT TRUE,
    
    puntos_totales FLOAT DEFAULT 100.0,
    activa BOOLEAN DEFAULT TRUE,
    
    id_docente_creador VARCHAR(36) NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    fecha_disponible_desde DATETIME,
    fecha_disponible_hasta DATETIME,
    
    INDEX idx_capitulo (id_capitulo),
    INDEX idx_docente (id_docente_creador)
);
```

### Tabla: preguntas
Preguntas de una evaluación.

```sql
CREATE TABLE preguntas (
    id_pregunta VARCHAR(36) PRIMARY KEY,
    id_evaluacion VARCHAR(36) NOT NULL,
    
    tipo ENUM('opcion_multiple', 'verdadero_falso', 'respuesta_corta', 'ensayo') NOT NULL,
    enunciado TEXT NOT NULL,
    explicacion TEXT,
    
    orden INT NOT NULL,
    puntos FLOAT DEFAULT 1.0,
    obligatoria BOOLEAN DEFAULT TRUE,
    
    respuesta_correcta_texto TEXT,
    
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_evaluacion) REFERENCES evaluaciones(id_evaluacion) ON DELETE CASCADE,
    INDEX idx_evaluacion_orden (id_evaluacion, orden)
);
```

### Tabla: opciones
Opciones de respuesta para preguntas de opción múltiple.

```sql
CREATE TABLE opciones (
    id_opcion VARCHAR(36) PRIMARY KEY,
    id_pregunta VARCHAR(36) NOT NULL,
    
    texto TEXT NOT NULL,
    es_correcta BOOLEAN DEFAULT FALSE,
    orden INT NOT NULL,
    retroalimentacion TEXT,
    
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_pregunta) REFERENCES preguntas(id_pregunta) ON DELETE CASCADE,
    INDEX idx_pregunta (id_pregunta)
);
```

### Tabla: intentos
Registra los intentos de evaluación de los estudiantes.

```sql
CREATE TABLE intentos (
    id_intento VARCHAR(36) PRIMARY KEY,
    id_evaluacion VARCHAR(36) NOT NULL,
    id_estudiante VARCHAR(36) NOT NULL,
    
    estado ENUM('en_progreso', 'completado', 'abandonado') DEFAULT 'en_progreso',
    numero_intento INT NOT NULL,
    
    puntos_obtenidos FLOAT DEFAULT 0.0,
    puntos_totales FLOAT NOT NULL,
    porcentaje FLOAT DEFAULT 0.0,
    aprobado BOOLEAN DEFAULT FALSE,
    
    fecha_inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_finalizacion DATETIME,
    tiempo_transcurrido_segundos INT DEFAULT 0,
    
    FOREIGN KEY (id_evaluacion) REFERENCES evaluaciones(id_evaluacion) ON DELETE CASCADE,
    INDEX idx_estudiante (id_estudiante),
    INDEX idx_evaluacion (id_evaluacion)
);
```

### Tabla: respuestas
Respuestas individuales del estudiante a cada pregunta.

```sql
CREATE TABLE respuestas (
    id_respuesta VARCHAR(36) PRIMARY KEY,
    id_intento VARCHAR(36) NOT NULL,
    id_pregunta VARCHAR(36) NOT NULL,
    
    id_opcion_seleccionada VARCHAR(36),
    respuesta_texto TEXT,
    
    es_correcta BOOLEAN,
    puntos_obtenidos FLOAT DEFAULT 0.0,
    
    retroalimentacion_docente TEXT,
    
    fecha_respuesta DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_intento) REFERENCES intentos(id_intento) ON DELETE CASCADE,
    FOREIGN KEY (id_pregunta) REFERENCES preguntas(id_pregunta) ON DELETE CASCADE,
    INDEX idx_intento (id_intento)
);
```

---

## Diagrama Entidad-Relación Resumido

### Base de Datos: contenido_db
```
capitulos (1) ←→ (N) union_capitulo_contenido (N) ←→ (1) contenidos
```

### Base de Datos: usuarios_db
```
usuarios (1) ←→ (1) estudiantes
usuarios (1) ←→ (1) docentes
usuarios (N) ←→ (N) roles ←→ (N) permisos
```

### Base de Datos: evaluaciones_db
```
evaluaciones (1) ←→ (N) preguntas (1) ←→ (N) opciones
evaluaciones (1) ←→ (N) intentos (1) ←→ (N) respuestas (N) ←→ (1) preguntas
```

---

## Notas de Implementación

1. **UUIDs**: Se usan VARCHAR(36) para IDs generados con UUID v4
2. **Timestamps**: Todas las tablas tienen campos de auditoría (fecha_creacion, fecha_modificacion)
3. **Soft Delete**: Campos `activo` permiten desactivar sin eliminar
4. **Índices**: Se crean índices en campos de búsqueda frecuente
5. **Cascadas**: ON DELETE CASCADE para mantener integridad referencial
6. **Charset**: Se recomienda utf8mb4 para soporte de emojis y caracteres especiales

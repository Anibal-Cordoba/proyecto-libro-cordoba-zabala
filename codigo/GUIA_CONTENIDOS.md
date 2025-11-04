# 📚 Sistema de Gestión de Contenidos - Guía de Uso

## 🎯 Descripción General

El sistema ahora incluye funcionalidad completa para crear y gestionar **contenidos** que se pueden asociar a los capítulos. Estos contenidos son los bloques de texto e imágenes (y más) que componen cada capítulo del libro.

## 📋 Tipos de Contenido Disponibles

### 1. 📝 Texto
Bloques de texto que contienen información, explicaciones, definiciones, etc.

**Campos:**
- `tema`: Tema del contenido (ej: "Células", "Fotosíntesis")
- `cuerpo_texto`: El contenido textual completo

**Ejemplo:**
```json
{
  "tipo": "texto",
  "tema": "Células eucariotas",
  "cuerpo_texto": "Las células eucariotas son células que tienen un núcleo definido..."
}
```

### 2. 🖼️ Imagen
Imágenes, diagramas, fotografías, ilustraciones.

**Campos:**
- `tema`: Tema de la imagen
- `url_archivo`: URL donde está alojada la imagen
- `formato`: Formato del archivo (jpg, png, gif, webp, svg)

**Ejemplo:**
```json
{
  "tipo": "imagen",
  "tema": "Estructura celular",
  "url_archivo": "https://ejemplo.com/celula.png",
  "formato": "png"
}
```

### 3. 🎥 Video
Videos educativos, animaciones, explicaciones audiovisuales.

**Campos:**
- `tema`: Tema del video
- `url_archivo`: URL del video
- `formato`: Formato (mp4, webm, ogg, mov)
- `duracion`: Duración en segundos (opcional)

**Ejemplo:**
```json
{
  "tipo": "video",
  "tema": "Mitosis celular",
  "url_archivo": "https://ejemplo.com/mitosis.mp4",
  "formato": "mp4",
  "duracion": 180
}
```

### 4. 🎨 Objeto 3D
Modelos tridimensionales interactivos (moléculas, organelas, etc.).

**Campos:**
- `tema`: Tema del modelo
- `url_archivo`: URL del archivo 3D
- `formato`: Formato (obj, fbx, gltf, glb)

**Ejemplo:**
```json
{
  "tipo": "objeto3d",
  "tema": "Molécula de ADN",
  "url_archivo": "https://ejemplo.com/adn.glb",
  "formato": "glb"
}
```

---

## 🌐 Interfaces Web Disponibles

### 1. Página Principal
**URL:** `http://localhost:8000/`

Pantalla de inicio con acceso a todas las funcionalidades:
- ➕ Crear Capítulo
- 📖 Ver Capítulos  
- 📝 Gestionar Contenidos

### 2. Gestionar Contenidos
**URL:** `http://localhost:8000/gestionar-contenidos`

Interfaz completa para:
- ✅ Crear nuevos contenidos (texto, imagen, video, objeto3D)
- 📋 Ver lista de todos los contenidos creados
- 🔍 Filtrar contenidos por tipo
- 🗑️ Eliminar contenidos
- ➕ Asignar contenidos a capítulos

**Características:**
- Formulario dinámico que cambia según el tipo de contenido seleccionado
- Vista en tiempo real de todos los contenidos
- Filtros por tipo de contenido
- Asignación directa a capítulos con orden personalizado

---

## 🚀 API REST - Endpoints de Contenidos

### Crear Contenido
```
POST /api/contenidos/
```

**Body (Texto):**
```json
{
  "tipo": "texto",
  "tema": "Fotosíntesis",
  "cuerpo_texto": "La fotosíntesis es el proceso..."
}
```

**Respuesta:**
```json
{
  "id_contenido": "uuid-generado",
  "tipo": "texto",
  "tema": "Fotosíntesis",
  "cuerpo_texto": "La fotosíntesis es el proceso...",
  "fecha_creacion": "2025-11-04T10:00:00",
  "fecha_modificacion": "2025-11-04T10:00:00"
}
```

### Listar Contenidos
```
GET /api/contenidos/
GET /api/contenidos/?tipo=texto
GET /api/contenidos/?tema=celula
GET /api/contenidos/?skip=0&limit=50
```

**Respuesta:**
```json
[
  {
    "id_contenido": "uuid-1",
    "tipo": "texto",
    "tema": "Células",
    ...
  },
  {
    "id_contenido": "uuid-2",
    "tipo": "imagen",
    "tema": "Mitosis",
    ...
  }
]
```

### Obtener un Contenido
```
GET /api/contenidos/{id_contenido}
```

### Eliminar Contenido
```
DELETE /api/contenidos/{id_contenido}
```

### Asignar Contenido a Capítulo
```
POST /api/contenidos/asignar?id_capitulo={id}&id_contenido={id}&orden={num}
```

**Parámetros:**
- `id_capitulo`: UUID del capítulo
- `id_contenido`: UUID del contenido
- `orden`: Número de orden (posición en el capítulo)

**Ejemplo:**
```
POST /api/contenidos/asignar?id_capitulo=abc-123&id_contenido=def-456&orden=1
```

**Respuesta:**
```json
{
  "message": "Contenido asignado exitosamente",
  "id": 1,
  "id_capitulo": "abc-123",
  "id_contenido": "def-456",
  "orden": 1
}
```

### Listar Contenidos de un Capítulo
```
GET /api/contenidos/capitulo/{id_capitulo}
```

Devuelve todos los contenidos asignados a un capítulo, **ordenados** por el campo `orden`.

### Desasignar Contenido de Capítulo
```
DELETE /api/contenidos/desasignar/{id_capitulo}/{id_contenido}
```

---

## 📊 Flujo de Trabajo Típico

### 1. Crear un Capítulo
1. Ir a `/crear-capitulo`
2. Completar: número, título, introducción, tema, estado
3. Guardar → Obtienes un `id_capitulo`

### 2. Crear Contenidos para el Capítulo
1. Ir a `/gestionar-contenidos`
2. Seleccionar tipo de contenido (texto, imagen, etc.)
3. Completar los campos específicos
4. Crear múltiples contenidos

### 3. Asignar Contenidos al Capítulo
**Opción A - Desde la interfaz web:**
1. En `/gestionar-contenidos`, clic en "➕ Asignar a Capítulo"
2. Ingresar el `id_capitulo`
3. Ingresar el orden (1, 2, 3...)

**Opción B - Mediante API:**
```bash
curl -X POST "http://localhost:8000/api/contenidos/asignar?id_capitulo=abc-123&id_contenido=def-456&orden=1"
```

### 4. Ver el Capítulo con sus Contenidos
```bash
curl "http://localhost:8000/api/contenidos/capitulo/abc-123"
```

Esto devuelve todos los contenidos en orden.

---

## 🔍 Ejemplos Prácticos

### Crear un capítulo sobre células con múltiples contenidos:

1. **Crear el capítulo**
```json
POST /api/capitulos/
{
  "numero": 1,
  "titulo": "La Célula",
  "introduccion": "Unidad básica de la vida",
  "tema": "Biología Celular",
  "estado": "PUBLICADO"
}
```
→ Obtienes `id_capitulo = "cap-001"`

2. **Crear bloque de texto introductorio**
```json
POST /api/contenidos/
{
  "tipo": "texto",
  "tema": "Introducción a las células",
  "cuerpo_texto": "Las células son las unidades fundamentales de todos los seres vivos..."
}
```
→ Obtienes `id_contenido = "txt-001"`

3. **Crear imagen de célula**
```json
POST /api/contenidos/
{
  "tipo": "imagen",
  "tema": "Estructura celular",
  "url_archivo": "https://ejemplo.com/celula.png",
  "formato": "png"
}
```
→ Obtienes `id_contenido = "img-001"`

4. **Crear más texto explicativo**
```json
POST /api/contenidos/
{
  "tipo": "texto",
  "tema": "Tipos de células",
  "cuerpo_texto": "Existen dos tipos principales: procariotas y eucariotas..."
}
```
→ Obtienes `id_contenido = "txt-002"`

5. **Asignar contenidos al capítulo en orden**
```bash
# Texto introductorio (orden 1)
POST /api/contenidos/asignar?id_capitulo=cap-001&id_contenido=txt-001&orden=1

# Imagen (orden 2)
POST /api/contenidos/asignar?id_capitulo=cap-001&id_contenido=img-001&orden=2

# Texto explicativo (orden 3)
POST /api/contenidos/asignar?id_capitulo=cap-001&id_contenido=txt-002&orden=3
```

6. **Recuperar el capítulo completo**
```bash
# Datos del capítulo
GET /api/capitulos/cap-001

# Contenidos ordenados
GET /api/contenidos/capitulo/cap-001
```

---

## 📁 Estructura de Base de Datos

### Tabla: `contenidos`
```sql
- id_contenido (PK, UUID)
- tipo (texto|imagen|video|objeto3d)
- tema (string)
- fecha_creacion
- fecha_modificacion
- cuerpo_texto (para tipo=texto)
- url_archivo (para imagen/video/objeto3d)
- formato (para imagen/objeto3d/video)
- duracion (para video, en segundos)
```

### Tabla: `union_capitulo_contenido`
```sql
- id (PK, autoincrement)
- id_capitulo (FK → capitulos)
- id_contenido (FK → contenidos)
- orden (integer)
```

Esta tabla de unión permite:
- ✅ Un contenido puede estar en múltiples capítulos
- ✅ Un capítulo puede tener múltiples contenidos
- ✅ El orden de los contenidos se controla explícitamente
- ✅ CASCADE DELETE: al eliminar capítulo o contenido, se limpian las relaciones

---

## 🎨 Validaciones Implementadas

### Para Texto:
- ✅ `cuerpo_texto` es obligatorio
- ✅ No puede estar vacío

### Para Imagen:
- ✅ `url_archivo` y `formato` son obligatorios
- ✅ Formato debe ser: jpg, jpeg, png, gif, webp, svg

### Para Video:
- ✅ `url_archivo` es obligatorio
- ✅ Formato debe ser: mp4, webm, ogg, mov
- ✅ Duración debe ser > 0 (si se proporciona)

### Para Objeto 3D:
- ✅ `url_archivo` y `formato` son obligatorios
- ✅ Formato debe ser: obj, fbx, gltf, glb

---

## 🚦 Códigos de Estado HTTP

- **201 Created**: Contenido creado exitosamente
- **200 OK**: Operación exitosa (GET, asignación)
- **204 No Content**: Eliminación exitosa
- **400 Bad Request**: Datos inválidos o campos faltantes
- **404 Not Found**: Contenido o capítulo no encontrado

---

## 📚 Documentación Interactiva

Accede a la documentación completa con ejemplos interactivos en:

**Swagger UI:** `http://localhost:8000/docs`
- Prueba todos los endpoints
- Ve los schemas de datos
- Ejecuta peticiones directamente

**ReDoc:** `http://localhost:8000/redoc`
- Documentación alternativa
- Vista más detallada

---

## 💡 Tips y Mejores Prácticas

1. **Orden de contenidos**: Usa números con espacio (10, 20, 30) en lugar de (1, 2, 3) para poder insertar elementos entre medias después.

2. **URLs de archivos**: Asegúrate de que las URLs sean públicamente accesibles y permanentes.

3. **Reutilización**: Un mismo contenido (por ejemplo, una imagen de ADN) puede usarse en múltiples capítulos sin duplicar.

4. **Temas coherentes**: Usa nombres de temas consistentes para facilitar búsquedas y filtros.

5. **Formato de imágenes**: Usa WebP o PNG para mejor calidad/tamaño.

6. **Videos**: Considera usar servicios de streaming (YouTube, Vimeo) para mejor performance.

---

## 🔧 Próximas Mejoras Sugeridas

- [ ] Upload directo de archivos (en vez de URLs)
- [ ] Editor de texto enriquecido (Markdown/HTML)
- [ ] Preview de imágenes y videos
- [ ] Viewer 3D integrado
- [ ] Reordenamiento drag-and-drop
- [ ] Búsqueda de contenidos por texto completo
- [ ] Versionado de contenidos
- [ ] Caché de URLs externas

---

## 📞 Soporte

Para más información o problemas, consulta:
- Documentación API: http://localhost:8000/docs
- Logs del servidor: Terminal donde corre uvicorn
- Base de datos: `codigo/data/contenido.db`

---

**Sistema de Libro Interactivo v2.0**  
Desarrollado por: Anibal Cordoba & Matias Zabala  
Fecha: Noviembre 2025

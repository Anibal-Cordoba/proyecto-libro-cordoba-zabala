## 🚀 API REST con FastAPI

Esta API proporciona una interfaz web y REST para gestionar capítulos del libro interactivo.

### Características

- ✅ Interfaz web visual con HTML/CSS
- ✅ API REST completa (CRUD de capítulos)
- ✅ Integración con paquetes instalados
- ✅ Validación con Pydantic
- ✅ Documentación automática (Swagger)

### Iniciar la API

```bash
cd codigo
bash iniciar_api.sh
```

La API estará disponible en: **http://localhost:8000**

### Páginas Web

- **http://localhost:8000** - Página principal con botones
- **http://localhost:8000/crear-capitulo** - Formulario para crear capítulo
- **http://localhost:8000/ver-capitulos** - Lista de capítulos

### Documentación API

- **http://localhost:8000/docs** - Swagger UI (interactiva)
- **http://localhost:8000/redoc** - ReDoc (alternativa)

### Endpoints API

#### Capítulos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/capitulos/` | Crear capítulo |
| `GET` | `/api/capitulos/` | Listar capítulos |
| `GET` | `/api/capitulos/{id}` | Obtener capítulo |
| `PUT` | `/api/capitulos/{id}` | Actualizar capítulo |
| `DELETE` | `/api/capitulos/{id}` | Eliminar capítulo |

#### Ejemplo: Crear Capítulo

```bash
curl -X POST "http://localhost:8000/api/capitulos/" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Introducción a la Célula",
    "numero": 1,
    "tema": "Biología Celular",
    "introduccion": "Este capítulo introduce los conceptos básicos..."
  }'
```

#### Ejemplo: Listar Capítulos

```bash
curl "http://localhost:8000/api/capitulos/"
```

### Configuración

1. Copia `.env.example` a `.env`:
```bash
cp .env.example .env
```

2. Edita `.env` con tus credenciales de base de datos:
```bash
DATABASE_URL_CONTENIDO=mysql+pymysql://user:pass@host:3306/contenido_db
```

3. Asegúrate de que las tablas existan:
```bash
python db/crear_tablas.py
```

### Estructura de la API

```
api/
├── main.py                 # Aplicación principal FastAPI
├── dependencies.py         # Dependencias (DB session)
├── routers/
│   ├── __init__.py
│   └── capitulos.py       # Endpoints de capítulos
├── schemas/
│   ├── __init__.py
│   ├── capitulo.py        # Schemas Pydantic
│   └── contenido.py
├── templates/
│   ├── index.html         # Página principal
│   ├── crear_capitulo.html
│   └── ver_capitulos.html
└── static/                # CSS, JS, imágenes
```

### Desarrollo

Para desarrollo con recarga automática:

```bash
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Próximas Características

- [ ] Endpoints para contenidos (texto, imagen, video, objeto3D)
- [ ] Asociar contenidos a capítulos
- [ ] Autenticación JWT
- [ ] Paginación
- [ ] Filtros avanzados
- [ ] Upload de archivos a S3

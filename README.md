# 📚 Libro Interactivo para la Enseñanza de Biología

> Sistema web interactivo para la enseñanza y aprendizaje de biología mediante recursos visuales y actividades multimedia.

## 🎯 Descripción

Plataforma web que funciona como libro virtual didáctico de biología, mejorando la comprensión de conceptos complejos mediante:
- 📖 **Capítulos estructurados** con contenido organizado
- 🖼️ **Recursos multimedia** (textos, imágenes, videos, modelos 3D)
- 🎨 **Visualización interactiva** con interfaz expandible
- 🔄 **Gestión dinámica** de contenidos educativos

## ✨ Estado del Proyecto: **Funcional y Operativo** ✅

- ✅ API REST completa con FastAPI
- ✅ Interfaz web para gestión de contenidos
- ✅ Sistema de 4 tipos de contenidos multimedia
- ✅ Base de datos SQLite configurada
- ✅ 115 tests automatizados implementados

## 👥 Equipo

- **Aníbal Córdoba** - Responsable del Repositorio
- **Matías Zabala** - Colaborador

## 📁 Estructura del Repositorio

```
proyecto-libro-cordoba-zabala/
├── documentacion/          # Documentos de requerimientos y especificaciones
├── diseño/                 # Diagramas, mockups y arquitectura
├── codigo/                 # 🚀 Código fuente del sistema (PRINCIPAL)
│   ├── api/                # API REST FastAPI (routers + schemas)
│   ├── paquetes/           # 📦 Paquetes modulares instalables
│   │   ├── gestor_capitulo/      # Lógica de negocio de capítulos
│   │   ├── gestor_contenido/     # Lógica de negocio de contenidos
│   │   └── modelo_*/             # Modelos ORM y repositorios
│   ├── db/                 # Configuración de base de datos
│   ├── tests/              # Tests automatizados (115 tests)
│   ├── data/               # Base de datos SQLite
│   └── README.md           # 📖 Documentación completa del sistema
└── recursos/               # Imágenes, plantillas y recursos
```

## 🚀 Inicio Rápido

### 1. Navega al directorio de código

```bash
cd codigo
```

### 2. Instala dependencias (si no lo has hecho)

```bash
# Dependencias externas (FastAPI, SQLAlchemy, etc.)
pip install -r requirements.txt

# Paquetes modulares del proyecto (gestores, modelos, repositorios)
./instalar_paquetes.sh
```

### 3. Inicia el servidor

```bash
./iniciar_api_final.sh
```

### 4. Accede a la aplicación

- 🌐 **Aplicación Web**: http://localhost:8000
- 📚 **Documentación API**: http://localhost:8000/docs
- 🔍 **Health Check**: http://localhost:8000/health

## 📖 Documentación Completa

**➡️ [Ver codigo/README.md](codigo/README.md)** para:
- 📋 Guía completa de instalación y uso
- 🎯 Descripción de características
- 📦 **Arquitectura de paquetes modulares** (NUEVO)
- 🌐 Documentación de API REST
- 🧪 Información sobre tests
- 🗄️ Configuración de base de datos
- 💻 Ejemplos de uso avanzado

**➡️ [Ver codigo/GUIA_CONTENIDOS.md](codigo/GUIA_CONTENIDOS.md)** para:
- 📝 Guía del sistema de contenidos
- 🔗 Flujo de trabajo completo
- 📊 Estructura de datos

**➡️ [Ver documentacion/](documentacion/)** para:
- 📄 Informes del proyecto
- 📊 Presentaciones
- 📋 Especificaciones y requerimientos

**➡️ [Ver diseño/arquitectura/](diseño/arquitectura/)** para:
- 🏗️ Diagramas de arquitectura del sistema
- 📐 Diseño técnico y patrones utilizados
- 🔄 Flujos y estructura del proyecto

## 🎨 Funcionalidades Principales

### Gestión de Capítulos
- ✅ Crear, editar y eliminar capítulos
- ✅ Organizar por número y tema
- ✅ Estados: BORRADOR, PUBLICADO, ARCHIVADO
- ✅ Vista expandible con contenidos asociados

### Gestión de Contenidos (4 Tipos)
1. **📝 Texto**: Contenido textual con formato (plain, markdown, html)
2. **🖼️ Imagen**: Imágenes con URL y formato
3. **🎥 Video**: Videos con duración y URL
4. **🎨 Objeto 3D**: Modelos 3D interactivos

### Sistema de Asignación
- ✅ Asignar múltiples contenidos a capítulos
- ✅ Ordenar contenidos dentro de cada capítulo
- ✅ Vista integrada capítulo + contenidos

## 🗄️ Base de Datos

- **Desarrollo**: SQLite (configuración por defecto)
- **Producción**: Soporte para MySQL
- **Tablas**: capitulos, contenidos, union_capitulo_contenido

## 🧪 Testing

- **115 tests** implementados
- Cobertura de endpoints de capítulos
- Tests de modelos ORM
- Ver `codigo/testing/` para documentación completa

## 📊 Elementos de Configuración

- Documentación: Requerimientos y especificaciones
- Diseño: 8 CIs (Diagramas y arquitectura)
- Código: Sistema completo funcional
- Recursos: Plantillas y recursos visuales

## 🔧 Scripts Principales

```bash
cd codigo

# Iniciar servidor
./iniciar_api_final.sh

# Inicializar/recrear base de datos
python inicializar_db.py

# Limpiar datos
python limpiar_db.py

# Ejecutar tests
./ejecutar_tests.sh all
```

## 📱 Capturas de Pantalla

La interfaz web incluye:
- 🏠 Página principal con navegación
- ➕ Formulario de creación de capítulos
- 📖 Vista de capítulos con contenidos expandibles (click to expand)
- 📚 Gestión completa de contenidos con selector por tipo

## 🐛 Solución de Problemas

Ver la sección "Solución de Problemas" en [codigo/README.md](codigo/README.md) para ayuda con errores comunes.

## 📅 Última Actualización

**[04/11/2025]** - v3.0 - Sistema de contenidos multimedia completo
- ✅ API REST con 15 endpoints
- ✅ Sistema de 4 tipos de contenidos
- ✅ Interfaz web completamente funcional
- ✅ Vista expandible de capítulos con contenidos
- ✅ Base de datos SQLite operativa

---

**🚀 Para comenzar, ve a [codigo/README.md](codigo/README.md)**

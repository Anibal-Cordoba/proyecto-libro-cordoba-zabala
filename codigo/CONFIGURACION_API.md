# Guía de Configuración para la API

## 📋 Pasos para Configurar

### 1️⃣ Configurar Base de Datos

Edita el archivo `.env` con tus credenciales reales de MySQL:

```bash
nano .env
```

Cambia esta línea:
```bash
# ANTES (ejemplo genérico)
DATABASE_URL_CONTENIDO=mysql+pymysql://usuario:password@localhost:3306/contenido_db

# DESPUÉS (tus credenciales reales)
DATABASE_URL_CONTENIDO=mysql+pymysql://root:tu_password_real@localhost:3306/contenido_db
```

### 2️⃣ Crear Base de Datos

Si la base de datos `contenido_db` no existe, créala:

```bash
mysql -u root -p
```

Luego en MySQL:
```sql
CREATE DATABASE contenido_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 3️⃣ Crear Tablas

Ejecuta el script que crea las tablas:

```bash
python db/crear_tablas.py
```

### 4️⃣ Verificar Configuración

Ejecuta el script de verificación:

```bash
python verificar_configuracion.py
```

Deberías ver:
```
✅ TODO LISTO - PUEDES INICIAR LA API
```

### 5️⃣ Iniciar la API

```bash
bash iniciar_api.sh
```

## 🐛 Solución de Problemas

### Problema: "Can't connect to MySQL server"

**Causa**: MySQL no está corriendo o credenciales incorrectas.

**Solución**:
```bash
# Verificar si MySQL está corriendo
sudo systemctl status mysql

# Si no está corriendo, iniciarlo
sudo systemctl start mysql

# Verificar credenciales
mysql -u root -p
```

### Problema: "Database 'contenido_db' doesn't exist"

**Causa**: La base de datos no fue creada.

**Solución**:
```bash
mysql -u root -p -e "CREATE DATABASE contenido_db;"
```

### Problema: "Faltan tablas"

**Causa**: Las tablas no fueron creadas.

**Solución**:
```bash
python db/crear_tablas.py
```

### Problema: "Faltan paquetes"

**Causa**: Los paquetes no están instalados.

**Solución**:
```bash
bash instalar_paquetes.sh
```

## ✅ Checklist Completo

- [ ] Archivo `.env` creado y configurado con credenciales reales
- [ ] MySQL está corriendo
- [ ] Base de datos `contenido_db` existe
- [ ] Tablas creadas (`capitulos`, `contenidos`, `union_capitulo_contenido`)
- [ ] 12 paquetes instalados
- [ ] FastAPI y dependencias instaladas
- [ ] Script `verificar_configuracion.py` pasa todas las pruebas

## 🚀 Una vez todo esté listo

```bash
# Iniciar la API
bash iniciar_api.sh

# Visitar en el navegador
# http://localhost:8000
```

## 📝 Ejemplo de .env Configurado

```bash
# Base de datos local
DATABASE_URL_CONTENIDO=mysql+pymysql://root:mipassword@localhost:3306/contenido_db

# O para AWS RDS
DATABASE_URL_CONTENIDO=mysql+pymysql://admin:password@mi-rds.us-east-1.rds.amazonaws.com:3306/contenido_db
```

"""
API REST con FastAPI para el Sistema de Libro Interactivo
===========================================================
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
from pathlib import Path

# Agregar el directorio padre al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.routers.capitulos import router as capitulos_router

# Crear aplicación FastAPI
app = FastAPI(
    title="Libro Interactivo API",
    description="API REST para gestión de capítulos y contenidos de biología",
    version="2.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar templates (usar path absoluto)
template_dir = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(template_dir))

# Incluir routers de API
app.include_router(capitulos_router, prefix="/api")

# Ruta principal - Página de inicio
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Página principal con botones"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/crear-capitulo", response_class=HTMLResponse)
async def crear_capitulo_page(request: Request):
    """Página para crear capítulo"""
    return templates.TemplateResponse("crear_capitulo.html", {"request": request})


@app.get("/ver-capitulos", response_class=HTMLResponse)
async def ver_capitulos_page(request: Request):
    """Página para ver capítulos"""
    return templates.TemplateResponse("ver_capitulos.html", {"request": request})


@app.get("/health")
async def health_check():
    """Endpoint de salud"""
    return {"status": "ok", "version": "2.0.0"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

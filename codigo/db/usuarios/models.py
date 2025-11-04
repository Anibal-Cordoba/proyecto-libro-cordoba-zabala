"""
Modelos SQLAlchemy para la Base de Datos de Usuarios
=====================================================
Tablas: usuarios, estudiantes, docentes, roles, permisos, usuario_rol
"""

from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Table, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import BaseUsuarios


# Tabla de asociación N:M entre Usuario y Rol
usuario_rol = Table(
    'usuario_rol',
    BaseUsuarios.metadata,
    Column('id_usuario', String(36), ForeignKey('usuarios.id_usuario', ondelete='CASCADE'), primary_key=True),
    Column('id_rol', Integer, ForeignKey('roles.id_rol', ondelete='CASCADE'), primary_key=True)
)


# Tabla de asociación N:M entre Rol y Permiso
rol_permiso = Table(
    'rol_permiso',
    BaseUsuarios.metadata,
    Column('id_rol', Integer, ForeignKey('roles.id_rol', ondelete='CASCADE'), primary_key=True),
    Column('id_permiso', Integer, ForeignKey('permisos.id_permiso', ondelete='CASCADE'), primary_key=True)
)


class TipoUsuario(enum.Enum):
    """Enum para tipos de usuario."""
    ESTUDIANTE = "estudiante"
    DOCENTE = "docente"
    ADMINISTRADOR = "administrador"


class Usuario(BaseUsuarios):
    """
    Tabla: usuarios
    Información base de todos los usuarios del sistema.
    """
    __tablename__ = 'usuarios'
    
    id_usuario = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)  # Hash bcrypt
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    tipo_usuario = Column(SQLEnum(TipoUsuario), nullable=False)
    
    activo = Column(Boolean, default=True)
    email_verificado = Column(Boolean, default=False)
    
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    ultimo_acceso = Column(DateTime, nullable=True)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    roles = relationship("Rol", secondary=usuario_rol, back_populates="usuarios")
    estudiante = relationship("Estudiante", back_populates="usuario", uselist=False, cascade="all, delete-orphan")
    docente = relationship("Docente", back_populates="usuario", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Usuario(id={self.id_usuario}, email='{self.email}', tipo='{self.tipo_usuario.value}')>"


class Estudiante(BaseUsuarios):
    """
    Tabla: estudiantes
    Información específica de estudiantes.
    """
    __tablename__ = 'estudiantes'
    
    id_estudiante = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_usuario = Column(String(36), ForeignKey('usuarios.id_usuario', ondelete='CASCADE'), unique=True, nullable=False)
    
    # Datos académicos
    matricula = Column(String(50), unique=True, nullable=True)
    carrera = Column(String(200), nullable=True)
    nivel = Column(String(50), nullable=True)  # Ej: "Licenciatura", "Maestría"
    semestre = Column(Integer, nullable=True)
    
    # Estadísticas de uso
    capitulos_completados = Column(Integer, default=0)
    tiempo_estudio_total = Column(Integer, default=0)  # En minutos
    ultimo_capitulo_visto = Column(String(36), nullable=True)  # ID del capítulo
    progreso_general = Column(Integer, default=0)  # Porcentaje 0-100
    
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="estudiante")
    
    def __repr__(self):
        return f"<Estudiante(id={self.id_estudiante}, matricula='{self.matricula}', progreso={self.progreso_general}%)>"


class Docente(BaseUsuarios):
    """
    Tabla: docentes
    Información específica de docentes.
    """
    __tablename__ = 'docentes'
    
    id_docente = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_usuario = Column(String(36), ForeignKey('usuarios.id_usuario', ondelete='CASCADE'), unique=True, nullable=False)
    
    # Datos profesionales
    numero_empleado = Column(String(50), unique=True, nullable=True)
    departamento = Column(String(200), nullable=True)
    titulo_academico = Column(String(100), nullable=True)  # Ej: "Dr.", "M.C.", "Ing."
    especialidad = Column(String(200), nullable=True)
    
    # Información adicional
    biografia = Column(Text, nullable=True)
    oficina = Column(String(100), nullable=True)
    telefono_extension = Column(String(20), nullable=True)
    horario_atencion = Column(Text, nullable=True)
    
    # Estadísticas
    capitulos_creados = Column(Integer, default=0)
    evaluaciones_creadas = Column(Integer, default=0)
    
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="docente")
    
    def __repr__(self):
        return f"<Docente(id={self.id_docente}, num_empleado='{self.numero_empleado}', dept='{self.departamento}')>"


class Rol(BaseUsuarios):
    """
    Tabla: roles
    Define roles del sistema (Administrador, Docente, Estudiante, etc.).
    """
    __tablename__ = 'roles'
    
    id_rol = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)
    activo = Column(Boolean, default=True)
    
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    usuarios = relationship("Usuario", secondary=usuario_rol, back_populates="roles")
    permisos = relationship("Permiso", secondary=rol_permiso, back_populates="roles")
    
    def __repr__(self):
        return f"<Rol(id={self.id_rol}, nombre='{self.nombre}')>"


class Permiso(BaseUsuarios):
    """
    Tabla: permisos
    Define permisos granulares del sistema.
    """
    __tablename__ = 'permisos'
    
    id_permiso = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)
    recurso = Column(String(50), nullable=False)  # Ej: "capitulo", "contenido", "evaluacion"
    accion = Column(String(50), nullable=False)   # Ej: "crear", "leer", "actualizar", "eliminar"
    
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    roles = relationship("Rol", secondary=rol_permiso, back_populates="permisos")
    
    def __repr__(self):
        return f"<Permiso(id={self.id_permiso}, nombre='{self.nombre}', recurso='{self.recurso}', accion='{self.accion}')>"

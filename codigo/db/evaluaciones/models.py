"""
Modelos SQLAlchemy para la Base de Datos de Evaluaciones
=========================================================
Tablas: evaluaciones, preguntas, opciones, intentos, respuestas
"""

from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Float, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import BaseEvaluaciones


class TipoPregunta(enum.Enum):
    """Enum para tipos de pregunta."""
    OPCION_MULTIPLE = "opcion_multiple"
    VERDADERO_FALSO = "verdadero_falso"
    RESPUESTA_CORTA = "respuesta_corta"
    ENSAYO = "ensayo"


class EstadoIntento(enum.Enum):
    """Enum para estados del intento."""
    EN_PROGRESO = "en_progreso"
    COMPLETADO = "completado"
    ABANDONADO = "abandonado"


class Evaluacion(BaseEvaluaciones):
    """
    Tabla: evaluaciones
    Define las evaluaciones asociadas a capítulos.
    """
    __tablename__ = 'evaluaciones'
    
    id_evaluacion = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_capitulo = Column(String(36), nullable=False, index=True)  # Referencia a BD Contenido
    
    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    instrucciones = Column(Text, nullable=True)
    
    # Configuración
    duracion_minutos = Column(Integer, nullable=True)  # Null = sin límite de tiempo
    intentos_maximos = Column(Integer, default=1)
    calificacion_minima_aprobacion = Column(Float, default=60.0)  # Porcentaje
    mostrar_respuestas_correctas = Column(Boolean, default=True)
    
    # Ponderación
    puntos_totales = Column(Float, default=100.0)
    
    # Estado
    activa = Column(Boolean, default=True)
    
    # Metadatos
    id_docente_creador = Column(String(36), nullable=False, index=True)  # Referencia a BD Usuarios
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    fecha_disponible_desde = Column(DateTime, nullable=True)
    fecha_disponible_hasta = Column(DateTime, nullable=True)
    
    # Relaciones
    preguntas = relationship("Pregunta", back_populates="evaluacion", cascade="all, delete-orphan", order_by="Pregunta.orden")
    intentos = relationship("Intento", back_populates="evaluacion", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Evaluacion(id={self.id_evaluacion}, titulo='{self.titulo}', capitulo={self.id_capitulo})>"


class Pregunta(BaseEvaluaciones):
    """
    Tabla: preguntas
    Preguntas de una evaluación.
    """
    __tablename__ = 'preguntas'
    
    id_pregunta = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_evaluacion = Column(String(36), ForeignKey('evaluaciones.id_evaluacion', ondelete='CASCADE'), nullable=False)
    
    tipo = Column(SQLEnum(TipoPregunta), nullable=False)
    enunciado = Column(Text, nullable=False)
    explicacion = Column(Text, nullable=True)  # Explicación de la respuesta correcta
    
    # Configuración
    orden = Column(Integer, nullable=False)
    puntos = Column(Float, default=1.0)
    obligatoria = Column(Boolean, default=True)
    
    # Para respuestas de texto
    respuesta_correcta_texto = Column(Text, nullable=True)
    
    # Metadatos
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    evaluacion = relationship("Evaluacion", back_populates="preguntas")
    opciones = relationship("Opcion", back_populates="pregunta", cascade="all, delete-orphan", order_by="Opcion.orden")
    respuestas = relationship("Respuesta", back_populates="pregunta", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Pregunta(id={self.id_pregunta}, tipo='{self.tipo.value}', orden={self.orden})>"


class Opcion(BaseEvaluaciones):
    """
    Tabla: opciones
    Opciones de respuesta para preguntas de opción múltiple.
    """
    __tablename__ = 'opciones'
    
    id_opcion = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_pregunta = Column(String(36), ForeignKey('preguntas.id_pregunta', ondelete='CASCADE'), nullable=False)
    
    texto = Column(Text, nullable=False)
    es_correcta = Column(Boolean, default=False)
    orden = Column(Integer, nullable=False)
    
    # Retroalimentación específica de la opción (opcional)
    retroalimentacion = Column(Text, nullable=True)
    
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    pregunta = relationship("Pregunta", back_populates="opciones")
    
    def __repr__(self):
        return f"<Opcion(id={self.id_opcion}, correcta={self.es_correcta}, orden={self.orden})>"


class Intento(BaseEvaluaciones):
    """
    Tabla: intentos
    Registra los intentos de evaluación de los estudiantes.
    """
    __tablename__ = 'intentos'
    
    id_intento = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_evaluacion = Column(String(36), ForeignKey('evaluaciones.id_evaluacion', ondelete='CASCADE'), nullable=False)
    id_estudiante = Column(String(36), nullable=False, index=True)  # Referencia a BD Usuarios
    
    # Estado del intento
    estado = Column(SQLEnum(EstadoIntento), default=EstadoIntento.EN_PROGRESO)
    numero_intento = Column(Integer, nullable=False)  # 1, 2, 3...
    
    # Calificación
    puntos_obtenidos = Column(Float, default=0.0)
    puntos_totales = Column(Float, nullable=False)
    porcentaje = Column(Float, default=0.0)  # 0-100
    aprobado = Column(Boolean, default=False)
    
    # Tiempos
    fecha_inicio = Column(DateTime, default=datetime.utcnow)
    fecha_finalizacion = Column(DateTime, nullable=True)
    tiempo_transcurrido_segundos = Column(Integer, default=0)
    
    # Relaciones
    evaluacion = relationship("Evaluacion", back_populates="intentos")
    respuestas = relationship("Respuesta", back_populates="intento", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Intento(id={self.id_intento}, estudiante={self.id_estudiante}, intento={self.numero_intento}, puntaje={self.porcentaje}%)>"


class Respuesta(BaseEvaluaciones):
    """
    Tabla: respuestas
    Respuestas individuales del estudiante a cada pregunta.
    """
    __tablename__ = 'respuestas'
    
    id_respuesta = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_intento = Column(String(36), ForeignKey('intentos.id_intento', ondelete='CASCADE'), nullable=False)
    id_pregunta = Column(String(36), ForeignKey('preguntas.id_pregunta', ondelete='CASCADE'), nullable=False)
    
    # Respuesta del estudiante
    id_opcion_seleccionada = Column(String(36), nullable=True)  # Para opción múltiple
    respuesta_texto = Column(Text, nullable=True)  # Para respuesta corta/ensayo
    
    # Calificación
    es_correcta = Column(Boolean, nullable=True)  # Null si aún no se califica
    puntos_obtenidos = Column(Float, default=0.0)
    
    # Retroalimentación del docente (para preguntas de ensayo)
    retroalimentacion_docente = Column(Text, nullable=True)
    
    # Metadatos
    fecha_respuesta = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    intento = relationship("Intento", back_populates="respuestas")
    pregunta = relationship("Pregunta", back_populates="respuestas")
    
    def __repr__(self):
        return f"<Respuesta(id={self.id_respuesta}, correcta={self.es_correcta}, puntos={self.puntos_obtenidos})>"

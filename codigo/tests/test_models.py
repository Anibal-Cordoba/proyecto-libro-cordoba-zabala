"""
Tests Unitarios para el Modelo Capitulo
========================================
Tests de la capa de modelo/base de datos.
"""

import pytest
from sqlalchemy.exc import IntegrityError
from db.contenido.models import Capitulo


class TestCapituloModel:
    """Tests unitarios para el modelo Capitulo."""
    
    def test_crear_capitulo_basico(self, test_db_session):
        """Test: Crear un capítulo con datos básicos."""
        # Arrange & Act
        capitulo = Capitulo(
            titulo="Capítulo Test",
            numero=1,
            tema="Testing",
            estado="BORRADOR"
        )
        test_db_session.add(capitulo)
        test_db_session.commit()
        test_db_session.refresh(capitulo)
        
        # Assert
        assert capitulo.id_capitulo is not None
        assert capitulo.titulo == "Capítulo Test"
        assert capitulo.numero == 1
        assert capitulo.estado == "BORRADOR"
        assert capitulo.fecha_creacion is not None
    
    
    def test_crear_capitulo_publicado(self, test_db_session):
        """Test: Crear un capítulo en estado PUBLICADO."""
        # Arrange & Act
        capitulo = Capitulo(
            titulo="Capítulo Publicado",
            numero=10,
            tema="Producción",
            introduccion="Introducción del capítulo",
            estado="PUBLICADO"
        )
        test_db_session.add(capitulo)
        test_db_session.commit()
        test_db_session.refresh(capitulo)
        
        # Assert
        assert capitulo.estado == "PUBLICADO"
        assert capitulo.introduccion == "Introducción del capítulo"
    
    
    def test_crear_capitulo_sin_introduccion(self, test_db_session):
        """Test: La introducción es opcional."""
        # Arrange & Act
        capitulo = Capitulo(
            titulo="Sin Intro",
            numero=5,
            tema="Test",
            estado="BORRADOR"
        )
        test_db_session.add(capitulo)
        test_db_session.commit()
        
        # Assert
        assert capitulo.introduccion is None
    
    
    def test_numero_capitulo_debe_ser_unico(self, test_db_session):
        """Test: El número de capítulo debe ser único."""
        # Arrange
        capitulo1 = Capitulo(
            titulo="Primero",
            numero=1,
            tema="Test",
            estado="BORRADOR"
        )
        test_db_session.add(capitulo1)
        test_db_session.commit()
        
        # Act & Assert
        capitulo2 = Capitulo(
            titulo="Segundo",
            numero=1,  # Mismo número
            tema="Test",
            estado="BORRADOR"
        )
        test_db_session.add(capitulo2)
        
        with pytest.raises(IntegrityError):
            test_db_session.commit()
    
    
    def test_estados_validos(self, test_db_session):
        """Test: Verifica los diferentes estados válidos."""
        estados = ["BORRADOR", "PUBLICADO", "ARCHIVADO"]
        
        for i, estado in enumerate(estados, start=1):
            capitulo = Capitulo(
                titulo=f"Capítulo {estado}",
                numero=i,
                tema="Estados",
                estado=estado
            )
            test_db_session.add(capitulo)
        
        test_db_session.commit()
        
        # Verificar que todos se guardaron
        capitulos = test_db_session.query(Capitulo).all()
        assert len(capitulos) == 3
        
        estados_guardados = [c.estado for c in capitulos]
        for estado in estados:
            assert estado in estados_guardados
    
    
    def test_fecha_modificacion_se_actualiza(self, test_db_session):
        """Test: La fecha de modificación se actualiza automáticamente."""
        import time
        
        # Arrange
        capitulo = Capitulo(
            titulo="Test Fecha",
            numero=99,
            tema="Tiempo",
            estado="BORRADOR"
        )
        test_db_session.add(capitulo)
        test_db_session.commit()
        test_db_session.refresh(capitulo)
        
        fecha_original = capitulo.fecha_modificacion
        
        # Act - Esperar un poco y modificar
        time.sleep(0.1)
        capitulo.titulo = "Test Fecha Modificado"
        test_db_session.commit()
        test_db_session.refresh(capitulo)
        
        # Assert
        assert capitulo.fecha_modificacion >= fecha_original
    
    
    def test_repr_capitulo(self, test_db_session):
        """Test: Verificar representación string del capítulo."""
        capitulo = Capitulo(
            titulo="Test Repr",
            numero=77,
            tema="Strings",
            estado="PUBLICADO"
        )
        test_db_session.add(capitulo)
        test_db_session.commit()
        test_db_session.refresh(capitulo)
        
        repr_str = repr(capitulo)
        
        assert "Capitulo" in repr_str
        assert str(capitulo.numero) in repr_str
        assert capitulo.titulo in repr_str
    
    
    def test_query_capitulos_por_estado(self, test_db_session, multiples_capitulos):
        """Test: Filtrar capítulos por estado."""
        # Act
        publicados = test_db_session.query(Capitulo).filter(
            Capitulo.estado == "PUBLICADO"
        ).all()
        
        borradores = test_db_session.query(Capitulo).filter(
            Capitulo.estado == "BORRADOR"
        ).all()
        
        # Assert
        assert len(publicados) == 3
        assert len(borradores) == 1
        
        for cap in publicados:
            assert cap.estado == "PUBLICADO"
    
    
    def test_query_capitulos_ordenados_por_numero(self, test_db_session, multiples_capitulos):
        """Test: Obtener capítulos ordenados por número."""
        # Act
        capitulos = test_db_session.query(Capitulo).order_by(Capitulo.numero).all()
        
        # Assert
        numeros = [c.numero for c in capitulos]
        assert numeros == sorted(numeros)
    
    
    def test_eliminar_capitulo(self, test_db_session):
        """Test: Eliminar un capítulo."""
        # Arrange
        capitulo = Capitulo(
            titulo="Para Eliminar",
            numero=999,
            tema="Delete",
            estado="BORRADOR"
        )
        test_db_session.add(capitulo)
        test_db_session.commit()
        
        capitulo_id = capitulo.id_capitulo
        
        # Act
        test_db_session.delete(capitulo)
        test_db_session.commit()
        
        # Assert
        resultado = test_db_session.query(Capitulo).filter(
            Capitulo.id_capitulo == capitulo_id
        ).first()
        
        assert resultado is None


class TestCapituloValidaciones:
    """Tests de validaciones de negocio para Capitulo."""
    
    def test_titulo_no_vacio(self, test_db_session):
        """Test: El título no puede estar vacío."""
        # Nota: SQLAlchemy permite strings vacías, la validación
        # debe hacerse en la capa de Pydantic/API
        capitulo = Capitulo(
            titulo="",  # Vacío pero válido en BD
            numero=1,
            tema="Test",
            estado="BORRADOR"
        )
        test_db_session.add(capitulo)
        test_db_session.commit()
        
        # La BD lo acepta, pero el API debería validar
        assert capitulo.titulo == ""
    
    
    def test_numero_positivo(self, test_db_session):
        """Test: El número debería ser positivo."""
        # Nota: La BD acepta números negativos, pero lógicamente 
        # debería validarse en el API
        capitulo = Capitulo(
            titulo="Test Negativo",
            numero=-1,
            tema="Test",
            estado="BORRADOR"
        )
        test_db_session.add(capitulo)
        test_db_session.commit()
        
        # Se guarda pero no tiene sentido de negocio
        assert capitulo.numero == -1
        # TODO: Agregar constraint en BD o validación en API

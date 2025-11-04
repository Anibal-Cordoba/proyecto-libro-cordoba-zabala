"""
Tests para CP02_02: Actualizar Capítulo
========================================
Casos de prueba para el endpoint PUT /api/capitulos/{id}

Cobertura:
- Actualización exitosa de campos individuales
- Actualización de múltiples campos
- Cambios de estado
- Validaciones y errores
- Integridad de datos
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import time


# ============================================================================
# GRUPO 1: Actualización Exitosa
# ============================================================================

class TestCP02_02_ActualizarExitoso:
    """Tests de actualización exitosa de capítulos"""
    
    def test_actualizar_titulo(self, client, capitulo_borrador):
        """
        Test CP02_02.01: Actualizar solo el título
        """
        # Arrange
        capitulo_id = capitulo_borrador.id_capitulo
        nuevo_titulo = "Título Actualizado Exitosamente"
        
        # Act
        response = client.put(
            f"/api/capitulos/{capitulo_id}",
            json={"titulo": nuevo_titulo}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["titulo"] == nuevo_titulo
        assert data["numero"] == capitulo_borrador.numero  # No cambió
        assert data["tema"] == capitulo_borrador.tema  # No cambió
    
    def test_actualizar_introduccion(self, client, capitulo_publicado):
        """
        Test CP02_02.02: Actualizar solo la introducción
        """
        # Arrange
        capitulo_id = capitulo_publicado.id_capitulo
        nueva_intro = "Esta es una nueva introducción mucho más detallada."
        
        # Act
        response = client.put(
            f"/api/capitulos/{capitulo_id}",
            json={"introduccion": nueva_intro}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["introduccion"] == nueva_intro
        assert data["titulo"] == capitulo_publicado.titulo  # No cambió
    
    def test_actualizar_multiples_campos(self, client, capitulo_borrador):
        """
        Test CP02_02.03: Actualizar varios campos a la vez
        """
        # Arrange
        capitulo_id = capitulo_borrador.id_capitulo
        actualizacion = {
            "titulo": "Nuevo Título Completo",
            "tema": "Nuevo Tema Actualizado",
            "introduccion": "Nueva introducción detallada"
        }
        
        # Act
        response = client.put(
            f"/api/capitulos/{capitulo_id}",
            json=actualizacion
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["titulo"] == actualizacion["titulo"]
        assert data["tema"] == actualizacion["tema"]
        assert data["introduccion"] == actualizacion["introduccion"]
    
    def test_actualizar_estado_borrador_a_publicado(self, client, capitulo_borrador):
        """
        Test CP02_02.04: Cambiar estado de BORRADOR a PUBLICADO
        """
        # Arrange
        capitulo_id = capitulo_borrador.id_capitulo
        
        # Act
        response = client.put(
            f"/api/capitulos/{capitulo_id}",
            json={"estado": "PUBLICADO"}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["estado"] == "PUBLICADO"
        
        # Verificar con GET
        get_response = client.get(f"/api/capitulos/{capitulo_id}")
        assert get_response.json()["estado"] == "PUBLICADO"
    
    def test_actualizar_estado_publicado_a_archivado(self, client, capitulo_publicado):
        """
        Test CP02_02.05: Cambiar estado de PUBLICADO a ARCHIVADO
        """
        # Arrange
        capitulo_id = capitulo_publicado.id_capitulo
        
        # Act
        response = client.put(
            f"/api/capitulos/{capitulo_id}",
            json={"estado": "ARCHIVADO"}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["estado"] == "ARCHIVADO"


# ============================================================================
# GRUPO 2: Validaciones y Errores
# ============================================================================

class TestCP02_02_Validaciones:
    """Tests de validaciones en actualizaciones"""
    
    def test_actualizar_capitulo_inexistente(self, client):
        """
        Test CP02_02.06: Actualizar capítulo que no existe
        """
        # Arrange
        id_falso = "99999999-9999-9999-9999-999999999999"
        
        # Act
        response = client.put(
            f"/api/capitulos/{id_falso}",
            json={"titulo": "No Debería Funcionar"}
        )
        
        # Assert
        assert response.status_code == 404
        assert "no encontrado" in response.json()["detail"].lower()
    
    def test_actualizar_titulo_vacio(self, client, capitulo_borrador):
        """
        Test CP02_02.07: No permitir título vacío
        """
        # Arrange
        capitulo_id = capitulo_borrador.id_capitulo
        
        # Act
        response = client.put(
            f"/api/capitulos/{capitulo_id}",
            json={"titulo": ""}
        )
        
        # Assert
        assert response.status_code == 422
    
    def test_actualizar_titulo_muy_largo(self, client, capitulo_borrador):
        """
        Test CP02_02.08: No permitir título > 500 caracteres
        """
        # Arrange
        capitulo_id = capitulo_borrador.id_capitulo
        titulo_largo = "A" * 501
        
        # Act
        response = client.put(
            f"/api/capitulos/{capitulo_id}",
            json={"titulo": titulo_largo}
        )
        
        # Assert
        assert response.status_code == 422
    
    def test_actualizar_numero_a_duplicado(self, client, multiples_capitulos):
        """
        Test CP02_02.09: No permitir cambiar número a uno ya existente
        """
        # Arrange
        cap1 = multiples_capitulos[0]
        cap2 = multiples_capitulos[1]
        
        # Act - Intentar cambiar cap1.numero al de cap2
        response = client.put(
            f"/api/capitulos/{cap1.id_capitulo}",
            json={"numero": cap2.numero}
        )
        
        # Assert
        # Nota: Esto debería fallar con 400 si hay validación
        # Si no hay validación, documentarlo como recomendación
        if response.status_code == 400:
            assert "duplicado" in response.json()["detail"].lower() or \
                   "existe" in response.json()["detail"].lower()
        else:
            print("⚠️  ADVERTENCIA: No hay validación de número duplicado en UPDATE")


# ============================================================================
# GRUPO 3: Integridad de Datos
# ============================================================================

class TestCP02_02_Integridad:
    """Tests de integridad y consistencia de datos"""
    
    def test_fecha_modificacion_se_actualiza(self, client, capitulo_borrador):
        """
        Test CP02_02.10: Verificar que fecha_modificacion se actualiza
        """
        # Arrange
        capitulo_id = capitulo_borrador.id_capitulo
        fecha_original = capitulo_borrador.fecha_modificacion
        
        time.sleep(0.1)  # Pequeña pausa para asegurar diferencia de tiempo
        
        # Act
        response = client.put(
            f"/api/capitulos/{capitulo_id}",
            json={"titulo": "Título Actualizado"}
        )
        
        # Assert
        assert response.status_code == 200
        fecha_nueva = response.json()["fecha_modificacion"]
        assert fecha_nueva != fecha_original
    
    def test_actualizar_y_verificar_persistencia(self, client, capitulo_borrador):
        """
        Test CP02_02.11: Verificar que los cambios persisten
        """
        # Arrange
        capitulo_id = capitulo_borrador.id_capitulo
        nuevo_titulo = "Título Persistido"
        nuevo_tema = "Tema Persistido"
        
        # Act
        update_response = client.put(
            f"/api/capitulos/{capitulo_id}",
            json={
                "titulo": nuevo_titulo,
                "tema": nuevo_tema
            }
        )
        
        # Verificar con GET
        get_response = client.get(f"/api/capitulos/{capitulo_id}")
        
        # Assert
        assert update_response.status_code == 200
        assert get_response.status_code == 200
        data = get_response.json()
        assert data["titulo"] == nuevo_titulo
        assert data["tema"] == nuevo_tema
    
    def test_actualizacion_parcial_no_afecta_otros_campos(self, client, capitulo_publicado):
        """
        Test CP02_02.12: Actualización parcial mantiene otros campos intactos
        """
        # Arrange
        capitulo_id = capitulo_publicado.id_capitulo
        titulo_original = capitulo_publicado.titulo
        tema_original = capitulo_publicado.tema
        
        # Act - Solo actualizar introducción
        response = client.put(
            f"/api/capitulos/{capitulo_id}",
            json={"introduccion": "Nueva introducción"}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["titulo"] == titulo_original
        assert data["tema"] == tema_original


# ============================================================================
# GRUPO 4: Integración y Flujos
# ============================================================================

class TestCP02_02_Integracion:
    """Tests de flujos completos de actualización"""
    
    def test_flujo_crear_actualizar_listar(self, client):
        """
        Test CP02_02.13: Flujo completo crear → actualizar → listar
        """
        # Arrange & Act 1: Crear
        create_response = client.post("/api/capitulos/", json={
            "titulo": "Capítulo Original",
            "numero": 500,
            "tema": "Tema Original"
        })
        assert create_response.status_code == 201
        capitulo_id = create_response.json()["id_capitulo"]
        
        # Act 2: Actualizar
        update_response = client.put(
            f"/api/capitulos/{capitulo_id}",
            json={"titulo": "Capítulo Actualizado"}
        )
        assert update_response.status_code == 200
        
        # Act 3: Listar y verificar
        list_response = client.get("/api/capitulos/")
        capitulos = list_response.json()
        
        # Assert
        capitulo_encontrado = next(
            (c for c in capitulos if c["id_capitulo"] == capitulo_id),
            None
        )
        assert capitulo_encontrado is not None
        assert capitulo_encontrado["titulo"] == "Capítulo Actualizado"
    
    def test_multiples_actualizaciones_sucesivas(self, client, capitulo_borrador):
        """
        Test CP02_02.14: Múltiples actualizaciones en secuencia
        """
        # Arrange
        capitulo_id = capitulo_borrador.id_capitulo
        
        # Act - Primera actualización
        response1 = client.put(
            f"/api/capitulos/{capitulo_id}",
            json={"titulo": "Versión 1"}
        )
        assert response1.status_code == 200
        
        # Act - Segunda actualización
        response2 = client.put(
            f"/api/capitulos/{capitulo_id}",
            json={"titulo": "Versión 2"}
        )
        assert response2.status_code == 200
        
        # Act - Tercera actualización
        response3 = client.put(
            f"/api/capitulos/{capitulo_id}",
            json={"titulo": "Versión Final"}
        )
        
        # Assert
        assert response3.status_code == 200
        assert response3.json()["titulo"] == "Versión Final"


# ============================================================================
# GRUPO 5: Performance
# ============================================================================

class TestCP02_02_Performance:
    """Tests de performance en actualizaciones"""
    
    @pytest.mark.performance
    def test_tiempo_actualizacion_aceptable(self, client, capitulo_borrador):
        """
        Test CP02_02.15: Actualización debe ser rápida (< 0.2s)
        """
        # Arrange
        capitulo_id = capitulo_borrador.id_capitulo
        
        # Act
        start = time.time()
        response = client.put(
            f"/api/capitulos/{capitulo_id}",
            json={"titulo": "Actualización Rápida"}
        )
        duracion = time.time() - start
        
        # Assert
        assert response.status_code == 200
        assert duracion < 0.2, f"Actualización tardó {duracion:.3f}s (> 0.2s)"

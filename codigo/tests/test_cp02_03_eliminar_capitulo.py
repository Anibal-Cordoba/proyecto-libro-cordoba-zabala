"""
Tests para CP02_03: Eliminar Capítulo
======================================
Casos de prueba para el endpoint DELETE /api/capitulos/{id}

Cobertura:
- Eliminación exitosa
- Validaciones y errores
- Verificación de persistencia
- Integridad referencial (CASCADE)
"""

import pytest
from fastapi.testclient import TestClient


# ============================================================================
# GRUPO 1: Eliminación Exitosa
# ============================================================================

class TestCP02_03_EliminarExitoso:
    """Tests de eliminación exitosa de capítulos"""
    
    def test_eliminar_capitulo_borrador(self, client, capitulo_borrador):
        """
        Test CP02_03.01: Eliminar capítulo en estado BORRADOR
        """
        # Arrange
        capitulo_id = capitulo_borrador.id_capitulo
        
        # Act
        response = client.delete(f"/api/capitulos/{capitulo_id}")
        
        # Assert
        assert response.status_code == 204
        assert response.text == "" or response.text == "null"
    
    def test_eliminar_capitulo_publicado(self, client, capitulo_publicado):
        """
        Test CP02_03.02: Eliminar capítulo en estado PUBLICADO
        """
        # Arrange
        capitulo_id = capitulo_publicado.id_capitulo
        
        # Act
        response = client.delete(f"/api/capitulos/{capitulo_id}")
        
        # Assert
        assert response.status_code == 204
    
    def test_eliminar_capitulo_archivado(self, client, capitulo_archivado):
        """
        Test CP02_03.03: Eliminar capítulo en estado ARCHIVADO
        """
        # Arrange
        capitulo_id = capitulo_archivado.id_capitulo
        
        # Act
        response = client.delete(f"/api/capitulos/{capitulo_id}")
        
        # Assert
        assert response.status_code == 204


# ============================================================================
# GRUPO 2: Verificación de Eliminación
# ============================================================================

class TestCP02_03_VerificarEliminacion:
    """Tests que verifican que el capítulo realmente desapareció"""
    
    def test_capitulo_eliminado_no_aparece_en_get(self, client, capitulo_borrador):
        """
        Test CP02_03.04: Capítulo eliminado retorna 404 en GET
        """
        # Arrange
        capitulo_id = capitulo_borrador.id_capitulo
        
        # Act
        delete_response = client.delete(f"/api/capitulos/{capitulo_id}")
        assert delete_response.status_code == 204
        
        # Verificar con GET
        get_response = client.get(f"/api/capitulos/{capitulo_id}")
        
        # Assert
        assert get_response.status_code == 404
        assert "no encontrado" in get_response.json()["detail"].lower()
    
    def test_capitulo_eliminado_no_aparece_en_lista(self, client, capitulo_publicado):
        """
        Test CP02_03.05: Capítulo eliminado no aparece en listado
        """
        # Arrange
        capitulo_id = capitulo_publicado.id_capitulo
        numero = capitulo_publicado.numero
        
        # Act - Eliminar
        delete_response = client.delete(f"/api/capitulos/{capitulo_id}")
        assert delete_response.status_code == 204
        
        # Act - Listar
        list_response = client.get("/api/capitulos/")
        capitulos = list_response.json()
        
        # Assert
        numeros = [c["numero"] for c in capitulos]
        assert numero not in numeros
    
    def test_no_se_puede_eliminar_dos_veces(self, client, capitulo_borrador):
        """
        Test CP02_03.06: Segunda eliminación retorna 404
        """
        # Arrange
        capitulo_id = capitulo_borrador.id_capitulo
        
        # Act - Primera eliminación
        response1 = client.delete(f"/api/capitulos/{capitulo_id}")
        assert response1.status_code == 204
        
        # Act - Segunda eliminación
        response2 = client.delete(f"/api/capitulos/{capitulo_id}")
        
        # Assert
        assert response2.status_code == 404


# ============================================================================
# GRUPO 3: Validaciones y Errores
# ============================================================================

class TestCP02_03_Validaciones:
    """Tests de validaciones en eliminación"""
    
    def test_eliminar_capitulo_inexistente(self, client):
        """
        Test CP02_03.07: Eliminar capítulo que no existe
        """
        # Arrange
        id_falso = "99999999-9999-9999-9999-999999999999"
        
        # Act
        response = client.delete(f"/api/capitulos/{id_falso}")
        
        # Assert
        assert response.status_code == 404
        assert "no encontrado" in response.json()["detail"].lower()
    
    def test_eliminar_con_id_invalido(self, client):
        """
        Test CP02_03.08: ID malformado retorna error
        """
        # Arrange
        id_invalido = "no-es-un-uuid"
        
        # Act
        response = client.delete(f"/api/capitulos/{id_invalido}")
        
        # Assert
        # Puede ser 404 o 422 dependiendo de la validación
        assert response.status_code in [404, 422]


# ============================================================================
# GRUPO 4: Integridad Referencial
# ============================================================================

class TestCP02_03_IntegridadReferencial:
    """Tests de CASCADE y relaciones"""
    
    def test_eliminar_capitulo_con_contenido_simula_cascade(self, client, capitulo_con_contenido):
        """
        Test CP02_03.09: Eliminar capítulo (simula que tiene contenido)
        
        Nota: Este test documenta el comportamiento esperado.
        Cuando se implementen las uniones, verificar CASCADE.
        """
        # Arrange
        capitulo_id = capitulo_con_contenido.id_capitulo
        
        # Act
        response = client.delete(f"/api/capitulos/{capitulo_id}")
        
        # Assert
        assert response.status_code == 204
        
        # Verificar que desapareció
        get_response = client.get(f"/api/capitulos/{capitulo_id}")
        assert get_response.status_code == 404
        
        print("✅ Capítulo eliminado. En futuro verificar CASCADE de uniones.")


# ============================================================================
# GRUPO 5: Integración y Flujos
# ============================================================================

class TestCP02_03_Integracion:
    """Tests de flujos completos con eliminación"""
    
    def test_flujo_crear_y_eliminar(self, client):
        """
        Test CP02_03.10: Flujo completo crear → eliminar → verificar
        """
        # Act 1: Crear
        create_response = client.post("/api/capitulos/", json={
            "titulo": "Capítulo a Eliminar",
            "numero": 600,
            "tema": "Testing Eliminación"
        })
        assert create_response.status_code == 201
        capitulo_id = create_response.json()["id_capitulo"]
        
        # Act 2: Verificar que existe
        get_response1 = client.get(f"/api/capitulos/{capitulo_id}")
        assert get_response1.status_code == 200
        
        # Act 3: Eliminar
        delete_response = client.delete(f"/api/capitulos/{capitulo_id}")
        assert delete_response.status_code == 204
        
        # Act 4: Verificar que ya no existe
        get_response2 = client.get(f"/api/capitulos/{capitulo_id}")
        assert get_response2.status_code == 404

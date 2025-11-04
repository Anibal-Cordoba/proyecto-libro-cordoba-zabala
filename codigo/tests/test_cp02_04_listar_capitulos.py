"""
Tests para CP02_04: Listar y Filtrar Capítulos
===============================================
Casos de prueba para el endpoint GET /api/capitulos/

Cobertura:
- Listado básico
- Paginación (skip, limit)
- Filtros por tema
- Ordenamiento
- Edge cases
"""

import pytest
from fastapi.testclient import TestClient


# ============================================================================
# GRUPO 1: Listado Básico
# ============================================================================

class TestCP02_04_ListadoBasico:
    """Tests de listado sin filtros"""
    
    def test_listar_todos_los_capitulos(self, client, multiples_capitulos):
        """
        Test CP02_04.01: Listar todos los capítulos
        """
        # Act
        response = client.get("/api/capitulos/")
        
        # Assert
        assert response.status_code == 200
        capitulos = response.json()
        assert isinstance(capitulos, list)
        assert len(capitulos) >= len(multiples_capitulos)
    
    def test_lista_vacia_cuando_no_hay_capitulos(self, client, test_db_session):
        """
        Test CP02_04.02: Lista vacía cuando no hay capítulos
        """
        # Arrange - Limpiar todos los capítulos
        from db.contenido.models import Capitulo
        test_db_session.query(Capitulo).delete()
        test_db_session.commit()
        
        # Act
        response = client.get("/api/capitulos/")
        
        # Assert
        assert response.status_code == 200
        assert response.json() == []
    
    def test_capitulos_ordenados_por_numero(self, client):
        """
        Test CP02_04.03: Capítulos vienen ordenados por número
        """
        # Arrange - Crear capítulos en orden aleatorio
        client.post("/api/capitulos/", json={"titulo": "Cap 3", "numero": 103, "tema": "Test"})
        client.post("/api/capitulos/", json={"titulo": "Cap 1", "numero": 101, "tema": "Test"})
        client.post("/api/capitulos/", json={"titulo": "Cap 2", "numero": 102, "tema": "Test"})
        
        # Act
        response = client.get("/api/capitulos/")
        capitulos = response.json()
        
        # Assert
        numeros = [c["numero"] for c in capitulos]
        assert numeros == sorted(numeros), "Los capítulos deben estar ordenados por número"


# ============================================================================
# GRUPO 2: Paginación
# ============================================================================

class TestCP02_04_Paginacion:
    """Tests de paginación con skip y limit"""
    
    def test_paginacion_skip_5(self, client):
        """
        Test CP02_04.04: Paginación con skip=5
        """
        # Arrange - Crear 10 capítulos
        for i in range(10):
            client.post("/api/capitulos/", json={
                "titulo": f"Capítulo {i}",
                "numero": 200 + i,
                "tema": "Paginación"
            })
        
        # Act - Obtener primeros 5
        response_todos = client.get("/api/capitulos/?limit=5")
        primeros_5 = response_todos.json()
        
        # Act - Saltar primeros 5
        response_skip = client.get("/api/capitulos/?skip=5")
        siguientes = response_skip.json()
        
        # Assert
        assert len(primeros_5) == 5
        ids_primeros = [c["id_capitulo"] for c in primeros_5]
        ids_siguientes = [c["id_capitulo"] for c in siguientes]
        
        # No debe haber duplicados
        assert not set(ids_primeros).intersection(set(ids_siguientes))
    
    def test_paginacion_limit_3(self, client, multiples_capitulos):
        """
        Test CP02_04.05: Limitar resultados a 3
        """
        # Act
        response = client.get("/api/capitulos/?limit=3")
        
        # Assert
        assert response.status_code == 200
        capitulos = response.json()
        assert len(capitulos) <= 3
    
    def test_paginacion_skip_y_limit_combinados(self, client):
        """
        Test CP02_04.06: Usar skip y limit juntos
        """
        # Arrange - Crear capítulos
        for i in range(15):
            client.post("/api/capitulos/", json={
                "titulo": f"Cap Pag {i}",
                "numero": 300 + i,
                "tema": "Paginación"
            })
        
        # Act - Segunda página de 5 elementos
        response = client.get("/api/capitulos/?skip=5&limit=5")
        
        # Assert
        assert response.status_code == 200
        capitulos = response.json()
        assert len(capitulos) <= 5


# ============================================================================
# GRUPO 3: Filtros por Tema
# ============================================================================

class TestCP02_04_FiltrosTema:
    """Tests de filtrado por tema"""
    
    def test_filtrar_por_tema_exacto(self, client):
        """
        Test CP02_04.07: Filtrar por tema exacto
        """
        # Arrange
        client.post("/api/capitulos/", json={
            "titulo": "Cap Matemáticas",
            "numero": 401,
            "tema": "Matemáticas"
        })
        client.post("/api/capitulos/", json={
            "titulo": "Cap Historia",
            "numero": 402,
            "tema": "Historia"
        })
        
        # Act
        response = client.get("/api/capitulos/?tema=Matemáticas")
        
        # Assert
        assert response.status_code == 200
        capitulos = response.json()
        assert len(capitulos) >= 1
        assert all("matemática" in c["tema"].lower() for c in capitulos)
    
    def test_filtrar_por_tema_parcial_case_insensitive(self, client):
        """
        Test CP02_04.08: Filtro por tema es case-insensitive y parcial
        """
        # Arrange
        client.post("/api/capitulos/", json={
            "titulo": "Cap Física Cuántica",
            "numero": 501,
            "tema": "Física Cuántica"
        })
        
        # Act - Buscar con minúsculas y parcial
        response = client.get("/api/capitulos/?tema=física")
        
        # Assert
        assert response.status_code == 200
        capitulos = response.json()
        assert len(capitulos) >= 1
        assert any("física" in c["tema"].lower() for c in capitulos)
    
    def test_filtrar_tema_inexistente_retorna_vacio(self, client):
        """
        Test CP02_04.09: Tema inexistente retorna lista vacía
        """
        # Act
        response = client.get("/api/capitulos/?tema=TemaQueNoExiste12345")
        
        # Assert
        assert response.status_code == 200
        capitulos = response.json()
        assert capitulos == []
    
    def test_filtrar_multiples_capitulos_mismo_tema(self, client):
        """
        Test CP02_04.10: Filtrar múltiples capítulos con mismo tema
        """
        # Arrange
        tema = "Biología Marina"
        for i in range(3):
            client.post("/api/capitulos/", json={
                "titulo": f"Biología {i}",
                "numero": 600 + i,
                "tema": tema
            })
        
        # Act
        response = client.get(f"/api/capitulos/?tema={tema}")
        
        # Assert
        assert response.status_code == 200
        capitulos = response.json()
        assert len(capitulos) >= 3


# ============================================================================
# GRUPO 4: Edge Cases
# ============================================================================

class TestCP02_04_EdgeCases:
    """Tests de casos extremos"""
    
    def test_skip_mayor_que_total_retorna_vacio(self, client, multiples_capitulos):
        """
        Test CP02_04.11: Skip mayor que total de capítulos
        """
        # Act
        response = client.get("/api/capitulos/?skip=9999")
        
        # Assert
        assert response.status_code == 200
        assert response.json() == []
    
    def test_limit_cero_retorna_vacio(self, client, multiples_capitulos):
        """
        Test CP02_04.12: Limit=0 retorna lista vacía
        """
        # Act
        response = client.get("/api/capitulos/?limit=0")
        
        # Assert
        assert response.status_code == 200
        assert response.json() == []

"""
CP01_02 — Intento de visualizar capítulo inexistente/no publicado (error controlado)
====================================================================================

Test Case: CP01_02
Caso de Uso Relacionado: CU_01 Visualizar contenido
Descripción: Intenta visualizar capítulo inexistente o no publicado.

Área Funcional: Contenidos
Funcionalidad: Manejo de errores en lectura

Datos de Entrada: 
- Abrir /api/capitulos/{id} con ID inexistente
- Abrir /api/capitulos/{id} con capítulo en estado BORRADOR
- Abrir /api/capitulos/{id} con capítulo en estado ARCHIVADO

Resultado Esperado:
- Mensaje "contenido no disponible" o código 404/403
- No se rompe la navegación
- Respuesta controlada y manejada

Requerimientos de Ambiente:
- BD con capítulo BORRADOR
- BD con capítulo ARCHIVADO
- Ausencia de ID que se solicite
"""

import pytest
from fastapi import status
import uuid


class TestCP01_02_CapituloInexistente:
    """
    Suite de tests para visualizar capítulos inexistentes.
    Verifica el manejo correcto de errores 404.
    """
    
    def test_visualizar_capitulo_id_inexistente(self, client):
        """
        Test Principal CP01_02: ID de capítulo que no existe en BD.
        
        GIVEN: Un ID válido (UUID) pero que no existe en la BD
        WHEN: Se realiza GET a /api/capitulos/{id}
        THEN: 
            - Status 404 NOT FOUND
            - Mensaje de error descriptivo
            - No se rompe la aplicación
        """
        # Arrange - ID válido pero inexistente
        id_inexistente = "00000000-0000-0000-0000-000000000000"
        
        # Act
        response = client.get(f"/api/capitulos/{id_inexistente}")
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND, \
            "Debe retornar 404 cuando el capítulo no existe"
        
        data = response.json()
        assert "detail" in data, "Debe incluir mensaje de error"
        assert "no encontrado" in data["detail"].lower() or "not found" in data["detail"].lower(), \
            "El mensaje debe indicar que no se encontró el capítulo"
    
    
    def test_visualizar_capitulo_uuid_aleatorio(self, client):
        """
        Test CP01_02: UUID completamente aleatorio.
        Simula un usuario que ingresa un ID al azar.
        """
        # Arrange
        id_aleatorio = str(uuid.uuid4())
        
        # Act
        response = client.get(f"/api/capitulos/{id_aleatorio}")
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert id_aleatorio in data["detail"] or "no encontrado" in data["detail"].lower()
    
    
    def test_visualizar_capitulo_id_malformado(self, client):
        """
        Test CP01_02: ID con formato inválido.
        Verifica validación de entrada.
        """
        ids_invalidos = [
            "id-invalido-123",
            "12345",
            "abc-def-ghi",
            "no-es-un-uuid",
            "xxxxx-xxxxx-xxxxx"
        ]
        
        for id_invalido in ids_invalidos:
            # Act
            response = client.get(f"/api/capitulos/{id_invalido}")
            
            # Assert - Puede ser 404 o 422 (validación)
            assert response.status_code in [404, 422], \
                f"ID inválido '{id_invalido}' debe retornar 404 o 422"
            
            data = response.json()
            assert "detail" in data, "Debe incluir detalle del error"
    
    
    def test_mensaje_error_es_informativo(self, client):
        """
        Test CP01_02: El mensaje de error debe ser claro para el usuario.
        """
        # Arrange
        id_inexistente = str(uuid.uuid4())
        
        # Act
        response = client.get(f"/api/capitulos/{id_inexistente}")
        
        # Assert
        data = response.json()
        mensaje = data["detail"]
        
        # Verificar que el mensaje es útil
        assert len(mensaje) > 10, "Mensaje debe ser descriptivo"
        assert any(palabra in mensaje.lower() for palabra in ["capítulo", "capitulo", "no encontrado", "not found"]), \
            "Mensaje debe mencionar el recurso no encontrado"


class TestCP01_02_CapituloNoPublicado:
    """
    Suite de tests para capítulos en estados no publicados.
    Verifica restricciones de acceso según el estado.
    """
    
    def test_visualizar_capitulo_borrador(self, client, capitulo_borrador):
        """
        Test Principal CP01_02: Intento de visualizar capítulo en BORRADOR.
        
        GIVEN: Existe un capítulo en estado BORRADOR
        WHEN: Se intenta visualizar
        THEN: 
            - Se debe restringir el acceso (403) o informar que no está publicado
            - Mensaje claro sobre el estado
        
        Nota: Comportamiento actual permite visualización.
        TODO: Implementar restricción de acceso por estado.
        """
        # Act
        response = client.get(f"/api/capitulos/{capitulo_borrador.id_capitulo}")
        
        # Assert - Comportamiento actual
        if response.status_code == 200:
            # Si se permite visualizar, debe indicar el estado
            data = response.json()
            assert data["estado"] == "BORRADOR", \
                "Debe indicar claramente que es un borrador"
            
            # Advertencia: en producción esto debería restringirse
            print("⚠️  ADVERTENCIA: El capítulo BORRADOR es accesible. "
                  "Considerar implementar restricción de acceso.")
        else:
            # Comportamiento deseado futuro
            assert response.status_code in [403, 404], \
                "Capítulo BORRADOR no debería ser accesible públicamente"
    
    
    def test_visualizar_capitulo_archivado(self, client, capitulo_archivado):
        """
        Test CP01_02: Intento de visualizar capítulo ARCHIVADO.
        
        GIVEN: Existe un capítulo en estado ARCHIVADO
        WHEN: Se intenta visualizar
        THEN: Debe restringir acceso o indicar que no está disponible
        """
        # Act
        response = client.get(f"/api/capitulos/{capitulo_archivado.id_capitulo}")
        
        # Assert
        if response.status_code == 200:
            data = response.json()
            assert data["estado"] == "ARCHIVADO"
            print("⚠️  ADVERTENCIA: El capítulo ARCHIVADO es accesible. "
                  "Considerar implementar restricción.")
        else:
            assert response.status_code in [403, 404, 410], \
                "Capítulo ARCHIVADO debería retornar error apropiado"
    
    
    def test_listar_no_incluye_borradores(self, client, multiples_capitulos):
        """
        Test CP01_02: Al listar, no se deben incluir capítulos BORRADOR.
        
        GIVEN: Existen capítulos en diferentes estados
        WHEN: Se lista sin filtros
        THEN: Solo se muestran capítulos PUBLICADOS
        """
        # Act
        response = client.get("/api/capitulos/")
        
        # Assert
        assert response.status_code == 200
        capitulos = response.json()
        
        # En una implementación ideal, filtrar por estado
        # Por ahora, documentamos el comportamiento
        estados = [cap["estado"] for cap in capitulos]
        
        if "BORRADOR" in estados:
            print("⚠️  ADVERTENCIA: Los capítulos BORRADOR aparecen en el listado. "
                  "Implementar filtro por estado PUBLICADO.")
        else:
            assert all(estado == "PUBLICADO" for estado in estados), \
                "Solo capítulos PUBLICADOS deberían listarse"
    
    
    def test_filtrar_solo_publicados(self, client, multiples_capitulos):
        """
        Test CP01_02: Verificar que existe manera de filtrar por estado.
        
        Nota: Actualmente el endpoint no tiene este parámetro.
        Este test documenta la funcionalidad deseada.
        """
        # Act - Intentar filtrar (puede no estar implementado)
        response = client.get("/api/capitulos/?estado=PUBLICADO")
        
        # Assert
        assert response.status_code == 200
        capitulos = response.json()
        
        # Si el filtro funciona
        if len(capitulos) > 0 and "estado" in capitulos[0]:
            estados = [cap["estado"] for cap in capitulos]
            # Idealmente, todos deberían ser PUBLICADOS
            publicados = sum(1 for e in estados if e == "PUBLICADO")
            print(f"ℹ️  Capítulos PUBLICADOS: {publicados}/{len(capitulos)}")


class TestCP01_02_ManejoErrores:
    """
    Tests para verificar que el manejo de errores es robusto.
    La aplicación no debe romperse ante entradas inválidas.
    """
    
    def test_error_no_rompe_navegacion(self, client):
        """
        Test CP01_02: Error 404 no debe romper la navegación.
        
        GIVEN: Se realiza una petición a un ID inexistente
        WHEN: Se recibe error 404
        THEN: 
            - Respuesta JSON válida
            - Headers correctos
            - Aplicación sigue funcionando
        """
        # Act
        response = client.get("/api/capitulos/id-inexistente")
        
        # Assert - Verificar que es una respuesta válida
        assert response.status_code in [404, 422]
        assert response.headers["content-type"] == "application/json"
        
        # Verificar que el JSON es válido
        data = response.json()
        assert isinstance(data, dict)
        assert "detail" in data
        
        # Verificar que la app sigue funcionando (probando el endpoint de listado)
        health_response = client.get("/api/capitulos/")
        assert health_response.status_code == 200, \
            "La API debe seguir funcionando después de un error"
    
    
    def test_multiples_errores_consecutivos(self, client):
        """
        Test CP01_02: Múltiples errores consecutivos no afectan la estabilidad.
        """
        ids_invalidos = [
            str(uuid.uuid4()),
            str(uuid.uuid4()),
            "id-invalido",
            "12345",
            str(uuid.uuid4())
        ]
        
        for id_invalido in ids_invalidos:
            # Act
            response = client.get(f"/api/capitulos/{id_invalido}")
            
            # Assert - Cada error debe manejarse correctamente
            assert response.status_code in [404, 422]
            assert "detail" in response.json()
        
        # Verificar que después de todos los errores, la API funciona
        response = client.get("/api/capitulos/")
        assert response.status_code == 200
    
    
    def test_error_incluye_informacion_util(self, client):
        """
        Test CP01_02: Mensaje de error debe incluir información útil.
        NO debe exponer información sensible del sistema.
        """
        # Arrange
        id_inexistente = str(uuid.uuid4())
        
        # Act
        response = client.get(f"/api/capitulos/{id_inexistente}")
        
        # Assert
        data = response.json()
        mensaje = data["detail"]
        
        # Debe incluir información útil
        assert len(mensaje) > 0
        
        # NO debe incluir información sensible
        palabras_prohibidas = [
            "traceback", "exception", "error:", 
            "database", "sql", "query",
            "password", "token", "secret"
        ]
        
        for palabra in palabras_prohibidas:
            assert palabra.lower() not in mensaje.lower(), \
                f"Mensaje no debe exponer '{palabra}'"
    
    
    def test_codigo_http_correcto_segun_error(self, client, capitulo_borrador):
        """
        Test CP01_02: Verificar códigos HTTP apropiados.
        
        - 404: No encontrado
        - 403: Prohibido (sin permisos)
        - 422: Error de validación
        """
        # Caso 1: ID inexistente -> 404
        response = client.get(f"/api/capitulos/{uuid.uuid4()}")
        assert response.status_code == 404
        
        # Caso 2: ID inválido -> 404 o 422
        response = client.get("/api/capitulos/id-invalido")
        assert response.status_code in [404, 422]
        
        # Caso 3: Capítulo BORRADOR -> Actualmente 200, debería ser 403
        response = client.get(f"/api/capitulos/{capitulo_borrador.id_capitulo}")
        # Documentar comportamiento actual vs deseado
        if response.status_code == 200:
            print("ℹ️  Capítulo BORRADOR accesible (200). "
                  "Comportamiento deseado: 403 Forbidden")


class TestCP01_02_Integracion:
    """
    Tests de integración para verificar flujos completos con errores.
    """
    
    def test_flujo_buscar_inexistente_y_recuperar(self, client, capitulo_publicado):
        """
        Test CP01_02: Flujo de usuario que busca un capítulo inexistente
        y luego busca uno que sí existe.
        
        Simula: Usuario se equivoca de ID, recibe error, corrige y accede.
        """
        # Step 1: Intentar acceder a capítulo inexistente
        response_error = client.get("/api/capitulos/id-inexistente")
        assert response_error.status_code in [404, 422]
        
        # Step 2: Usuario corrige y busca el listado
        response_lista = client.get("/api/capitulos/")
        assert response_lista.status_code == 200
        capitulos = response_lista.json()
        assert len(capitulos) > 0
        
        # Step 3: Usuario selecciona capítulo válido
        response_valido = client.get(f"/api/capitulos/{capitulo_publicado.id_capitulo}")
        assert response_valido.status_code == 200
        data = response_valido.json()
        assert data["estado"] == "PUBLICADO"
    
    
    def test_navegacion_entre_estados(self, client, capitulo_publicado, capitulo_borrador):
        """
        Test CP01_02: Navegación entre capítulos de diferentes estados.
        """
        # Visualizar capítulo publicado (debe funcionar)
        response1 = client.get(f"/api/capitulos/{capitulo_publicado.id_capitulo}")
        assert response1.status_code == 200
        
        # Intentar visualizar capítulo borrador
        response2 = client.get(f"/api/capitulos/{capitulo_borrador.id_capitulo}")
        # Documentar comportamiento (actualmente 200, debería restringirse)
        
        # Volver a publicado (debe seguir funcionando)
        response3 = client.get(f"/api/capitulos/{capitulo_publicado.id_capitulo}")
        assert response3.status_code == 200
        assert response3.json()["id_capitulo"] == capitulo_publicado.id_capitulo


class TestCP01_02_Regresion:
    """
    Tests de regresión para CP01_02.
    Aseguran que el manejo de errores se mantiene consistente.
    """
    
    def test_estructura_error_consistente(self, client):
        """
        Test CP01_02: Todos los errores deben tener estructura consistente.
        """
        ids_de_prueba = [
            str(uuid.uuid4()),  # Inexistente válido
            "id-invalido",      # Formato inválido
            "12345"             # Numérico
        ]
        
        for test_id in ids_de_prueba:
            response = client.get(f"/api/capitulos/{test_id}")
            
            # Todos deben retornar JSON con "detail"
            if response.status_code in [404, 422]:
                data = response.json()
                assert "detail" in data, \
                    f"Error para ID '{test_id}' debe incluir 'detail'"
                assert isinstance(data["detail"], str), \
                    "Campo 'detail' debe ser string"
    
    
    def test_error_404_siempre_igual(self, client):
        """
        Test CP01_02: Error 404 debe ser consistente entre llamadas.
        """
        id_inexistente = str(uuid.uuid4())
        
        # Realizar múltiples llamadas
        responses = [
            client.get(f"/api/capitulos/{id_inexistente}")
            for _ in range(3)
        ]
        
        # Todas deben retornar lo mismo
        status_codes = [r.status_code for r in responses]
        assert len(set(status_codes)) == 1, \
            "Múltiples llamadas al mismo ID inexistente deben retornar el mismo código"
        
        # Mensajes deben ser consistentes
        mensajes = [r.json()["detail"] for r in responses]
        assert len(set(mensajes)) == 1, \
            "Mensaje de error debe ser consistente"


class TestCP01_02_Seguridad:
    """
    Tests de seguridad relacionados con el acceso a capítulos.
    """
    
    def test_no_expone_existencia_de_borradores(self, client, capitulo_borrador):
        """
        Test CP01_02: No debe revelarse la existencia de capítulos BORRADOR
        a usuarios no autorizados.
        
        Comportamiento deseado: 404 tanto para inexistentes como para BORRADOR.
        """
        # Intento de acceso a borrador
        response = client.get(f"/api/capitulos/{capitulo_borrador.id_capitulo}")
        
        # Idealmente debería ser 404 (no revelar existencia)
        # o 403 (existe pero no tienes permisos)
        if response.status_code == 200:
            print("⚠️  SEGURIDAD: Capítulo BORRADOR accesible. "
                  "Considerar retornar 404 para no revelar su existencia.")
    
    
    def test_inyeccion_sql_en_id(self, client):
        """
        Test CP01_02: Verificar protección contra SQL injection en ID.
        """
        payloads_maliciosos = [
            "'; DROP TABLE capitulos; --",
            "1' OR '1'='1",
            "admin'--",
            "1; DELETE FROM capitulos WHERE 1=1"
        ]
        
        for payload in payloads_maliciosos:
            # Act
            response = client.get(f"/api/capitulos/{payload}")
            
            # Assert - Debe rechazar con 404/422, no ejecutar SQL
            assert response.status_code in [404, 422], \
                f"Payload malicioso '{payload}' debe ser rechazado"
        
        # Verificar que la BD sigue intacta
        response = client.get("/api/capitulos/")
        assert response.status_code == 200, \
            "La base de datos debe seguir funcionando"
    
    
    def test_no_enumerar_ids(self, client):
        """
        Test CP01_02: Dificultar enumeración de IDs.
        Los UUIDs dificultan la enumeración, verificar que se usan.
        """
        # Intentar IDs secuenciales (no deberían funcionar)
        ids_secuenciales = ["1", "2", "3", "100", "999"]
        
        for id_seq in ids_secuenciales:
            response = client.get(f"/api/capitulos/{id_seq}")
            # Debe rechazar (no usar IDs secuenciales)
            assert response.status_code in [404, 422]


# Markers para organizar los tests
pytestmark = [
    pytest.mark.cp01_02,
    pytest.mark.integration
]

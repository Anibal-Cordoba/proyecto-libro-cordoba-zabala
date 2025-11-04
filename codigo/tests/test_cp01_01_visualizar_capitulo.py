"""
CP01_01 — Visualizar capítulo publicado (éxito)
================================================

Test Case: CP01_01
Caso de Uso Relacionado: CU_01 Visualizar contenido
Descripción: Accede a un capítulo existente en estado publicado.

Área Funcional: Contenidos
Funcionalidad: Lectura de capítulo

Datos de Entrada: abrir /capitulos/{id} con id válido y publicado.

Resultado Esperado:
- Se muestran título, número e introducción (y el resto de campos definidos)
- Se registra la visualización si aplica
- Status code 200 OK
- Datos completos del capítulo

Requerimientos de Ambiente:
- BD con al menos un capítulo de prueba en estado PUBLICADO
"""

import pytest
from fastapi import status


class TestCP01_01_VisualizarCapituloPublicado:
    """
    Suite de tests para el caso de prueba CP01_01.
    Verifica la visualización exitosa de un capítulo publicado.
    """
    
    def test_visualizar_capitulo_publicado_exitoso(self, client, capitulo_publicado):
        """
        Test Principal CP01_01: Visualizar capítulo publicado con éxito.
        
        GIVEN: Existe un capítulo en estado PUBLICADO en la base de datos
        WHEN: Se realiza una petición GET a /capitulos/{id}
        THEN: 
            - Se retorna status 200 OK
            - Se obtienen todos los campos del capítulo
            - El título se muestra correctamente
            - El número se muestra correctamente
            - La introducción se muestra correctamente
            - El estado es PUBLICADO
        """
        # Arrange
        capitulo_id = capitulo_publicado.id_capitulo
        
        # Act
        response = client.get(f"/api/capitulos/{capitulo_id}")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK, \
            "Debe retornar 200 OK al visualizar un capítulo publicado"
        
        data = response.json()
        
        # Verificar que se retornan todos los campos esperados
        assert "id_capitulo" in data, "Debe incluir el ID del capítulo"
        assert "titulo" in data, "Debe incluir el título"
        assert "numero" in data, "Debe incluir el número"
        assert "introduccion" in data, "Debe incluir la introducción"
        assert "tema" in data, "Debe incluir el tema"
        assert "estado" in data, "Debe incluir el estado"
        assert "fecha_creacion" in data, "Debe incluir fecha de creación"
        
        # Verificar los valores específicos
        assert data["id_capitulo"] == capitulo_id, "El ID debe coincidir"
        assert data["titulo"] == capitulo_publicado.titulo, \
            "El título debe mostrarse correctamente"
        assert data["numero"] == capitulo_publicado.numero, \
            "El número debe mostrarse correctamente"
        assert data["introduccion"] == capitulo_publicado.introduccion, \
            "La introducción debe mostrarse correctamente"
        assert data["tema"] == capitulo_publicado.tema, \
            "El tema debe mostrarse correctamente"
        assert data["estado"] == "PUBLICADO", \
            "El estado debe ser PUBLICADO"
    
    
    def test_visualizar_capitulo_publicado_estructura_respuesta(self, client, capitulo_publicado):
        """
        Test CP01_01 - Validación de Estructura:
        Verifica que la respuesta tenga la estructura correcta según el schema.
        """
        # Act
        response = client.get(f"/api/capitulos/{capitulo_publicado.id_capitulo}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        
        # Validar tipos de datos
        assert isinstance(data["id_capitulo"], str), "ID debe ser string (UUID)"
        assert isinstance(data["titulo"], str), "Título debe ser string"
        assert isinstance(data["numero"], int), "Número debe ser entero"
        assert isinstance(data["tema"], str), "Tema debe ser string"
        assert isinstance(data["estado"], str), "Estado debe ser string"
        
        # Validar que introducción puede ser string o None
        assert data["introduccion"] is None or isinstance(data["introduccion"], str), \
            "Introducción debe ser string o None"
    
    
    def test_visualizar_capitulo_publicado_contenido_correcto(self, client, capitulo_publicado):
        """
        Test CP01_01 - Validación de Contenido:
        Verifica que el contenido retornado sea el esperado.
        """
        # Act
        response = client.get(f"/api/capitulos/{capitulo_publicado.id_capitulo}")
        data = response.json()
        
        # Assert - Verificar contenido específico
        assert data["titulo"] == "Introducción a las Estructuras de Datos"
        assert data["numero"] == 2
        assert data["tema"] == "Algoritmos y Estructuras"
        assert "estructuras de datos" in data["introduccion"].lower()
    
    
    def test_visualizar_multiples_capitulos_publicados(self, client, multiples_capitulos):
        """
        Test CP01_01 - Caso Múltiple:
        Verifica que se puedan visualizar varios capítulos publicados.
        """
        # Filtrar solo los publicados
        publicados = [c for c in multiples_capitulos if c.estado == "PUBLICADO"]
        
        assert len(publicados) >= 2, "Debe haber al menos 2 capítulos publicados"
        
        # Intentar visualizar cada uno
        for capitulo in publicados:
            response = client.get(f"/api/capitulos/{capitulo.id_capitulo}")
            
            assert response.status_code == 200
            data = response.json()
            assert data["estado"] == "PUBLICADO"
            assert data["id_capitulo"] == capitulo.id_capitulo


class TestCP01_01_CasosNegativos:
    """
    Tests de casos negativos relacionados con CP01_01.
    Verifica el comportamiento cuando las condiciones no son óptimas.
    """
    
    def test_visualizar_capitulo_inexistente(self, client):
        """
        Test CP01_01 - Caso Negativo:
        Intenta visualizar un capítulo que no existe.
        """
        # Act
        response = client.get("/api/capitulos/00000000-0000-0000-0000-000000000000")
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND, \
            "Debe retornar 404 cuando el capítulo no existe"
        
        data = response.json()
        assert "detail" in data, "Debe incluir un mensaje de error"
    
    
    def test_visualizar_capitulo_id_invalido(self, client):
        """
        Test CP01_01 - Caso Negativo:
        Intenta visualizar con un ID inválido.
        """
        # Act
        response = client.get("/api/capitulos/id-invalido-123")
        
        # Assert
        # Puede ser 404 (no encontrado) o 422 (validación)
        assert response.status_code in [404, 422]
    
    
    def test_visualizar_capitulo_borrador(self, client, capitulo_borrador):
        """
        Test CP01_01 - Caso Especial:
        Verifica qué sucede al intentar visualizar un capítulo en BORRADOR.
        
        Nota: Actualmente el endpoint retorna el capítulo independientemente 
        del estado. En una implementación futura podría restringirse.
        """
        # Act
        response = client.get(f"/api/capitulos/{capitulo_borrador.id_capitulo}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["estado"] == "BORRADOR"
        
        # Documentar comportamiento actual
        # TODO: Considerar si se debe restringir acceso a capítulos no publicados


class TestCP01_01_Integracion:
    """
    Tests de integración para CP01_01.
    Verifica el flujo completo de visualización.
    """
    
    def test_flujo_completo_listar_y_visualizar(self, client, capitulo_publicado):
        """
        Test CP01_01 - Integración:
        Flujo completo: listar capítulos y luego visualizar uno específico.
        """
        # Step 1: Listar capítulos
        response = client.get("/api/capitulos/")
        assert response.status_code == 200
        capitulos = response.json()
        assert len(capitulos) > 0
        
        # Step 2: Obtener ID del primer capítulo publicado
        publicados = [c for c in capitulos if c["estado"] == "PUBLICADO"]
        assert len(publicados) > 0, "Debe haber al menos un capítulo publicado"
        
        primer_publicado = publicados[0]
        
        # Step 3: Visualizar ese capítulo específico
        response = client.get(f"/api/capitulos/{primer_publicado['id_capitulo']}")
        assert response.status_code == 200
        
        detalle = response.json()
        assert detalle["id_capitulo"] == primer_publicado["id_capitulo"]
        assert detalle["titulo"] == primer_publicado["titulo"]
    
    
    def test_visualizar_capitulo_con_contenido(self, client, capitulo_con_contenido):
        """
        Test CP01_01 - Integración con Contenido:
        Verifica visualización de capítulo que tiene contenido asociado.
        """
        # Act
        response = client.get(f"/api/capitulos/{capitulo_con_contenido.id_capitulo}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["estado"] == "PUBLICADO"
        
        # El capítulo debe tener uniones con contenido
        assert len(capitulo_con_contenido.uniones) > 0, \
            "El capítulo debe tener contenido asociado"


class TestCP01_01_Performance:
    """
    Tests de rendimiento para CP01_01.
    Verifica que la visualización sea eficiente.
    """
    
    def test_tiempo_respuesta_visualizacion(self, client, capitulo_publicado):
        """
        Test CP01_01 - Performance:
        Verifica que el tiempo de respuesta sea aceptable.
        """
        import time
        
        # Act
        inicio = time.time()
        response = client.get(f"/api/capitulos/{capitulo_publicado.id_capitulo}")
        tiempo_respuesta = time.time() - inicio
        
        # Assert
        assert response.status_code == 200
        assert tiempo_respuesta < 1.0, \
            f"La respuesta debe ser menor a 1 segundo. Actual: {tiempo_respuesta:.3f}s"
    
    
    def test_multiples_visualizaciones_simultaneas(self, client, multiples_capitulos):
        """
        Test CP01_01 - Performance:
        Verifica que se puedan realizar múltiples visualizaciones.
        """
        import time
        
        publicados = [c for c in multiples_capitulos if c.estado == "PUBLICADO"]
        
        # Act
        inicio = time.time()
        for capitulo in publicados:
            response = client.get(f"/api/capitulos/{capitulo.id_capitulo}")
            assert response.status_code == 200
        
        tiempo_total = time.time() - inicio
        
        # Assert
        tiempo_promedio = tiempo_total / len(publicados)
        assert tiempo_promedio < 0.5, \
            f"Tiempo promedio por visualización debe ser < 0.5s. Actual: {tiempo_promedio:.3f}s"


class TestCP01_01_Regresion:
    """
    Tests de regresión para CP01_01.
    Verifica que funcionalidades previas sigan funcionando.
    """
    
    def test_endpoint_mantiene_retrocompatibilidad(self, client, capitulo_publicado):
        """
        Test CP01_01 - Regresión:
        Verifica que el endpoint mantenga la estructura de respuesta esperada.
        """
        # Act
        response = client.get(f"/api/capitulos/{capitulo_publicado.id_capitulo}")
        
        # Assert
        data = response.json()
        
        # Campos obligatorios que siempre deben existir
        campos_obligatorios = [
            "id_capitulo", "titulo", "numero", "tema", "estado"
        ]
        
        for campo in campos_obligatorios:
            assert campo in data, \
                f"Campo obligatorio '{campo}' debe estar presente en la respuesta"
    
    
    def test_estado_publicado_no_cambia_al_visualizar(self, client, capitulo_publicado, test_db_session):
        """
        Test CP01_01 - Regresión:
        Verifica que visualizar un capítulo no cambie su estado.
        """
        # Arrange
        estado_inicial = capitulo_publicado.estado
        
        # Act
        response = client.get(f"/api/capitulos/{capitulo_publicado.id_capitulo}")
        
        # Assert
        assert response.status_code == 200
        
        # Refrescar desde BD
        test_db_session.refresh(capitulo_publicado)
        
        assert capitulo_publicado.estado == estado_inicial, \
            "El estado no debe cambiar al visualizar"
        assert capitulo_publicado.estado == "PUBLICADO"

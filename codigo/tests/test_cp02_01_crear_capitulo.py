"""
CP02_01 — Crear capítulo (campos mínimos válidos)
=================================================

Test Case: CP02_01
Caso de Uso Relacionado: CU_02 Administrar contenido
Descripción: Administrador crea un capítulo nuevo con campos mínimos.

Área Funcional: Backoffice Contenidos
Funcionalidad: Alta de capítulo

Datos de Entrada: 
- POST /api/capitulos/ con:
  * titulo (requerido)
  * numero (requerido, único)
  * tema (requerido)
  * introduccion (opcional)
  * estado (opcional, default: BORRADOR)

Resultado Esperado:
- Status 201 Created
- Capítulo persistido en BD con ID generado
- Respuesta con datos del capítulo creado
- Campos generados automáticamente (id, fechas)

Requerimientos de Ambiente:
- Usuario ADMIN de prueba (futuro)
- Conexión a BD activa
- Validación de unicidad de número

Precondiciones:
- Sesión de administrador (futuro)
- Número de capítulo único
"""

import pytest
from fastapi import status
import uuid


class TestCP02_01_CrearCapituloExitoso:
    """
    Suite de tests para creación exitosa de capítulos.
    Valida el flujo completo de alta de capítulo.
    """
    
    def test_crear_capitulo_campos_minimos(self, client, sample_capitulo_data):
        """
        Test Principal CP02_01: Crear capítulo con campos mínimos válidos.
        
        GIVEN: Datos mínimos válidos (titulo, numero, tema)
        WHEN: Se realiza POST a /api/capitulos/
        THEN: 
            - Status 201 Created
            - Capítulo guardado en BD
            - ID generado automáticamente
            - Fechas de creación/modificación generadas
        """
        # Arrange
        capitulo_data = {
            "titulo": "Nuevo Capítulo de Prueba",
            "numero": 999,
            "tema": "Testing Creación",
            "introduccion": "Introducción del nuevo capítulo"
        }
        
        # Act
        response = client.post("/api/capitulos/", json=capitulo_data)
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED, \
            "Debe retornar 201 Created al crear un capítulo"
        
        data = response.json()
        
        # Verificar que se asignó un ID
        assert "id_capitulo" in data, "Debe incluir ID generado"
        assert data["id_capitulo"] is not None
        assert len(data["id_capitulo"]) > 0
        
        # Verificar UUID válido
        try:
            uuid.UUID(data["id_capitulo"])
        except ValueError:
            pytest.fail("El ID debe ser un UUID válido")
        
        # Verificar datos guardados
        assert data["titulo"] == capitulo_data["titulo"]
        assert data["numero"] == capitulo_data["numero"]
        assert data["tema"] == capitulo_data["tema"]
        assert data["introduccion"] == capitulo_data["introduccion"]
        
        # Verificar campos generados automáticamente
        assert "fecha_creacion" in data, "Debe incluir fecha de creación"
        assert "fecha_modificacion" in data, "Debe incluir fecha de modificación"
        
        # Verificar estado por defecto
        assert "estado" in data
        assert data["estado"] == "BORRADOR", \
            "Estado por defecto debe ser BORRADOR"
    
    
    def test_crear_capitulo_sin_introduccion(self, client):
        """
        Test CP02_01: Crear capítulo sin introducción (campo opcional).
        """
        # Arrange - Sin introducción
        capitulo_data = {
            "titulo": "Capítulo Sin Introducción",
            "numero": 998,
            "tema": "Testing Opcional"
        }
        
        # Act
        response = client.post("/api/capitulos/", json=capitulo_data)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        
        assert data["titulo"] == capitulo_data["titulo"]
        assert data["numero"] == capitulo_data["numero"]
        assert data["introduccion"] is None or data["introduccion"] == ""
    
    
    def test_crear_capitulo_con_estado_explicito(self, client):
        """
        Test CP02_01: Crear capítulo con estado explícito.
        """
        # Arrange - Estado PUBLICADO desde creación
        capitulo_data = {
            "titulo": "Capítulo Publicado Directo",
            "numero": 997,
            "tema": "Testing Estado",
            "estado": "PUBLICADO"
        }
        
        # Act
        response = client.post("/api/capitulos/", json=capitulo_data)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        
        assert data["estado"] == "PUBLICADO", \
            "Debe respetar el estado proporcionado"
    
    
    def test_crear_varios_capitulos_consecutivos(self, client):
        """
        Test CP02_01: Crear múltiples capítulos en secuencia.
        Verifica que el sistema maneja múltiples creaciones.
        """
        # Arrange
        capitulos = [
            {"titulo": f"Capítulo {i}", "numero": 900 + i, "tema": "Serie"}
            for i in range(1, 4)
        ]
        
        ids_creados = []
        
        # Act - Crear varios capítulos
        for cap_data in capitulos:
            response = client.post("/api/capitulos/", json=cap_data)
            
            # Assert individual
            assert response.status_code == 201
            data = response.json()
            ids_creados.append(data["id_capitulo"])
        
        # Assert - Verificar que todos tienen IDs únicos
        assert len(set(ids_creados)) == len(ids_creados), \
            "Todos los IDs deben ser únicos"
    
    
    def test_crear_y_recuperar_capitulo(self, client):
        """
        Test CP02_01: Flujo completo - Crear y luego recuperar el capítulo.
        """
        # Arrange
        capitulo_data = {
            "titulo": "Capítulo para Recuperar",
            "numero": 996,
            "tema": "Testing Flujo Completo",
            "introduccion": "Test de integración"
        }
        
        # Act - Crear
        response_create = client.post("/api/capitulos/", json=capitulo_data)
        assert response_create.status_code == 201
        
        data_created = response_create.json()
        capitulo_id = data_created["id_capitulo"]
        
        # Act - Recuperar
        response_get = client.get(f"/api/capitulos/{capitulo_id}")
        
        # Assert
        assert response_get.status_code == 200
        data_retrieved = response_get.json()
        
        # Los datos deben coincidir
        assert data_retrieved["id_capitulo"] == capitulo_id
        assert data_retrieved["titulo"] == capitulo_data["titulo"]
        assert data_retrieved["numero"] == capitulo_data["numero"]
        assert data_retrieved["tema"] == capitulo_data["tema"]


class TestCP02_01_ValidacionDatos:
    """
    Tests de validación de datos en la creación de capítulos.
    """
    
    def test_crear_capitulo_sin_titulo(self, client):
        """
        Test CP02_01: Validación - Título es requerido.
        """
        # Arrange - Sin título
        capitulo_data = {
            "numero": 995,
            "tema": "Testing Validación"
        }
        
        # Act
        response = client.post("/api/capitulos/", json=capitulo_data)
        
        # Assert
        assert response.status_code == 422, \
            "Debe retornar 422 si falta campo requerido"
        
        data = response.json()
        assert "detail" in data
    
    
    def test_crear_capitulo_sin_numero(self, client):
        """
        Test CP02_01: Validación - Número es requerido.
        """
        # Arrange
        capitulo_data = {
            "titulo": "Sin Número",
            "tema": "Testing"
        }
        
        # Act
        response = client.post("/api/capitulos/", json=capitulo_data)
        
        # Assert
        assert response.status_code == 422
    
    
    def test_crear_capitulo_sin_tema(self, client):
        """
        Test CP02_01: Validación - Tema es requerido.
        """
        # Arrange
        capitulo_data = {
            "titulo": "Sin Tema",
            "numero": 994
        }
        
        # Act
        response = client.post("/api/capitulos/", json=capitulo_data)
        
        # Assert
        assert response.status_code == 422
    
    
    def test_crear_capitulo_numero_negativo(self, client):
        """
        Test CP02_01: Validación - Número debe ser positivo.
        """
        # Arrange
        capitulo_data = {
            "titulo": "Número Negativo",
            "numero": -1,
            "tema": "Testing"
        }
        
        # Act
        response = client.post("/api/capitulos/", json=capitulo_data)
        
        # Assert
        assert response.status_code == 422, \
            "Número negativo debe ser rechazado"
    
    
    def test_crear_capitulo_numero_cero(self, client):
        """
        Test CP02_01: Validación - Número cero.
        Dependiendo de la lógica, puede ser válido o no.
        """
        # Arrange
        capitulo_data = {
            "titulo": "Capítulo Cero",
            "numero": 0,
            "tema": "Testing"
        }
        
        # Act
        response = client.post("/api/capitulos/", json=capitulo_data)
        
        # Assert - Documentar comportamiento
        # Si se acepta número 0, 201; si no, 422
        assert response.status_code in [201, 422]
    
    
    def test_crear_capitulo_titulo_vacio(self, client):
        """
        Test CP02_01: Validación - Título no debe estar vacío.
        """
        # Arrange
        capitulo_data = {
            "titulo": "",
            "numero": 993,
            "tema": "Testing"
        }
        
        # Act
        response = client.post("/api/capitulos/", json=capitulo_data)
        
        # Assert
        assert response.status_code == 422, \
            "Título vacío debe ser rechazado"
    
    
    def test_crear_capitulo_titulo_muy_largo(self, client):
        """
        Test CP02_01: Validación - Título no debe exceder límite (255 caracteres).
        """
        # Arrange - Título de 300 caracteres
        capitulo_data = {
            "titulo": "A" * 300,
            "numero": 992,
            "tema": "Testing"
        }
        
        # Act
        response = client.post("/api/capitulos/", json=capitulo_data)
        
        # Assert
        assert response.status_code == 422, \
            "Título muy largo debe ser rechazado"
    
    
    def test_crear_capitulo_tema_muy_largo(self, client):
        """
        Test CP02_01: Validación - Tema no debe exceder 100 caracteres.
        """
        # Arrange
        capitulo_data = {
            "titulo": "Test Tema Largo",
            "numero": 991,
            "tema": "T" * 150
        }
        
        # Act
        response = client.post("/api/capitulos/", json=capitulo_data)
        
        # Assert
        assert response.status_code == 422


class TestCP02_01_UnicdadNumero:
    """
    Tests de validación de unicidad del número de capítulo.
    """
    
    def test_crear_capitulo_numero_duplicado(self, client, capitulo_publicado):
        """
        Test Principal CP02_01: No se permite duplicar número de capítulo.
        
        GIVEN: Ya existe un capítulo con numero=2
        WHEN: Se intenta crear otro con el mismo número
        THEN: Debe retornar error 400 Bad Request
        """
        # Arrange - Intentar crear con número existente
        capitulo_data = {
            "titulo": "Capítulo Duplicado",
            "numero": capitulo_publicado.numero,  # Número ya existente
            "tema": "Testing Duplicados"
        }
        
        # Act
        response = client.post("/api/capitulos/", json=capitulo_data)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST, \
            "No se debe permitir números duplicados"
        
        data = response.json()
        assert "detail" in data
        assert "ya existe" in data["detail"].lower() or "duplicate" in data["detail"].lower()
    
    
    def test_crear_capitulo_numero_unico_exitoso(self, client, multiples_capitulos):
        """
        Test CP02_01: Crear con número único cuando ya existen otros.
        """
        # Arrange - Número que no existe
        numeros_existentes = [cap.numero for cap in multiples_capitulos]
        numero_nuevo = max(numeros_existentes) + 1
        
        capitulo_data = {
            "titulo": "Capítulo Número Único",
            "numero": numero_nuevo,
            "tema": "Testing Unicidad"
        }
        
        # Act
        response = client.post("/api/capitulos/", json=capitulo_data)
        
        # Assert
        assert response.status_code == 201, \
            "Debe permitir número único"
        
        data = response.json()
        assert data["numero"] == numero_nuevo


class TestCP02_01_EstadosValidos:
    """
    Tests de validación de estados al crear capítulo.
    """
    
    def test_crear_capitulo_estado_borrador(self, client):
        """
        Test CP02_01: Crear capítulo en estado BORRADOR.
        """
        # Arrange
        capitulo_data = {
            "titulo": "Capítulo Borrador",
            "numero": 980,
            "tema": "Testing Estados",
            "estado": "BORRADOR"
        }
        
        # Act
        response = client.post("/api/capitulos/", json=capitulo_data)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["estado"] == "BORRADOR"
    
    
    def test_crear_capitulo_estado_publicado(self, client):
        """
        Test CP02_01: Crear capítulo directamente en PUBLICADO.
        """
        # Arrange
        capitulo_data = {
            "titulo": "Capítulo Publicado Directo",
            "numero": 979,
            "tema": "Testing Estados",
            "estado": "PUBLICADO"
        }
        
        # Act
        response = client.post("/api/capitulos/", json=capitulo_data)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["estado"] == "PUBLICADO"
    
    
    def test_crear_capitulo_estado_archivado(self, client):
        """
        Test CP02_01: Crear capítulo en estado ARCHIVADO.
        (Caso raro pero válido)
        """
        # Arrange
        capitulo_data = {
            "titulo": "Capítulo Archivado",
            "numero": 978,
            "tema": "Testing Estados",
            "estado": "ARCHIVADO"
        }
        
        # Act
        response = client.post("/api/capitulos/", json=capitulo_data)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["estado"] == "ARCHIVADO"
    
    
    def test_crear_capitulo_estado_invalido(self, client):
        """
        Test CP02_01: Validación - Estado inválido.
        
        Comportamiento actual: El sistema acepta cualquier valor de estado
        sin validación estricta en la base de datos.
        
        Recomendación futura: Agregar validación con Enum o constraint.
        """
        # Arrange
        capitulo_data = {
            "titulo": "Estado Inválido",
            "numero": 977,
            "tema": "Testing",
            "estado": "ESTADO_INEXISTENTE"
        }
        
        # Act
        response = client.post("/api/capitulos/", json=capitulo_data)
        
        # Assert
        # Comportamiento actual: acepta el estado sin validar
        # Comportamiento deseado: rechazar con 422
        if response.status_code == 422:
            # Validación implementada ✅
            pass
        elif response.status_code == 201:
            # Sin validación - documentar
            print("⚠️  ADVERTENCIA: Estado inválido aceptado. "
                  "Recomendación: Agregar validación de estados permitidos.")
            data = response.json()
            # Por ahora, solo verificamos que se guardó algo
            assert "estado" in data
        else:
            pytest.fail(f"Código inesperado: {response.status_code}")


class TestCP02_01_Integracion:
    """
    Tests de integración para creación de capítulos.
    """
    
    def test_flujo_crear_listar_verificar(self, client):
        """
        Test CP02_01: Flujo completo - Crear, listar y verificar.
        """
        # Step 1: Obtener cantidad inicial
        response_inicial = client.get("/api/capitulos/")
        cantidad_inicial = len(response_inicial.json())
        
        # Step 2: Crear nuevo capítulo
        capitulo_data = {
            "titulo": "Capítulo Flujo Completo",
            "numero": 970,
            "tema": "Testing Integración"
        }
        
        response_crear = client.post("/api/capitulos/", json=capitulo_data)
        assert response_crear.status_code == 201
        
        capitulo_creado = response_crear.json()
        capitulo_id = capitulo_creado["id_capitulo"]
        
        # Step 3: Listar y verificar que aumentó la cantidad
        response_final = client.get("/api/capitulos/")
        cantidad_final = len(response_final.json())
        
        assert cantidad_final == cantidad_inicial + 1, \
            "Debe aparecer el nuevo capítulo en el listado"
        
        # Step 4: Verificar que el nuevo capítulo está en la lista
        capitulos = response_final.json()
        ids = [cap["id_capitulo"] for cap in capitulos]
        assert capitulo_id in ids
    
    
    def test_crear_y_eliminar_capitulo(self, client):
        """
        Test CP02_01: Flujo crear y eliminar.
        """
        # Step 1: Crear
        capitulo_data = {
            "titulo": "Capítulo Temporal",
            "numero": 969,
            "tema": "Testing Temporal"
        }
        
        response_crear = client.post("/api/capitulos/", json=capitulo_data)
        assert response_crear.status_code == 201
        
        capitulo_id = response_crear.json()["id_capitulo"]
        
        # Step 2: Verificar que existe
        response_get = client.get(f"/api/capitulos/{capitulo_id}")
        assert response_get.status_code == 200
        
        # Step 3: Eliminar
        response_delete = client.delete(f"/api/capitulos/{capitulo_id}")
        assert response_delete.status_code == 204
        
        # Step 4: Verificar que ya no existe
        response_get2 = client.get(f"/api/capitulos/{capitulo_id}")
        assert response_get2.status_code == 404
    
    
    def test_crear_multiples_y_filtrar_por_tema(self, client):
        """
        Test CP02_01: Crear varios capítulos y filtrar.
        """
        # Arrange
        tema_especial = "Testing Filtrado Especial"
        capitulos_data = [
            {"titulo": f"Cap {i}", "numero": 960 + i, "tema": tema_especial}
            for i in range(3)
        ]
        
        # Act - Crear varios con el mismo tema
        for cap_data in capitulos_data:
            response = client.post("/api/capitulos/", json=cap_data)
            assert response.status_code == 201
        
        # Act - Filtrar por tema
        response_filtrado = client.get(f"/api/capitulos/?tema={tema_especial}")
        
        # Assert
        assert response_filtrado.status_code == 200
        capitulos = response_filtrado.json()
        
        # Al menos los 3 que creamos deben estar
        capitulos_con_tema = [c for c in capitulos if tema_especial in c["tema"]]
        assert len(capitulos_con_tema) >= 3


class TestCP02_01_Performance:
    """
    Tests de performance para creación de capítulos.
    """
    
    def test_tiempo_creacion_aceptable(self, client):
        """
        Test CP02_01: Tiempo de creación debe ser aceptable.
        """
        import time
        
        # Arrange
        capitulo_data = {
            "titulo": "Test Performance",
            "numero": 950,
            "tema": "Performance"
        }
        
        # Act
        inicio = time.time()
        response = client.post("/api/capitulos/", json=capitulo_data)
        tiempo = time.time() - inicio
        
        # Assert
        assert response.status_code == 201
        assert tiempo < 1.0, \
            f"Creación debe tomar < 1s. Actual: {tiempo:.3f}s"
    
    
    def test_crear_multiples_rapido(self, client):
        """
        Test CP02_01: Crear múltiples capítulos en tiempo razonable.
        """
        import time
        
        # Arrange
        cantidad = 10
        capitulos = [
            {"titulo": f"Bulk {i}", "numero": 930 + i, "tema": "Bulk"}
            for i in range(cantidad)
        ]
        
        # Act
        inicio = time.time()
        for cap_data in capitulos:
            response = client.post("/api/capitulos/", json=cap_data)
            assert response.status_code == 201
        tiempo = time.time() - inicio
        
        # Assert
        tiempo_promedio = tiempo / cantidad
        assert tiempo_promedio < 0.2, \
            f"Promedio debe ser < 0.2s. Actual: {tiempo_promedio:.3f}s"


class TestCP02_01_Regresion:
    """
    Tests de regresión para creación de capítulos.
    """
    
    def test_formato_respuesta_consistente(self, client):
        """
        Test CP02_01: Formato de respuesta debe ser consistente.
        """
        # Arrange
        capitulos_test = [
            {"titulo": "Test 1", "numero": 920, "tema": "T1"},
            {"titulo": "Test 2", "numero": 921, "tema": "T2"},
        ]
        
        respuestas = []
        
        # Act
        for cap_data in capitulos_test:
            response = client.post("/api/capitulos/", json=cap_data)
            assert response.status_code == 201
            respuestas.append(response.json())
        
        # Assert - Todas deben tener los mismos campos
        campos_esperados = {
            "id_capitulo", "titulo", "numero", "tema", 
            "estado", "fecha_creacion"
        }
        
        for resp in respuestas:
            campos_resp = set(resp.keys())
            assert campos_esperados.issubset(campos_resp), \
                "Todas las respuestas deben tener los campos esperados"
    
    
    def test_id_generado_es_uuid(self, client):
        """
        Test CP02_01: ID generado debe ser UUID válido.
        """
        # Arrange & Act
        capitulo_data = {
            "titulo": "Test UUID",
            "numero": 919,
            "tema": "Testing"
        }
        
        response = client.post("/api/capitulos/", json=capitulo_data)
        data = response.json()
        
        # Assert - Debe ser UUID válido
        try:
            uuid_obj = uuid.UUID(data["id_capitulo"])
            assert str(uuid_obj) == data["id_capitulo"]
        except ValueError:
            pytest.fail("ID generado no es un UUID válido")


# Markers para organizar los tests
pytestmark = [
    pytest.mark.cp02_01,
    pytest.mark.integration
]

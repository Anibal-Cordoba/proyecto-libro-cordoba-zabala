#!/usr/bin/env python3
"""
Script de prueba de la API
===========================
Verifica que la API esté funcionando correctamente
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Prueba el endpoint de salud"""
    print("🔍 Probando health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print(f"✅ Health check OK: {response.json()}")
            return True
        else:
            print(f"❌ Health check falló: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print("   ¿Está el servidor corriendo? Ejecuta: bash iniciar_api.sh")
        return False


def test_crear_capitulo():
    """Prueba crear un capítulo"""
    print("\n🔍 Probando crear capítulo...")
    
    capitulo_data = {
        "titulo": "Capítulo de Prueba",
        "numero": 999,
        "tema": "Testing",
        "introduccion": "Este es un capítulo de prueba automática"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/capitulos/",
            json=capitulo_data
        )
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Capítulo creado: {data['titulo']}")
            print(f"   ID: {data['id_capitulo']}")
            return data['id_capitulo']
        else:
            print(f"❌ Error al crear: {response.status_code}")
            print(f"   {response.json()}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_listar_capitulos():
    """Prueba listar capítulos"""
    print("\n🔍 Probando listar capítulos...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/capitulos/")
        
        if response.status_code == 200:
            capitulos = response.json()
            print(f"✅ Capítulos encontrados: {len(capitulos)}")
            for cap in capitulos[:3]:  # Mostrar primeros 3
                print(f"   - Cap {cap['numero']}: {cap['titulo']}")
            return True
        else:
            print(f"❌ Error al listar: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_obtener_capitulo(capitulo_id):
    """Prueba obtener un capítulo específico"""
    if not capitulo_id:
        return False
        
    print(f"\n🔍 Probando obtener capítulo {capitulo_id}...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/capitulos/{capitulo_id}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Capítulo obtenido: {data['titulo']}")
            return True
        else:
            print(f"❌ Error al obtener: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_eliminar_capitulo(capitulo_id):
    """Prueba eliminar un capítulo"""
    if not capitulo_id:
        return False
        
    print(f"\n🔍 Probando eliminar capítulo {capitulo_id}...")
    
    try:
        response = requests.delete(f"{BASE_URL}/api/capitulos/{capitulo_id}")
        
        if response.status_code == 204:
            print(f"✅ Capítulo eliminado exitosamente")
            return True
        else:
            print(f"❌ Error al eliminar: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Ejecuta todas las pruebas"""
    print("=" * 60)
    print("  PRUEBAS DE LA API")
    print("=" * 60)
    
    # Health check
    if not test_health():
        return
    
    # Crear capítulo
    capitulo_id = test_crear_capitulo()
    
    # Listar capítulos
    test_listar_capitulos()
    
    # Obtener capítulo
    test_obtener_capitulo(capitulo_id)
    
    # Eliminar capítulo
    test_eliminar_capitulo(capitulo_id)
    
    print("\n" + "=" * 60)
    print("  PRUEBAS COMPLETADAS")
    print("=" * 60)
    print("\n💡 Visita http://localhost:8000 en tu navegador")
    print("   para ver la interfaz web")


if __name__ == "__main__":
    main()

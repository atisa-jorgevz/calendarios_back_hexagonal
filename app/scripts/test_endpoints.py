# app/scripts/test_endpoints.py

import requests

BASE = "http://localhost:8000"
PROCESOS_URL = f"{BASE}/v1/procesos"
HITOS_URL = f"{BASE}/v1/hitos"
PHM_URL = f"{BASE}/v1/proceso-hitos"
PLANTILLAS_URL = f"{BASE}/v1/plantillas"

def test_crear_proceso():
    payload = {
        "nombre": "Proceso Test API",
        "frecuencia": 1,
        "temporalidad": "mes",
        "inicia_dia_1": True,
        "fecha_inicio": "2023-01-01",
        "fecha_fin": "2023-12-31",
        "descripcion": "Proceso de prueba con test"
    }
    r = requests.post(PROCESOS_URL, json=payload)
    assert r.status_code == 200, f"Error al crear proceso: {r.text}"
    data = r.json()
    print(f"✅ POST /procesos: {data}")
    return data["id"]

def test_crear_hito():
    payload = {
        "nombre": "Hito Test",
        "frecuencia": 1,
        "temporalidad": "mes",
        "fecha_inicio": "2023-01-01"
    }
    r = requests.post(HITOS_URL, json=payload)
    assert r.status_code == 200, f"Error al crear hito: {r.text}"
    data = r.json()
    print(f"✅ POST /hitos: {data}")
    return data["id"]

def test_listar(url, entidad):
    r = requests.get(url)
    assert r.status_code == 200, f"Error al listar {entidad}: {r.text}"
    print(f"✅ GET /{entidad}: {len(r.json())} encontrados")

def test_obtener(url, entidad, id_):
    r = requests.get(f"{url}/{id_}")
    assert r.status_code == 200, f"{entidad} no encontrado: {r.text}"
    print(f"✅ GET /{entidad}/{id_}: {r.json()}")

def test_actualizar(url, entidad, id_, data):
    r = requests.put(f"{url}/{id_}", json=data)
    assert r.status_code == 200, f"Error al actualizar {entidad}: {r.text}"
    print(f"✅ PUT /{entidad}/{id_}: {r.json()}")

def test_eliminar(url, entidad, id_):
    r = requests.delete(f"{url}/{id_}")
    assert r.status_code == 200, f"Error al eliminar {entidad}: {r.text}"
    print(f"✅ DELETE /{entidad}/{id_}: {r.json()}")

def test_crear_plantilla():
    payload = {
        "nombre": "Plantilla Test API",
        "descripcion": "Plantilla generada desde test"
    }
    r = requests.post(PLANTILLAS_URL, json=payload)
    assert r.status_code == 200, f"Error al crear plantilla: {r.text}"
    data = r.json()
    print(f"✅ POST /plantillas: {data}")
    return data["id"]

def test_listar_plantillas():
    r = requests.get(PLANTILLAS_URL)
    assert r.status_code == 200, f"Error al listar plantillas: {r.text}"
    print(f"✅ GET /plantillas: {len(r.json())} encontradas")

def test_obtener_plantilla(id_):
    r = requests.get(f"{PLANTILLAS_URL}/{id_}")
    assert r.status_code == 200, f"Plantilla no encontrada: {r.text}"
    print(f"✅ GET /plantillas/{id_}: {r.json()}")

def test_actualizar_plantilla(id_):
    payload = {
        "nombre": "Plantilla Test Modificada",
        "descripcion": "Descripción modificada"
    }
    r = requests.put(f"{PLANTILLAS_URL}/{id_}", json=payload)
    assert r.status_code == 200, f"Error al actualizar plantilla: {r.text}"
    print(f"✅ PUT /plantillas/{id_}: {r.json()}")

def test_eliminar_plantilla(id_):
    r = requests.delete(f"{PLANTILLAS_URL}/{id_}")
    assert r.status_code == 200, f"Error al eliminar plantilla: {r.text}"
    print(f"✅ DELETE /plantillas/{id_}: {r.json()}")

def test_asociar_proceso_hito(proceso_id, hito_id):
    payload = {
        "id_proceso": proceso_id,
        "id_hito": hito_id
    }
    r = requests.post(PHM_URL, json=payload)
    assert r.status_code == 200, f"Error al asociar proceso-hito: {r.text}"
    data = r.json()    
    print(f"✅ POST /proceso-hitos: {data}")
    return data["id"]
def test_eliminar_procesos_hitos(id_):
    r = requests.delete(f"{PHM_URL}/{id_}")
    assert r.status_code == 200, f"Error al eliminar proceso-hito: {r.text}"
    print(f"✅ DELETE /proceso-hitos/{id_}: {r.json()}")

def main():
        # Asociar proceso con hito maestro
    proceso_id = test_crear_proceso()
    hito_id = test_crear_hito()

    id_relacion_proceso_hito = test_asociar_proceso_hito(proceso_id, hito_id)

    # Listar relaciones
    test_listar(PHM_URL, "proceso-hitos")

    # Eliminar relación
    test_eliminar_procesos_hitos(id_relacion_proceso_hito)


    id_plantilla = test_crear_plantilla()
    test_listar_plantillas()
    test_obtener_plantilla(id_plantilla)
    test_actualizar_plantilla(id_plantilla)
    test_eliminar_plantilla(id_plantilla)
    print("💥 TEST DE PLANTILLAS FINALIZADO 💥")


    

    print("\n💥 TODOS LOS TESTS FINALIZADOS CON ÉXITO 💥")

if __name__ == "__main__":
    main()

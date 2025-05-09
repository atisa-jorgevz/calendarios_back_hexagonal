# app/scripts/test_endpoints.py

import requests

BASE = "http://localhost:8000"
PROCESOS_URL = f"{BASE}/v1/procesos"
HITOS_URL = f"{BASE}/v1/hitos"

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

def main():
        # Asociar proceso con hito maestro
    proceso_id = test_crear_proceso()
    hito_id = test_crear_hito()

    PHM_URL = f"{BASE}/v1/proceso-hitos"
    payload = {
        "id_proceso": proceso_id,
        "id_hito": hito_id
    }
    r = requests.post(PHM_URL, json=payload)
    assert r.status_code == 200, f"Error al asociar proceso-hito: {r.text}"
    phm_id = r.json()["id"]
    print(f"✅ POST /proceso-hitos: {r.json()}")

    # Listar relaciones
    test_listar(PHM_URL, "proceso-hitos")

    # Eliminar relación
    test_eliminar(PHM_URL, "proceso-hitos", phm_id)


    

    print("\n💥 TODOS LOS TESTS FINALIZADOS CON ÉXITO 💥")

if __name__ == "__main__":
    main()

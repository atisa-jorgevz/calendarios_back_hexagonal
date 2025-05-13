# app/scripts/test_endpoints.py

import requests

BASE = "http://localhost:8000"
PROCESOS_URL = f"{BASE}/v1/procesos"
HITOS_URL = f"{BASE}/v1/hitos"
PHM_URL = f"{BASE}/v1/proceso-hitos"
PLANTILLAS_URL = f"{BASE}/v1/plantillas"
RELACIONES_URL = f"{BASE}/v1/plantilla-procesos"
CLIENTES_URL = f"{BASE}/v1/clientes"
CLIENTE_PROCESO_URL = f"{BASE}/v1/cliente-procesos"
CLIENTE_PROCESO_HITO_URL = f"{BASE}/v1/cliente-proceso-hitos"

def test_listar_cliente_procesos():
    r = requests.get(CLIENTE_PROCESO_URL)
    assert r.status_code == 200, f"❌ Error al listar cliente_procesos: {r.text}"
    print(f"✅ GET /cliente-proceso → {len(r.json())} encontrados")

def test_obtener_cliente_proceso_por_id(id_):
    r = requests.get(f"{CLIENTE_PROCESO_URL}/{id_}")
    assert r.status_code == 200, f"❌ cliente_proceso {id_} no encontrado: {r.text}"
    print(f"✅ GET /cliente-proceso/{id_} → {r.json()}")

def test_listar_cliente_proceso_hitos():
    r = requests.get(CLIENTE_PROCESO_HITO_URL)
    assert r.status_code == 200, f"❌ Error al listar cliente_proceso_hito: {r.text}"
    print(f"✅ GET /cliente-proceso-hito → {len(r.json())} encontrados")

def test_obtener_cliente_proceso_hito_por_id(id_):
    r = requests.get(f"{CLIENTE_PROCESO_HITO_URL}/{id_}")
    assert r.status_code == 200, f"❌ cliente_proceso_hito {id_} no encontrado: {r.text}"
    print(f"✅ GET /cliente-proceso-hito/{id_} → {r.json()}")



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

def test_crear_relacion_plantilla_proceso(id_plantilla, id_proceso):
    r = requests.post(RELACIONES_URL, json={"plantilla_id": id_plantilla, "proceso_id": id_proceso})
    assert r.status_code == 200
    print(f"✅ POST /plantilla-procesos: {r.json()}")
    return r.json()["id"]

def test_listar_relaciones():
    r = requests.get(RELACIONES_URL)
    assert r.status_code == 200
    print(f"✅ GET /plantilla-procesos: {len(r.json())} relaciones")

def test_listar_procesos_de_plantilla(id_plantilla):
    r = requests.get(f"{RELACIONES_URL}/plantilla/{id_plantilla}")
    assert r.status_code == 200
    print(f"✅ GET /plantilla-procesos/plantilla/{id_plantilla}: {r.json()}")

def test_eliminar_relacion(id_relacion):
    r = requests.delete(f"{RELACIONES_URL}/{id_relacion}")
    assert r.status_code == 200
    print(f"✅ DELETE /plantilla-procesos/{id_relacion}: {r.json()}")

def test_eliminar_por_plantilla(id_plantilla):
    r = requests.delete(f"{RELACIONES_URL}/plantilla/{id_plantilla}")
    assert r.status_code == 200, f"Error al eliminar relaciones por plantilla: {r.text}"
    print(f"✅ DELETE /plantilla-procesos/plantilla/{id_plantilla}: {r.json()}")

def test_listar_clientes():
    r = requests.get(CLIENTES_URL)
    assert r.status_code == 200, f"Error al listar clientes: {r.text}"
    print(f"✅ GET /clientes: {len(r.json())} encontrados")

def test_buscar_por_nombre(nombre):
    r = requests.get(f"{CLIENTES_URL}/nombre/{nombre}")
    if r.status_code == 404:
        print(f"❌ No se encontraron clientes con nombre: {nombre}")
    else:
        print(f"✅ GET /clientes/nombre/{nombre}: {len(r.json())} encontrados")

def test_buscar_por_cif(cif):
    r = requests.get(f"{CLIENTES_URL}/cif/{cif}")
    if r.status_code == 404:
        print(f"❌ Cliente con CIF {cif} no encontrado")
    else:
        print(f"✅ GET /clientes/cif/{cif}: {r.json()}")


def main():

    test_listar_clientes()
    test_buscar_por_nombre("KIKO")     # Usa un nombre real que sepas que existe
    test_buscar_por_cif("B78491073")     # Cambia por un CIF real para que funcione

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
    id_relacion = test_crear_relacion_plantilla_proceso(id_plantilla, proceso_id)
    test_listar_relaciones()
    test_listar_procesos_de_plantilla(id_plantilla)
    test_eliminar_relacion(id_relacion)
    id_relacion = test_crear_relacion_plantilla_proceso(id_plantilla, proceso_id)
    test_eliminar_por_plantilla(id_plantilla)
    test_eliminar_plantilla(id_plantilla)
    print("💥 TEST DE PLANTILLAS FINALIZADO 💥")
    # Cliente Proceso
    #test_listar_cliente_procesos()
    #test_obtener_cliente_proceso_por_id(6)  # Ajusta el ID si lo necesitas

    # Cliente Proceso Hito
    #test_listar_cliente_proceso_hitos()
    #test_obtener_cliente_proceso_hito_por_id(7)  # Ajusta el ID si lo necesitas

    print("\n💥 TODOS LOS TESTS FINALIZADOS CON ÉXITO 💥")

if __name__ == "__main__":
    main()

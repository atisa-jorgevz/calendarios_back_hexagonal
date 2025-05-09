# app/scripts/mock_data.py

from sqlalchemy.orm import Session
from app.infrastructure.db.database import SessionLocal
from app.infrastructure.db.models import  ProcesoModel
from app.infrastructure.db.models  import HitoModel
from app.infrastructure.db.models import ProcesoHitoMaestroModel
from app.infrastructure.db.models import PlantillaModel

def poblar_datos_mock():
    db: Session = SessionLocal()

    # Limpieza opcional
    # db.query(HitoModel).delete()
    # db.query(ProcesoModel).delete()
    # db.commit()

    # Procesos de prueba
    procesos = [
        ProcesoModel(nombre="Contabilidad NOMINAS", frecuencia=1, temporalidad="mes", inicia_dia_1=True, fecha_inicio="2023-01-01"),
        ProcesoModel(nombre="Facturación BACKOFFICE", frecuencia=2, temporalidad="mes", inicia_dia_1=True, fecha_inicio="2023-01-01"),
        ProcesoModel(nombre="Modelo 190 - 3", frecuencia=1, temporalidad="año", inicia_dia_1=True, fecha_inicio="2023-01-01"),
    ]
    db.add_all(procesos)
    db.commit()

    # Hitos de prueba
    hitos = [
        HitoModel(nombre="Recibir documentos", frecuencia=1, temporalidad="mes", fecha_inicio="2023-01-01", fecha_fin="2023-01-05", obligatorio=1),
        HitoModel(nombre="Cerrar contabilidad", frecuencia=1, temporalidad="mes", fecha_inicio="2023-01-05", fecha_fin="2023-01-10", obligatorio=1),
        HitoModel(nombre="Enviar modelo", frecuencia=1, temporalidad="año", fecha_inicio="2023-01-10", fecha_fin="2023-01-15", obligatorio=1),
    ]
    db.add_all(hitos)
    db.commit()
    db.close()

    print("✅ Procesos y Hitos de prueba insertados correctamente")

def poblar_proceso_hito_maestro_mock():
    db: Session = SessionLocal()

    # Asegúrate de que haya al menos un proceso y un hito
    proceso = db.query(ProcesoModel).first()
    hito = db.query(HitoModel).first()

    if not proceso or not hito:
        print("❌ No hay procesos o hitos para relacionar")
        db.close()
        return

    relacion = ProcesoHitoMaestroModel(id_proceso=proceso.id, id_hito=hito.id)
    db.add(relacion)
    db.commit()
    db.close()
    print("✅ Relación Proceso-Hito insertada")

def poblar_plantillas_mock():
    db: Session = SessionLocal()

    plantillas = [
        PlantillaModel(nombre="Plantilla Contable", descripcion="Para procesos de contabilidad"),
        PlantillaModel(nombre="Plantilla Fiscal", descripcion="Para procesos fiscales"),
        PlantillaModel(nombre="Plantilla General", descripcion="Uso general en clientes")
    ]

    db.add_all(plantillas)
    db.commit()
    db.close()
    print("✅ Plantillas de prueba insertadas correctamente")

if __name__ == "__main__":
    poblar_datos_mock()
    poblar_proceso_hito_maestro_mock()
    poblar_plantillas_mock()
    print("✅ Datos de prueba insertados correctamente")

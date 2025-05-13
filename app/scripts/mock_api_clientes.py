from sqlalchemy.orm import Session
from app.infrastructure.db.database import SessionLocal, engine, Base
from app.infrastructure.db.models.api_cliente_model import ApiClienteModel

def crear_tabla_api_clientes():
    print("🛠️ Creando tabla api_clientes si no existe...")
    Base.metadata.create_all(bind=engine)

def poblar_api_clientes():
    db: Session = SessionLocal()

    clientes = [
        ApiClienteModel(nombre_cliente="PowerBI", api_key="clave_powerbi_123", activo=True),
        ApiClienteModel(nombre_cliente="ERP_Interno", api_key="clave_erp_456", activo=True),
        ApiClienteModel(nombre_cliente="Malicioso", api_key="clave_invalida", activo=False)
    ]

    db.add_all(clientes)
    db.commit()
    db.close()
    print("✅ Claves API mock insertadas correctamente.")

if __name__ == "__main__":
    crear_tabla_api_clientes()
    poblar_api_clientes()

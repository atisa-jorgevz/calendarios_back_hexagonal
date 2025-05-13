from app.infrastructure.db.database import Base, engine
from app.infrastructure.db.models import  ProcesoModel
from app.infrastructure.db.models  import HitoModel
from app.infrastructure.db.models import ProcesoHitoMaestroModel
from app.infrastructure.db.models import PlantillaModel
from app.infrastructure.db.models import PlantillaProcesoModel
from app.infrastructure.db.models import ClienteProcesoModel
from app.infrastructure.db.models import ClienteProcesoHitoModel

def drop_all_tables():
    print("⚠️ Borrando todas las tablas definidas en los modelos...")
    Base.metadata.drop_all(bind=engine)
    print("🧨 Tablas eliminadas.")

def create_all_tables():
    print("🛠️ Creando todas las tablas de nuevo...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas correctamente.")

if __name__ == "__main__":
    drop_all_tables()
    create_all_tables()
    print("🔥 Base de datos reiniciada correctamente (DROP + CREATE)")

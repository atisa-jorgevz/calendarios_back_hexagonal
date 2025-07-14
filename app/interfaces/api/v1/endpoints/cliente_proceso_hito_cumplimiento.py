from fastapi import APIRouter, Depends, HTTPException, Body, Path, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.infrastructure.db.database import SessionLocal
from app.infrastructure.db.repositories.cliente_proceso_hito_cumplimiento_repository_sql import ClienteProcesoHitoCumplimientoRepositorySQL
from app.infrastructure.db.repositories.cliente_proceso_hito_repository_sql import ClienteProcesoHitoRepositorySQL

from app.domain.entities.cliente_proceso_hito_cumplimiento import ClienteProcesoHitoCumplimiento

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_repo(db: Session = Depends(get_db)):
    return ClienteProcesoHitoCumplimientoRepositorySQL(db)

def get_repo_cliente_proceso_hito(db: Session = Depends(get_db)):
    return ClienteProcesoHitoRepositorySQL(db)

@router.post("/cliente-proceso-hito-cumplimientos", tags=["ClienteProcesoHitoCumplimiento"], summary="Crear cumplimiento de hito",
    description="Registra el cumplimiento de un hito específico de un proceso de cliente.")
def crear(
    data: dict = Body(..., example={
        "cliente_proceso_hito_id": 1,
        "fecha": "2023-01-01",
        "hora": "14:30:00",
        "observacion": "Hito cumplido satisfactoriamente",
        "usuario": "usuario@atisa.es"
    }),
    repo = Depends(get_repo),
    repo_cliente_proceso_hito = Depends(get_repo_cliente_proceso_hito)
):
    try:
        # Verificar que el cliente_proceso_hito_id existe
        cliente_proceso_hito = repo_cliente_proceso_hito.obtener_por_id(data["cliente_proceso_hito_id"])
        if not cliente_proceso_hito:
            raise HTTPException(status_code=404, detail="El cliente_proceso_hito_id especificado no existe")

        # Validar y formatear la hora si es necesario
        hora = data["hora"]
        if len(hora.split(":")) == 2:  # Si solo tiene HH:MM, agregar :00
            hora = hora + ":00"

        cumplimiento = ClienteProcesoHitoCumplimiento(
            cliente_proceso_hito_id=data["cliente_proceso_hito_id"],
            fecha=data["fecha"],
            hora=hora,
            observacion=data.get("observacion", ""),
            usuario=data["usuario"]
        )
        return repo.guardar(cumplimiento)
    except HTTPException:
        # Re-lanzar las excepciones HTTP ya manejadas
        raise
    except Exception as e:
        # Manejar errores inesperados
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/cliente-proceso-hito-cumplimientos", tags=["ClienteProcesoHitoCumplimiento"], summary="Listar todos los cumplimientos",
    description="Devuelve todos los registros de cumplimiento de hitos con soporte para paginación y ordenación.")
def listar(
    page: Optional[int] = Query(None, ge=1, description="Página actual"),
    limit: Optional[int] = Query(None, ge=1, le=100, description="Cantidad de resultados por página"),
    sort_field: Optional[str] = Query(None, description="Campo por el cual ordenar (id, cliente_proceso_hito_id, fecha, hora, observacion, usuario)"),
    sort_direction: Optional[str] = Query("asc", regex="^(asc|desc)$", description="Dirección de ordenación: asc o desc"),
    repo = Depends(get_repo)
):
    cumplimientos = repo.listar()
    total = len(cumplimientos)

    # Aplicar ordenación si se especifica
    if sort_field and hasattr(cumplimientos[0] if cumplimientos else None, sort_field):
        reverse = sort_direction == "desc"

        # Función de ordenación que maneja valores None
        def sort_key(cumplimiento):
            value = getattr(cumplimiento, sort_field, None)
            if value is None:
                return ""  # Los valores None van al final
            # Si es numérico (como id, cliente_proceso_hito_id), convertir a número para ordenación correcta
            if sort_field in ["id", "cliente_proceso_hito_id"]:
                try:
                    return int(value)
                except (ValueError, TypeError):
                    return 0
            # Para campos de texto/fecha/hora, convertir a string para ordenación
            return str(value).lower() if isinstance(value, str) else str(value)

        cumplimientos.sort(key=sort_key, reverse=reverse)

    # Aplicar paginación después de ordenar
    if page is not None and limit is not None:
        start = (page - 1) * limit
        end = start + limit
        cumplimientos = cumplimientos[start:end]

    if not cumplimientos:
        raise HTTPException(status_code=404, detail="No se encontraron cumplimientos")

    return {
        "total": total,
        "cumplimientos": cumplimientos
    }

@router.get("/cliente-proceso-hito-cumplimientos/{id}", tags=["ClienteProcesoHitoCumplimiento"], summary="Obtener cumplimiento por ID",
    description="Devuelve un registro de cumplimiento de hito específico según su ID.")
def obtener(
    id: int = Path(..., description="ID del cumplimiento a consultar"),
    repo = Depends(get_repo)
):
    cumplimiento = repo.obtener_por_id(id)
    if not cumplimiento:
        raise HTTPException(status_code=404, detail="Cumplimiento no encontrado")
    return cumplimiento

@router.put("/cliente-proceso-hito-cumplimientos/{id}", tags=["ClienteProcesoHitoCumplimiento"], summary="Actualizar cumplimiento",
    description="Actualiza un registro de cumplimiento de hito existente por su ID.")
def actualizar(
    id: int = Path(..., description="ID del cumplimiento a actualizar"),
    data: dict = Body(..., example={
        "fecha": "2023-01-02",
        "hora": "15:30:00",
        "observacion": "Observación actualizada",
        "usuario": "usuario@atisa.es"
    }),
    repo = Depends(get_repo)
):
    cumplimiento_actualizado = repo.actualizar(id, data)
    if not cumplimiento_actualizado:
        raise HTTPException(status_code=404, detail="Cumplimiento no encontrado")
    return cumplimiento_actualizado

@router.delete("/cliente-proceso-hito-cumplimientos/{id}", tags=["ClienteProcesoHitoCumplimiento"], summary="Eliminar cumplimiento",
    description="Elimina un registro de cumplimiento de hito existente por su ID.")
def eliminar(
    id: int = Path(..., description="ID del cumplimiento a eliminar"),
    repo = Depends(get_repo)
):
    eliminado = repo.eliminar(id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Cumplimiento no encontrado")
    return {"mensaje": "Cumplimiento eliminado exitosamente"}

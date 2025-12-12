from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.conductores import Conductor
from app.schemas.conductores_schemas import ConductorCreate

def crear_conductor(db: Session, conductor: ConductorCreate):
    conductor_data = conductor.model_dump()

    if not conductor_data.get("codigo"):
        conductor_data["codigo"] = f"C-{uuid.uuid4().hex[:6].upper()}"

    db_conductor = Conductor(**conductor_data)
    db.add(db_conductor)
    db.commit()
    db.refresh(db_conductor)
    return db_conductor

def obtener_conductores(db: Session):
    return db.query(Conductor).all()

def obtener_conductor(db: Session, conductor_id: int):
    return db.query(Conductor).filter(Conductor.id == conductor_id).first()

def buscar_conductores_por_nombre(db: Session, nombre: str):
    return db.query(Conductor).filter(Conductor.nombre.ilike(f"%{nombre}%")).all()

def buscar_conductores_por_apellido(db: Session, apellido: str):
    return db.query(Conductor).filter(Conductor.apellido.ilike(f"%{apellido}%")).all()

def obtener_conductores_con_licencias_proximas_a_vencer(db: Session, dias_antes: int):
    hoy = datetime.now().date()
    fecha_limite = hoy + timedelta(days=dias_antes)
    return db.query(Conductor).filter(Conductor.fecha_vencimiento_licencia <= fecha_limite).all()

def actualizar_conductor(db: Session, conductor_id: int, conductor: ConductorCreate):
    db_conductor = db.query(Conductor).filter(Conductor.id == conductor_id).first()
    if not db_conductor:
        return None
    
    db_conductor.codigo = conductor.codigo
    db_conductor.nombre = conductor.nombre
    db_conductor.apellido = conductor.apellido
    db_conductor.dni = conductor.dni
    db_conductor.foto = conductor.foto
    db_conductor.numero_contacto = conductor.numero_contacto
    db_conductor.email_contacto = conductor.email_contacto
    db_conductor.direccion = conductor.direccion
    db_conductor.estado = conductor.estado
    db_conductor.fecha_nacimiento = conductor.fecha_nacimiento
    db_conductor.actualizado_en = datetime.now()
    
    db.commit()
    db.refresh(db_conductor)
    return db_conductor

def eliminar_conductor(db: Session, conductor_id: int):
    db_conductor = db.query(Conductor).filter(Conductor.id == conductor_id).first()
    db.delete(db_conductor)
    db.commit()
    return db_conductor

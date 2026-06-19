from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import Despacho, Incidencia, get_db

app = FastAPI(title="Operations Service - Logística", version="1.0")

class OrderCreatedEvent(BaseModel):
    order_id: int
    client_name: str

# Caso de Uso 2: Procesar Evento Asíncrono (Worker)
@app.post("/api/v1/events/order_created")
async def handle_order_created_event(event: OrderCreatedEvent, db: Session = Depends(get_db)):
    print(f"[Worker] Procesando evento logístico para pedido: {event.order_id}")
    
    nuevo_despacho = Despacho(
        pedido_id=event.order_id, 
        conductor_asignado="Pendiente de asignación...", 
        estado_logistico="ESPERANDO_CONDUCTOR"
    )
    db.add(nuevo_despacho)
    db.commit()
    
    return {"status": "event_processed"}

# Caso de Uso 3: Asignar Repartidor
@app.post("/api/v1/dispatch/")
async def assign_driver(order_id: int, driver_name: str, db: Session = Depends(get_db)):
    despacho = db.query(Despacho).filter(Despacho.pedido_id == order_id).first()
    if despacho:
        despacho.conductor_asignado = driver_name
        despacho.estado_logistico = "EN_RUTA"
        db.commit()
        return {"status": "success", "message": f"Conductor {driver_name} asignado al pedido {order_id}"}
    return {"status": "error", "message": "Pedido no encontrado en operaciones"}

# Caso de Uso 4: Gestor de Incidencias
@app.post("/api/v1/support/incidents/")
async def report_incident(order_id: int, description: str, db: Session = Depends(get_db)):
    despacho = db.query(Despacho).filter(Despacho.pedido_id == order_id).first()
    
    if not despacho:
        return {"status": "error", "message": "No se puede reportar incidencia: Pedido no encontrado."}
    
    nueva_incidencia = Incidencia(pedido_id=order_id, descripcion=description)
    db.add(nueva_incidencia)
    
    despacho.estado_logistico = "INCIDENCIA_REPORTADA"
    db.commit()
    db.refresh(nueva_incidencia)
    
    return {
        "status": "success",
        "message": f"Incidencia reportada para el pedido {order_id}",
        "incident_id": nueva_incidencia.id
    }
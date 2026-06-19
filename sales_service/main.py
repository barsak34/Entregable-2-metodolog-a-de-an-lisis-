import httpx
from fastapi import FastAPI, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from database import Pedido, get_db

app = FastAPI(title="Sales Service - Ventas", version="1.0")

# Integración Asíncrona: Mock de publicación en Tópico/Cola
async def publish_order_created_event(order_id: int, client_name: str):
    async with httpx.AsyncClient() as client:
        payload = {"order_id": order_id, "client_name": client_name}
        try:
            # Emite el evento al servicio de operaciones (simulación Fan-out)
            await client.post("http://127.0.0.1:8001/api/v1/events/order_created", json=payload)
            print(f"[Event Bus] Evento PedidoCreado entregado para Order {order_id}")
        except Exception as e:
            print(f"[DLQ Simulada] Error entregando evento: {e}")

# Caso de Uso 1: Crear Pedido
@app.post("/api/v1/orders/")
async def create_order(client_name: str, item: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # 1. Guardar en base de datos local (Consistencia Fuerte en Ventas)
    nuevo_pedido = Pedido(cliente=client_name, item=item)
    db.add(nuevo_pedido)
    db.commit()
    db.refresh(nuevo_pedido)
    
    # 2. Publicar evento asíncrono para no bloquear al cliente
    background_tasks.add_task(publish_order_created_event, nuevo_pedido.id, client_name)
    
    # 3. Respuesta inmediata (Privilegia Disponibilidad)
    return {
        "status": "success", 
        "message": "Pedido guardado y evento encolado",
        "order_id": nuevo_pedido.id
    }
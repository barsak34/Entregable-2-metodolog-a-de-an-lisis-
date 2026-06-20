# Entregable 3: Arquitectura Tecnológica e Integración - Sistema de Logística 


El proyecto está dividido en dos servicios independientes que se comunican entre sí por debajo:
1. **Sales Service (Ventas):** Encargado de tomar los pedidos rapidísimo.
2. **Operations Service (Operaciones):** Encargado de la logística pesada, asignar repartidores y manejar problemas.

---

## Cómo ejecutar el proyecto 

Como el sistema ya no es un monolito, necesita levantar dos "servidores" distintos. Abre dos pestañas en tu terminal y sigue estos pasos:

### 1. Levantar el Servicio de Ventas (Terminal 1)
Entrar a la carpeta, instalar las librerías necesarias y levanta el servidor en el puerto 8000:
```bash
cd sales_service
python -m pip install fastapi uvicorn sqlalchemy httpx
python -m uvicorn main:app --port 8000 --reload

### 2. Levantar el servicio de operaciones (Terminal 2)
Entrar a la carpeta, instalar las librerías necesarias y levanta el servidor en el puerto 8001:
```bash
cd operations_service
python -m pip install fastapi uvicorn sqlalchemy httpx
python -m uvicorn main:app --port 8001 --reload
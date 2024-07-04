from fastapi import FastAPI
from app.routes import router
from infrastructure.db.database import engine, Base

# Creacion las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Restaurante API",
    version="1.0.0",
    description="El objetivo de este proyecto es desarrollar el backend de un sistema de gestión para un restaurante. El sistema permitirá a los administradores del restaurante gestionar inventarios de ingredientes, elaborar menús, procesar pedidos de los clientes, y generar reportes diversos.",
)

#Las rutas de los endpoints
app.include_router(router, prefix="/api/v1", tags=["router"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
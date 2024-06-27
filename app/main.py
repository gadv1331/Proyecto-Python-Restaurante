from fastapi import FastAPI
from app.routes import router
from infrastructure.db.database import engine, Base

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Incluir los routers
app.include_router(router, prefix="/api/v1", tags=["router"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
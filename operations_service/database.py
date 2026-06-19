from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Persistencia: SQLite local para Operaciones
SQLALCHEMY_DATABASE_URL = "sqlite:///./operaciones.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# Modelo de Dominio: Visión logística del pedido (Representación distribuida)
class Despacho(Base):
    __tablename__ = "despachos"
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, index=True) 
    conductor_asignado = Column(String, nullable=True)
    estado_logistico = Column(String, default="PENDIENTE_ASIGNACION")

# Modelo de Dominio: Gestión de incidencias
class Incidencia(Base):
    __tablename__ = "incidencias"
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, index=True)
    descripcion = Column(String)
    estado_incidencia = Column(String, default="ABIERTA")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
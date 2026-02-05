from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from db.database import Base, engine, SessionLocal

# Memory table
class Memory(Base):
    __tablename__ = "memory"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    value = Column(String)


# Create table
Base.metadata.create_all(bind=engine)


def tool_save_memory(key: str, value: str) -> dict:
    db: Session = SessionLocal()

    existing = db.query(Memory).filter(Memory.key == key).first()

    if existing:
        existing.value = value
    else:
        new_memory = Memory(key=key, value=value)
        db.add(new_memory)

    db.commit()
    db.close()

    return {"key": key, "value": value}


def tool_get_memory(key: str) -> dict:
    db: Session = SessionLocal()

    memory = db.query(Memory).filter(Memory.key == key).first()

    db.close()

    if memory:
        return {"key": memory.key, "value": memory.value}
    else:
        return {"error": "Memory not found"}

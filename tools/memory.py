from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from db.database import Base, engine, SessionLocal


class Memory(Base):
    __tablename__ = "memory"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    value = Column(String)


# Create table automatically
Base.metadata.create_all(bind=engine)


def tool_save_memory(key: str, value: str) -> dict:
    db: Session = SessionLocal()

    record = db.query(Memory).filter(Memory.key == key).first()

    if record:
        record.value = value
    else:
        record = Memory(key=key, value=value)
        db.add(record)

    db.commit()
    db.close()

    return {"key": key, "value": value}


def tool_get_memory(key: str) -> dict:
    db: Session = SessionLocal()

    record = db.query(Memory).filter(Memory.key == key).first()

    db.close()

    if record:
        return {"key": record.key, "value": record.value}

    return {"error": "Memory not found"}

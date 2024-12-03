from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base
import enum
from datetime import datetime

Base = declarative_base()

class UserType(str, enum.Enum):
    STUDENT = "student"
    PARENT = "parent"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserType), default=UserType.STUDENT)
    age = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow) 
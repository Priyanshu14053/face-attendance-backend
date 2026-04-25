from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    department = Column(String)
    year = Column(String)
    address = Column(String)
    username = Column(String)   # 👈 new
    password = Column(String)                # 👈 new
    face_encoding = Column(String)  # store as string
    role = Column(String, default="student")  # student / admin


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    date = Column(String)

    check_in = Column(String)
    check_out = Column(String)

    latitude = Column(String)
    longitude = Column(String)
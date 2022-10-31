from app.configs.base import Base

from sqlalchemy import Column, Integer, String


class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    cpf = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False, unique=True)
    type = Column(String(50))

    __mapper_args__ = {
        "polymorphic_identity": "person",
        "polymorphic_on": type,
    }

    def __init__(self):
        pass

    def __init__(self, name, password, email, cpf, phone):
        self.name = name
        self.password = password
        self.email = email
        self.cpf = cpf
        self.phone = phone

    

from app.configs.base import Base

from sqlalchemy import Column, ForeignKey, Integer, String


class Contacts(Base):
    __tablename__ = "contacts"
    id_contacts = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    cpf = Column(String)
    phone = Column(String)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    
    def __init__(self, name, email, cpf, phone, account_id):
        self.name = name
        self.email = email
        self.cpf = cpf
        self.phone = phone
        self.account_id = account_id

    def __repr__(self) -> str:
        return f"{self.name, self.email, self.cpf, self.phone}"

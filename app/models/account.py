from app.models.person import Person
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Float, ForeignKey, Integer, String


class Account(Person):
    __tablename__ = "accounts"
    id = Column(Integer, ForeignKey("person.id"), primary_key=True)
    bank = Column(String, nullable=False)
    agency = Column(String, nullable=False, unique=True)
    ca = Column(String, nullable=False, unique=True)
    balance = Column(Float)
    contacts = relationship("Contacts")
    bank_statement = relationship("BankStatement")

    __mapper_args__ = {
        "polymorphic_identity": "accounts",
    }
    
    def __init__(self, name, password, email, cpf, phone, agency="", ca="", bank="Knauer"):
        super().__init__(name, password, email, cpf, phone)
        self.bank = bank
        self.agency = agency
        self.ca = ca
        self.balance = 0

    '''
    def __repr__(self):
        return f"{self.id ,self.name, self.password, self.email, self.cpf, self.phone, self.agency, self.ca, self.bank}"
    '''

from app.configs.base import Base

from sqlalchemy import Column, Date, Float, ForeignKey, Integer


class BankStatement(Base):
    __tablename__ = "bank_statement"
    id = Column(Integer, primary_key=True)
    balance = Column(Float, nullable=False)
    money = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    
    def __init__(self, balance, money, total, date, account_id):
        self.balance = balance
        self.money = money
        self.total = total
        self.date = date
        self.account_id = account_id

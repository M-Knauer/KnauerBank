from datetime import datetime

from app.configs.connection import DbConnectionHandler
from app.models.bank_statement import BankStatement as Bank

class BankStatementRepository():
    
    def insert(self, balance, money, total, account_id, date=datetime.now()):
        try:
            with DbConnectionHandler() as db:
                bank_statement = Bank(balance=balance, money=money, total=total, date=date.now(), account_id=account_id)
                db.session.add(bank_statement)
                db.session.commit()
        except Exception:
            db.session.rollback()
            return Exception.with_traceback

    def select_all_by_id(self, id):
        try:
            with DbConnectionHandler() as db:
                return db.session.query(Bank).filter(Bank.account_id == id).order_by(Bank.date.desc()).all()
        except Exception:
            return Exception.with_traceback
    
    def select_all_by_id_offset(self, id, offset):
        try:
            with DbConnectionHandler() as db:
                # pagina com offset and limit
                return db.session.query(Bank).with_entities(Bank.balance, Bank.money, Bank.total, Bank.date).filter(Bank.account_id == id).order_by(Bank.date.desc()).offset(offset=offset).limit(10)
        except Exception:
            return Exception.with_traceback

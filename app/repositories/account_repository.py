from app.configs.connection import DbConnectionHandler
from app.models.account import Account
from app.models.person import Person


class AccountRepository():
    def insert(self, name, password, email, cpf, phone, agency, ca, bank="Knauer"):
        with DbConnectionHandler() as db:
            try:
                insert_data = Account(name=name, password=password, email=email, cpf=cpf, phone=phone, agency=agency, ca=ca, bank=bank)
                db.session.add(insert_data)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e
    
    def select_by_cpf(self, cpf):
        with DbConnectionHandler() as db:
            try:
                return db.session.query(Account)\
                    .filter(Account.cpf == cpf)\
                    .one_or_none()
            except Exception as e:
                raise e
    
    def select_by_id(self, id):
        with DbConnectionHandler() as db:
            try:
                return db.session.query(Account)\
                    .filter(Account.id == id)\
                    .one_or_none()
            except Exception as e:
                raise e

    def update_money(self, id, amount):
        with DbConnectionHandler() as db:
            try:
                db.session.query(Account).filter(Account.id == id).update({"balance": amount})
                db.session.commit()
            except Exception:
                db.session.rollback()
                return Exception
    
    def update(self, id, email, phone):
        with DbConnectionHandler() as db:
            try:
                db.session.query(Account).filter(Account.id == id)\
                    .update({"email": email, "phone": phone})
                db.session.commit()
            except Exception:
                db.session.rollback()
                return Exception

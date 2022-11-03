from app.configs.connection import DbConnectionHandler
from app.models.person import Person


class PersonRepository():
    def insert(self, name, password, email, cpf, phone):
        with DbConnectionHandler() as db:
            try:
                insert_data = Person(name=name, password=password, email=email, cpf=cpf, phone=phone)
                db.session.add(insert_data)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e

    def update(self, id, email, phone):
        with DbConnectionHandler() as db:
            try:
                db.session.query(Person).filter(Person.id == id)\
                    .update({"email": email, "phone": phone})
                db.session.commit()
            except Exception:
                db.session.rollback()
                return Exception

    def select_by_cpf(self, cpf):
        with DbConnectionHandler() as db:
            try:
                return db.session.query(Person).filter(Person.cpf == cpf).one_or_none()
            except Exception:
                return Exception
    
    def select_by_email(self, email):
        with DbConnectionHandler() as db:
            try:
                return db.session.query(Person).filter(Person.email == email).one_or_none()
            except Exception:
                return Exception
    
    def select_by_phone(self, phone):
        with DbConnectionHandler() as db:
            try:
                return db.session.query(Person).filter(Person.phone == phone).one_or_none()
            except Exception:
                return Exception

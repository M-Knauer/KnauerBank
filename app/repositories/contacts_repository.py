from app.configs.connection import DbConnectionHandler
from app.models.contacts import Contacts


class ContactsRepository():
    def add_contact(self, name, email, cpf, phone, account_id):
        with DbConnectionHandler() as db:
            try:
                contact = Contacts(name=name, email=email, cpf=cpf, phone=phone, account_id=account_id)
                db.session.add(contact)
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise Exception
    
    def select_all_by_id(self, id):
        with DbConnectionHandler() as db:
            try:
                return db.session.query(Contacts).filter(Contacts.account_id == id).all()
            except Exception:
                raise Exception
    
    def select_by_id(self, id):
        with DbConnectionHandler() as db:
            try:
                return db.session.query(Contacts).filter(Contacts.id_contacts == id).one()
            except Exception:
                raise Exception
    
    def select_all_by_id_offset(self, id, offset, per_page):
        try:
            with DbConnectionHandler() as db:
                # pagina com offset and limit
                return db.session.query(Contacts).filter(Contacts.account_id == id).order_by(Contacts.name).offset(offset=offset).limit(per_page)
        except Exception:
            return Exception.with_traceback
    
    def update(self, id, name, email, phone):
        with DbConnectionHandler() as db:
            try:
                db.session.query(Contacts).filter(Contacts.id_contacts == id)\
                    .update({"name": name, "email": email, "phone": phone})
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise Exception

    def delete(self, id):
        with DbConnectionHandler() as db:
            try:
                db.session.query(Contacts).filter(Contacts.id_contacts == id)\
                    .delete()
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise Exception

from functools import wraps
from random import randint

from app.repositories.bank_statatement_repository import \
    BankStatementRepository as br
from flask import redirect, session

db_br = br()

def set_ca():
    ca = ''
    for n in range(6):
        ca += str(randint(1, 9))
    ca += '-'
    ca += str(randint(1, 9))
    return ca

def set_agency():
    ag = ""
    for n in range(4):
        ag += str(randint(1, 9))
    return ag

def outgoing_money(balance, val, account_id):
    db_br.insert(balance=balance + val, money= -1 * val, total=balance, account_id=account_id)

def down_payment(balance, val, account_id):
    db_br.insert(balance=balance - val, money= val, total=balance, account_id=account_id)
    print(account_id)

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
from tempfile import mkdtemp
from app import app
from app.helper import (down_payment, login_required, outgoing_money,
                        set_agency, set_ca)
from app.repositories.account_repository import AccountRepository as ar
from app.repositories.bank_statatement_repository import \
    BankStatementRepository as br
from app.repositories.contacts_repository import ContactsRepository as cr
from flask import flash, redirect, render_template, request, session
from flask_session.__init__ import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_paginate import Pagination, get_page_args
from app.models.error_handler import InputError
from app.repositories.person_repositroy import PersonRepository as pr

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set repository
db_ar = ar()
db_cr = cr()
db_br = br()
db_pr = pr()

ROWS_PER_PAGE = 5

@app.route("/")
@login_required
def index():
    # Seleciona a atual conta logada
    acc = db_ar.select_by_id(session["user_id"])

    # Seleciona todos os contatos da conta logada
    contacts = db_cr.select_all_by_id(session["user_id"])


    # https://codingshiksha.com/flask/python-3-flask-bootstrap-4-pagination-example-to-paginate-array-of-users-in-browser-using-flask-paginate-in-html5/
    # Paginação
    # Padrão da função de paginação
    # https://gist.github.com/mozillazg/69fb40067ae6d80386e10e105e6803c9
    page, per_page, offset = get_page_args(quantity_per_page=5)
    
    pagination_contacts = db_cr.select_all_by_id_offset(session["user_id"], offset=offset, per_page=per_page)
    
    # pega o total de numeros da query
    total = 0
    for r in contacts:
        total += 1
    
    # configura a paginação
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')

    return render_template('index.html',
                           acc=acc,
                           contacts=pagination_contacts,
                           page=page,
                           per_page=5,
                           pagination=pagination
                           )
    
@app.route("/bank_statement")
@login_required
def bank_statement():
    # Seleciona todo o historico da atual conta logada
    bs = db_br.select_all_by_id(session["user_id"])

    # https://codingshiksha.com/flask/python-3-flask-bootstrap-4-pagination-example-to-paginate-array-of-users-in-browser-using-flask-paginate-in-html5/
    # Paginação
    # Padrão da função de paginação
    page, per_page, offset = get_page_args()
    
    pagination_bs = db_br.select_all_by_id_offset(session["user_id"], offset=offset)
    
    # pega o total de numeros da query
    total = 0
    for r in bs:
        total += 1
    
    # configura a paginação
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')

    return render_template('bank_statement.html',
                           bank_statement=pagination_bs,
                           page=page,
                           per_page=10,
                           pagination=pagination,
                           )


@app.route("/add_money", methods=["GET", "POST"])
@login_required
def add_money():
    try:
        if request.method == "POST":
            amount = float(request.form.get("amount"))
            
            if amount < 0:
                flash("Values must be a positive number")
                return redirect("/add_money")
            
            acc = db_ar.select_by_id(session["user_id"])
            acc.balance += amount
            db_ar.update_money(session["user_id"], acc.balance)
            flash("Money has been added!")

            # add to history
            down_payment(balance=acc.balance, val=amount, account_id=session["user_id"])

            return redirect("/")

        return render_template("money.html")
    except ValueError:
        flash("Values must be a number")
        return redirect("/add_money")

# consertar o erro

@app.route("/add_contact", methods=["GET", "POST"])
@login_required
def add_contact():
    try:
        if request.method == "POST":
            name = request.form.get("name")
            email = request.form.get("email")
            cpf = request.form.get("cpf")
            phone = request.form.get("phone")

            db_cr.add_contact(name=name, email=email, cpf=cpf, phone=phone, account_id=session["user_id"])
            flash("New contact has been added!")
            
            return redirect("/")
        
        return render_template("add_contact.html")
    except Exception:
        raise Exception.with_traceback

@app.route("/delete/<int:id_contacts>", methods=["POST"])
def delete(id_contacts):
    try:
        check = request.form.get("check")
        if check:
            db_cr.delete(id_contacts)
            flash("Contact has been deleted!")
        return redirect("/")
    except Exception:
        raise Exception


@app.route("/edit_contact/<int:id_contacts>", methods=["GET", "POST"])
@login_required
def edit_contact(id_contacts):
    try:
        if request.method == "POST":
            name = request.form.get("name").title()
            email = request.form.get("email")
            phone = request.form.get("phone")

            if phone == "":
                flash("Phone number cannot be empty")
                raise InputError
            elif not phone.isnumeric():
                flash("Phone number must be a number")
                raise InputError

            db_cr.update(id=id_contacts, name=name, email=email, phone=phone)
            flash("Contact has been updated!")

            return redirect("/")

        contact = db_cr.select_by_id(id_contacts)
        return render_template("add_contact.html", contact=contact)
    except InputError:
        return redirect(f"/edit_contact/{id_contacts}")
    except Exception:
        return Exception.with_traceback

@app.route("/pix", methods=["GET", "POST"])
@login_required
def pix():
    try:
        if request.method == "POST":
            cpf = request.form.get("cpf")
            contact_cpf = request.form.get("contact_cpf")
            value = float(request.form.get("value"))

            # get the destination account
            dest = db_ar.select_by_cpf(cpf=cpf if contact_cpf == "" else contact_cpf)
            # get the main account
            acc = db_ar.select_by_id(session["user_id"])

            if value < 0:
                flash("Value cannot be a negative number")
                raise InputError
            elif (acc.balance - value) < 0:
                flash("Not enough money")
                raise InputError
            elif contact_cpf == "":
                if len(cpf) > 0 and not cpf.isnumeric():
                    flash("CPF must be a numeric value")
                    raise InputError
                elif cpf.strip() == "":
                    flash("CPF cannot be empty")
                    raise InputError

            # add money to destination account
            if dest:
                dest.balance += value
                db_ar.update_money(dest.id, dest.balance)

                # add money to destination account register in history
                down_payment(dest.balance, value, dest.id)

            # subtract main account money 
            acc.balance -= value
            db_ar.update_money(acc.id, acc.balance)
            flash("Money has been sended!\n")

            # subtract main account money register in history
            outgoing_money(acc.balance, value, session["user_id"])

            # update the main account balance if has enough money for that 
            # and if contact is not already in contact list
            if contact_cpf == "" and cpf:
                userInput = request.form.get("userInput")
                if userInput:
                    new_contact = db_ar.select_by_cpf(cpf=cpf)
                    if new_contact:
                        db_cr.add_contact(
                            name=new_contact.name, email=new_contact.email, cpf=new_contact.cpf,\
                            phone=new_contact.phone, account_id=session["user_id"]
                        )
                        flash("Contact has been added")
                    else:
                        return render_template("add_contact.html", cpf_recived=cpf)
            
            return redirect("/")

        contacts = db_cr.select_all_by_id(session["user_id"])
        return render_template("pix.html", contacts=contacts)
    except InputError:
        return redirect("/pix")
    except ValueError:
        flash("Value must be a number")
        return redirect("/pix")
    except Exception:
        raise Exception.with_traceback

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    try:
        if request.method == "POST":
            email = request.form.get("email").strip()
            phone = request.form.get("phone").strip()
            
            if email == "":
                flash("Email cannot be empty")
                raise InputError
            elif phone == "":
                flash("Phone number cannot be empty")
                raise InputError
            elif not phone.isnumeric():
                flash("Phone number must be numeric")
                raise InputError
            
            db_pr.update(id=session["user_id"], email=email, phone=phone)

            flash("Account update!")
            return redirect("/profile")


        acc = db_ar.select_by_id(session["user_id"])
        return render_template("profile.html", acc=acc)

    except InputError:
        return redirect("/profile")
    except Exception:
        raise Exception.with_traceback


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        
        name = request.form.get("name").title()
        pw = request.form.get("password")
        pw_confirm = request.form.get("passwordConfirm")
        email = request.form.get("email")
        cpf = request.form.get("cpf")
        phone = request.form.get("phone")

        if not name:
            return "Error name!" 
        elif not pw:
            return "Error pw!" 
        elif not email:
            return "Error email!"
        elif not cpf:
            return "Error cpf!"
        elif not phone:
            return "Error phone!"
        if pw_confirm != pw:
            return "paasword not equal"

        agency = set_agency()
        ca = set_ca()
        pwHash = generate_password_hash(pw)
        
        db_ar.insert(name=name, password=pwHash, email=email, cpf=cpf, phone=phone, agency=agency, ca=ca)
        flash("You was successfully registered!")
        return redirect("/")
        
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("cpf"):
            return ("must provide cpf", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return ("must provide password", 403)

        # Query database for cpf
        cpf = request.form.get("cpf")
        rows = db_ar.select_by_cpf(cpf)
    
        # Ensure username exists and password is correct
        if not rows or not check_password_hash(rows.password, request.form.get("password")):
           return ("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows.id

        # Redirect user to home page
        flash("You are logged!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    # clear session
    session.clear()

    # redirect to home page
    return redirect("/")

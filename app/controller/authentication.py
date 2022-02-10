from flask import render_template, redirect, url_for, flash, session, request
from app import app, mysql
from app.models.user import User


@app.route("/users/new", methods=["GET", "POST"])
def sign_up():

    if request.method == "POST":
        req = request.form
        username = req.get("username")
        email = req.get("email")
        password = req.get("password")
        user = User()

        # verifica a disponibilidade de nome e email no banco de dados
        user_in_db = user.is_registered(username, email, mysql)
        if not user_in_db:
            if len(password) <= 8:
                flash("A senha precisa ter ao menos 8 caracteres.")
                return redirect(request.url)
            else:
                user_id = user.create_account(
                    username,
                    email,
                    password,
                    mysql
                )
                # cria uma nova sessão com o id do usuário
                session["USER_ID"] = user_id
                return redirect(url_for("index"))
        else:
            flash("Usuário já cadastrado.")
            return redirect(request.url)
    
    return render_template("public/new_user.html")


@app.route("/users/account", methods=["GET", "POST"])
def sign_in():

    if request.method == "POST":
        req = request.form
        username = req.get("username")
        password = req.get("password")
        # valida o nome de usuário e a senha
        user = User()
        user_id = user.login(username, password, mysql)

        if not user_id:
            flash("Nome de usuário ou senha incorretos.")
            return redirect(request.url)
        else:
            # cria uma sessão de usuário
            session["USER_ID"] = user_id
            return redirect(url_for("index"))

    return render_template("public/user_access.html")


@app.route("/users/session", methods=["POST"])
def sign_out():

    if request.method == "POST":
        # remove id do usuário encerrando a sessão
        session.pop("USER_ID", None)
        return redirect(url_for("index"), code=302)

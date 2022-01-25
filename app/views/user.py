from app import app, mysql


@app.route("/user/account")
def account():

    return "account"


@app.route("/user/new")
def new_user():

    return "new_user"


@app.route("user/session")
def user_session():

    return "user_session"
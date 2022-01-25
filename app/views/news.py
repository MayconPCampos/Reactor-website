from app import app, mysql


@app.route("/news")
def news():

    return "news"
from app import app, mysql
from app.models.news import News
from flask import render_template, request, redirect, url_for
import os


@app.route("/admin/contents")
def admin_contents():
    return render_template("admin/admin.html")


@app.route("/admin/contents/news", methods=["POST"])
def admin_news():
     
    if request.method == "POST":

        req = request.form
        label = req.get("label")
        title = req.get("title")
        sub = req.get("sub")
        text = req.get("text")

        if request.files:
            image = request.files.get("image")
            image.save(os.path.join(app.config["NEWS_IMAGES"], image.filename))
            image_filename = image.filename

    news = News()
    news.post_news(label, title, sub, text, image_filename, mysql)

    return redirect(url_for('admin_contents'))


@app.route("/admin/contents/titles", methods=["POST"])
def admin_title():
    pass

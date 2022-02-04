from app.tools import login_required
from flask import render_template, request
from app.models.game import *
from app.models.news import *
from app import app, mysql


@app.template_filter('format_date')
def format_date(date):
    """Recebe e formata a data e hora formatadas"""
    formated = date.strftime("%d %b %Y às %H:%M")
    return formated


@app.route("/")
def index():

    game_list = fetch_recent(mysql)
    news_list = fetch_news_limited(8, mysql)
    return render_template(
        "public/index.html",
        game_list=game_list,
        news_list=news_list
    )


@app.route("/search/")
def search():

    req = request.args
    search = req.get("s")
    results = 0
    game_list = search_games(search, mysql)
    news_list = search_news(search, mysql)

    # armazena o numero de items encontrados na busca
    results = 0
    if game_list:
        results += len(game_list)
    if news_list:
        results += len(news_list)

    return render_template(
        "public/search.html", 
        game_list=game_list,
        news_list=news_list,
        results=results
    )


@app.route("/titles/<id>")
def game(id):

    game = fetch_game_page(id, mysql)
    return render_template(
        "public/titles.html",
         game=game
    )


@app.route("/news")
def news_list():

    news_list = fetch_all(mysql)
    return render_template(
        "public/news_list.html",
        news_list=news_list
    )


@app.route("/news/<title>")
def news(title):    
    
    page_news = fetch_news_page(title, mysql)
    news_list = fetch_news_limited(7, mysql)
    return render_template(
        "public/news.html",
        page_news=page_news,
        news_list=news_list
    )


@app.route("/profile")
@login_required
def profile():
    return render_template("public/profile.html")

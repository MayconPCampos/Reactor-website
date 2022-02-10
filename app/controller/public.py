from app.tools import login_required
from flask import render_template, request, session, redirect
from app.models.game import *
from app.models.news import *
from app.models.user import User
from app import app, mysql


@app.template_filter('format_date')
def format_date(date):
    """Recebe e retorna a data e hora formatadas"""
    formated = date.strftime("%d %b %Y às %H:%M")
    return formated


@app.route("/")
def index():

    game = Game()
    game_list = game.get_recent_game_list(mysql)
    
    news = News()
    news_list = news.get_news_limited(8, mysql)
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

    game = Game()
    game_list = game.search_games(search, mysql)

    news = News()
    news_list = news.search_news(search, mysql)

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


@app.route("/title/<int:id>")
def title(id):

    game = Game()
    game.get_game_page(id, mysql)
    platform_list = game.platform.split(",")
    
    return render_template(
        "public/title.html",
         game=game,
         platform_list=platform_list
    )


@app.route('/reviews/<int:title_id>', methods=["GET","POST"])
def reviews(title_id):

    if request.method == "POST":
        req = request.form
        score = req.get("score")
        text = req.get("review")
        user_id = session["USER_ID"]
        
        # Buscando o username para ser
        # associado a review
        user = User()
        username = user.get_username_by_id(user_id, mysql)

        # enviando os dados da review para ser gravada
        # no banco de dados
        review = Review()
        review.post_review(title_id, username, score, text, mysql)
        return redirect(request.referrer)
    
    game = Game()
    game.get_game_page(title_id, mysql)
    return render_template(
        "public/review.html",
        game=game
    )


@app.route("/news")
def news_list():

    news = News()
    news_list = news.get_news(mysql)
    return render_template(
        "public/news_list.html",
        news_list=news_list
    )


@app.route("/news/<title>")
def news(title):    
    
    news = News()
    page_news = news.get_news_page(title, mysql)
    news_list = news.get_news_limited(8, mysql)
    return render_template(
        "public/news.html",
        page_news=page_news,
        news_list=news_list
    )


@app.route("/profile")
@login_required
def profile():
    return render_template("public/profile.html")

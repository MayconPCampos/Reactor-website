from app.tools import login_required
from flask import render_template, request, session, redirect, flash
from app.models.game import *
from app.models.news import *
from app.models.user import User
from app import app, mysql
from flask_paginate import Pagination, get_page_args


@app.template_filter('format_date')
def format_date(date):
    """Recebe e retorna a data e hora formatadas"""
    
    formated = date.strftime("%d %b %Y às %H:%M")
    return formated


@app.template_filter('format_review_text')
def format_review_text(text):
    """Recebe o texto da review e retorna uma
    abreviação caso ela exceda 50 caracteres
    """
    
    if len(text) > 50:
        formated = text[:50] + "..."
        return formated
    return text


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

    # obtem as informações de indice da página
    page, per_page, offset = get_page_args(
        page_parameter='page',
        per_page_parameter='per_page'
    )

    # cria uma lista com os resultados a serem
    # mostrados na página de acordo com o indice
    news_results = news_list[offset: offset + per_page]
    game_results = game_list[offset: offset + per_page]

    pagination = Pagination(
        page=page,
        per_page=per_page,
        total=results,
        css_framework='bootstrap4'
    )

    return render_template(
        "public/search.html", 
        game_results=game_results,
        news_results=news_results,
        pagination=pagination,
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
        score = float(req.get("score"))
        text = req.get("review")
        user_id = session["USER_ID"]
        
        # Buscando o username para ser
        # associado a review
        user = User()
        username = user.get_username_by_id(user_id, mysql)

        review = Review()
        username_review = review.check_review_username(username, title_id, mysql)
        
        if not username_review:

            # cria uma tupla para inicializar um objeto
            # Review, os valores None são preenchidos 
            # dentro da classe
            review_data = (
                None,
                title_id,
                score,
                text,
                None,
                username
            )

            review = Review(review_data)
            review.post_review(mysql)  # grava no banco de dados
            return redirect(request.referrer)
        
        else:
            flash("Você não pode enviar mais de uma review por título.")
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
    results = len(news_list)

    page, per_page, offset = get_page_args(
        page_parameter="page",
        per_page_parameter="per_page"
    )

    pagination = Pagination(
        page=page,
        per_page=per_page,
        total=results,
        css_framework='bootstrap4'
    )

    news_results = news_list[offset: offset + per_page]

    return render_template(
        "public/news_list.html",
        news_results=news_results,
        pagination=pagination
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


@app.route("/lenght/<int:title_id>", methods=["POST"])
def lenght(title_id):

    if request.method == "POST":

        req = request.form
        campaign = float(req.get("campaign"))
        dlc= float(req.get("dlc"))
        multiplayer = float(req.get("multiplayer"))
        complete = float(req.get("complete"))
        platform = req.get("platform")

        user = User()
        username = user.get_username_by_id(session["USER_ID"], mysql)

        # cria uma tupla para inicializar um objeto
        # Review, os valores None são preenchidos 
        # dentro da classe
        lenght_data = (
            None,
            title_id,
            username,
            platform,
            campaign,
            dlc,
            multiplayer,
            complete
        )

        lenght = Lenght(lenght_data)
        lenght.post_lenght(mysql) # grava no banco de dados
        return redirect(request.referrer)


@app.route("/profile")
@login_required
def profile():
    return render_template("public/profile.html")

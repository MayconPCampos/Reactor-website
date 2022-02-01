from app.tools import initialize_multiple


class News:

    def __init__(self: object, news_data=False) -> None:

        if news_data:
            self.id = news_data[0]
            self.label = news_data[1]
            self.title = news_data[2]
            self.sub = news_data[3]
            self.text = news_data[4]
            self.image = news_data[5]
            self.date = news_data[6]
            self.adm_id = news_data[7]


def fetch_news_limited(limit:int, mysql:object) -> list:
    """Busca um número delimitado de
    registros no banco de dados na
    tabela news, instancia e inicializa
    um objeto News para cada registro
    retornado na busca"""
    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT * FROM news LIMIT {limit}")
    news_data = cursor.fetchall()
    news_list = initialize_multiple(News, news_data)

    return news_list


def fetch_all(mysql:object) -> list:
    """Realiza busca no banco de dados,
    instancia e inicializa um objeto News
    para cada registro na tabela news"""
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM news")
    news_data = cursor.fetchall()
    news_list = initialize_multiple(News, news_data)

    return news_list


def fetch_news_page(title:str, mysql:object) -> list:
    """Realiza a busca usando o título
    da notícia no banco de dados e retorna
    os dados inicializando uma instancia do
    objeto News"""
    cursor = mysql.connection.cursor()
    cursor.execute(
        f'''SELECT * 
        FROM news 
        WHERE BINARY "{title}" = BINARY newsTitle;'''
    )
    news_data = cursor.fetchone()
    page_news = News(news_data)
    
    return page_news


def search_news(search:str, mysql:object) -> list:
    """REaliza busca no banco de dados
    através da palavra buscada, cria e
    inicializa uma instância do o objeto
    News para cada registro encontrado"""
    cursor = mysql.connection.cursor()
    cursor.execute(
        f'''SELECT * 
        FROM news 
        WHERE newsLabel 
        OR newsTitle LIKE "%{search}%";'''
    )
    news_data = cursor.fetchall()
    if news_data:
        news_list = initialize_multiple(News, news_data)
        return news_list
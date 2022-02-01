from app.tools import initialize_multiple


class Game:

    def __init__(self:object, game_data=False) -> None:

        if game_data:
            self.lenghts = []
            self.reviews = []
            self.id = game_data[0]
            self.image = game_data[7]
            self.genre = game_data[3]
            self.title = game_data[1]
            self.release = game_data[6]
            self.platform = game_data[2]
            self.developer = game_data[4]
            self.publisher = game_data[5]


class Review:

    def __init__(self:object, review_data:tuple) -> None:

        self.id = review_data[0]
        self.text = review_data[4]
        self.score = review_data[3]
        self.game_id = review_data[1]
        self.username = review_data[2]
        self.datetime = review_data[5]


class Lenght:

    def __init__(self:object, lenght_data:tuple) -> None:

        self.id = lenght_data[0]
        self.dlcs = lenght_data[5]
        self.game_id = lenght_data[1]
        self.complete = lenght_data[7]
        self.username = lenght_data[2]
        self.platform = lenght_data[3]
        self.multiplayer = lenght_data[6]
        self.main_history = lenght_data[4]


def fetch_recent(mysql:object) -> list:
    """Retorna os dados dos seis jogos recem
    adicionados"""
    cursor = mysql.connection.cursor()
    cursor.execute(
    f'''SELECT *
    FROM game
    WHERE gameTitle LIKE '%forza%'
    # ORDER BY gameId DESC
    LIMIT 6;'''
    )
    game_data = cursor.fetchall()
    game_list = initialize_multiple(Game, game_data)

    return game_list


def search_games(search:str, mysql:object) -> list:
    """Realiza uma busca e retorna os jogos
    os quais contem a palavra buscada no titulo"""
    cursor = mysql.connection.cursor()
    cursor.execute(
        f'''SELECT *
        FROM game
        WHERE gameTitle LIKE "%{search}%";'''
    )
    game_data = cursor.fetchall()

    if game_data:
        game_list = initialize_multiple(Game, game_data)
        return game_list
    

def fetch_game_page(id:int, mysql:object) -> object:
    """Retorna os dados do jogo da tabela game,
    realiza a busca usando o id do jogo na tabela
    reviews e lenght, instancia e inicializa um objeto
    para cada registro encontrado nas respectivas
    tabelas."""
    cursor = mysql.connection.cursor()
    cursor.execute(
        f'''SELECT *
        FROM game 
        WHERE gameId = "{id}";'''
    )
    game_data = cursor.fetchone()
    game = Game(game_data=game_data)

    print(game.title)

    cursor.execute(
        f'''SELECT *
        FROM review
        WHERE reviewGameId = "{game.id}";'''
    )
    review_data = cursor.fetchall()
    game.reviews = initialize_multiple(Lenght, review_data)

    cursor.execute(
        f'''SELECT *
        FROM lenght
        WHERE lenghtGameId = "{game.id}";'''
    )
    lenght_data = cursor.fetchall()
    game.lenghts = initialize_multiple(Lenght, lenght_data)

    return game

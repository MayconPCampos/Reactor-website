from app.tools import initialize_multiple
from datetime import datetime

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
    

    def get_recent_game_list(self, mysql:object) -> list:
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


    def search_games(self, search:str, mysql:object) -> list:
        """Realiza uma busca e retorna os jogos
        os quais contem a palavra procurada no titulo"""
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


    def get_game_page(self, id:int, mysql:object) -> object:
        """Busca os dados do jogo da tabela game e inicializa
        a instancia com esses dados, realiza a busca usando o
        id do jogo na tabela reviews e lenght, instancia e
        inicializa um objeto para cada registro encontrado
        nas respectivas tabelas."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            f'''SELECT *
            FROM game 
            WHERE gameId = "{id}";'''
        )
        game_data = cursor.fetchone()
        self.__init__(game_data=game_data)

        cursor.execute(
            f'''SELECT *
            FROM review
            WHERE reviewGameId = "{self.id}";'''
        )
        review_data = cursor.fetchall()
        self.reviews = initialize_multiple(Review, review_data)

        cursor.execute(
            f'''SELECT *
            FROM lenght
            WHERE lenghtGameId = "{self.id}";'''
        )
        lenght_data = cursor.fetchall()
        self.lenghts = initialize_multiple(Lenght, lenght_data)


class Review:

    def __init__(self:object, review_data=None) -> None:

        if review_data:
            self.id = review_data[0]
            self.text = review_data[3]
            self.score = review_data[2]
            self.game_id = review_data[1]
            self.username = review_data[5]
            self.datetime = review_data[4]


    def post_review(self, title_id:int, username:str, score:float, text:str, mysql:object) -> None:
        """Grava a review de um título enviada pelo usuário
        na tabela reviews no banco de dados"""
        review_date = datetime.now()
        cursor = mysql.connection.cursor()
        cursor.execute(
            f'''INSERT INTO review (
            reviewGameId,
            reviewUsername,
            reviewScore,
            reviewText,
            reviewDate)
            VALUES (
            "{title_id}",
            "{username}",
            "{score}",
            "{text}",
            "{review_date}");
            ''')
        mysql.connection.commit()


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

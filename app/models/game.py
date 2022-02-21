from unittest import result
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
            self.score = game_data[8]
    

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
        nas respectivas tabelas.
        Especificamente na tabela de lenghts traz os
        tempos de jogos com a média calculada para cada
        plataforma e tipo de tempo de jogo
        """
        
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
            f'''SELECT lenghtId,
            lenghtGameId,
            Platform,
            round(sum(mainHistory) / count(mainHistory),1),
            round(sum(dlcs) / count(dlcs),1),
            round(sum(multiplayer) / count(multiplayer),1),
            round(sum(complete) / count(complete),1),
            lenghtUsername
            from lenght
            WHERE lenghtGameId = {self.id}
            GROUP BY Platform;''')
        lenght_data = cursor.fetchall()
        self.lenghts = initialize_multiple(Lenght, lenght_data)


    def update_game_score(self, game_id, mysql):
        """Atualiza a média de nota de um jogo na
        tabela game do banco de dados"""
        
        cursor = mysql.connection.cursor()
        cursor.execute(
            f'''SELECT sum(reviewScore) / count(reviewScore)
            FROM review WHERE reviewGameId = {game_id};'''
        )
        average_score = cursor.fetchone()[0]

        # verifica se já existe nota de review para o titulo
        # caso não exista recebe 0
        if average_score:
            average_score = round(average_score, 1)
        else:
            average_score = 0

        cursor.execute(
            f'''UPDATE game 
            SET gameAverageScore = {average_score}
            WHERE gameId = {game_id};
            ''')
        mysql.connection.commit()


class Review:

    def __init__(self:object, review_data=None) -> None:

        if review_data:
            self.id = review_data[0]
            self.text = review_data[3]
            self.score = review_data[2]
            self.game_id = review_data[1]
            self.username = review_data[5]
            self.datetime = review_data[4]


    def post_review(self, mysql:object) -> None:
        """Grava a review de um título enviada pelo usuário
        na tabela reviews no banco de dados e usa o método
        que atualiza a nota do titulo de jogo"""

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
            "{self.game_id}",
            "{self.username}",
            "{self.score}",
            "{self.text}",
            "{review_date}");
            ''')
        mysql.connection.commit()

        # chama método para atualizar média de nota do jogo
        game = Game()
        game.update_game_score(self.game_id, mysql)

    def check_review_username(self, username, game_id, mysql):
        """Verifica se já existe review de um usuário para
        um mesmo título no banco de dados, retorna False
        caso exista"""
        
        cursor = mysql.connection.cursor()
        cursor.execute(
            f'''SELECT reviewUsername
            FROM review
            WHERE reviewGameId = {game_id}''')
        result = cursor.fetchone()
        
        if result == username or result == None:
            return True
        else:
            return False


class Lenght:

    def __init__(self:object, lenght_data:tuple) -> None:

        self.id = lenght_data[0]
        self.dlcs = lenght_data[4]
        self.game_id = lenght_data[1]
        self.complete = lenght_data[6]
        self.username = lenght_data[7]
        self.platform = lenght_data[2]
        self.multiplayer = lenght_data[5]
        self.main_history = lenght_data[3]


    def post_lenght(self, mysql):
        """Grava os dados de tempo de jogo de um
        no título no banco de dados"""
        
        cursor = mysql.connection.cursor()
        cursor.execute(
            f'''INSERT INTO lenght (
                lenghtGameId,
                lenghtUsername,
                Platform,
                mainHistory,
                dlcs,
                multiplayer,
                complete)
                VALUES (
                    "{self.game_id}",
                    "{self.username}",
                    "{self.platform}",
                    "{self.main_history}",
                    "{self.dlcs}",
                    "{self.multiplayer}",
                    "{self.complete}");
                ''')
        mysql.connection.commit()

from werkzeug.security import generate_password_hash, check_password_hash


class User:

    def __init__(self, **kwargs):
        self.__id = None
        self.__username = None
        self.__email_address = None
        self.__hash_password = None

    @property
    def id(self):
        return self.__id

    @property
    def username(self):
        return self.__username


    def is_registered(self:object, username:str, email:str, mysql:object) -> bool:
        """Realiza uma pesquisa na tabela users 
        no banco de dados com o nome de usuário
        e email, retorna True caso os dados existam
        ou False caso não existam."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            f'''SELECT userName, userEmail 
            FROM users 
            WHERE BINARY "{username}" = BINARY userName
            OR BINARY "{email}" = BINARY userEmail '''
        )
        user_data = cursor.fetchone()
        if user_data:
            return True
        else: 
            return False


    def get_user_info(self:object, mysql:object) -> tuple:
        """Retorna todos os dados de um usuário da tabela 
        users do banco de dados
        """
        cursor = mysql.connection.cursor()
        cursor.execute(
            f'''SELECT * 
            FROM users 
            WHERE BINARY "{self.__username}" = BINARY userName'''
        )
        user_data = cursor.fetchone()
        return user_data

    
    def create_account(self:object, username:str, email:str, password:str, mysql) -> int:
        """Cria uma hash com a senha fornecida pelo usuário,
        inseri os dados do novo usuário na tabela users
        no banco de dados, e retorna o id da nova conta
        """
        self.__username = username
        self.__email = email
        self.__hash_password = generate_password_hash(password)
        
        cursor = mysql.connection.cursor()
        cursor.execute(
            f'''INSERT INTO users (
                userName,
                userEmail,
                userHash
            )
            VALUES (
                "{self.__username}",
                "{self.__email}",
                "{self.__hash_password}"
            );
            '''
        )
        mysql.connection.commit()
        
        user_data = self.get_user_info(mysql)
        self.__id = user_data[0]

        return self.__id


    def login(self:object, username:str, password:str, mysql:object):
        """Realiza uma busca na tabela users através do
        username, se encontrado valida a hash do password
        e retorna o id caso a senha esteja correta, e caso
        não retorna False. Se o username não for encontrado
        na busca retorna False."""
        username = username
        password = password
        cursor = mysql.connection.cursor()
        cursor.execute(
            f'''SELECT userId, userName, userHash 
            FROM users 
            WHERE BINARY "{username}" = BINARY userName;'''
        )
        user_data = cursor.fetchone()
        if not user_data:
            return False
        else:
            self.__id = user_data[0]
            self.__hash_password = user_data[2]
            checked_password = check_password_hash(self.__hash_password, password)

            if checked_password:
                return self.__id
            else:
                return False


class Admin(User):

    def __init__(self:object):

        self.__id = None
        self.__hash_password = None
        super().__init__()

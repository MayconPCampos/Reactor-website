from flask import make_response, session
from functools import wraps


def login_required(func):
    """Decora uma função verificando se
    o há uma sessão de usuário nos cookies,
    caso positivo retorna a função, caso
    negativo retorna uma página com o status
    http unauthorized"""
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        id = session.get("USER_ID")
        if id != None:
            return func(*args, **kwargs)
        else:
            res = make_response("Unauthorized", 401)
            return res
    return wrapper


def initialize_multiple(object, object_data):
    """Recebe um objeto e uma lista de tuplas
    com dados vindos do banco de dados, instancia
    e inicializa um objeto para cada tupla na lista.
    Retorna uma lista com todos os objetos"""
    
    obj_list = []
    for data in object_data:
        new_object = object(data)
        obj_list.append(new_object)

    return obj_list

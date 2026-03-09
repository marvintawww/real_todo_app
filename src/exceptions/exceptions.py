class ItemAlreadyExist(Exception):
    """Объект уже существует"""

    pass


class ItemNotExist(Exception):
    """Объекта не существует"""

    pass


class AuthenticateError(Exception):
    """Ошибка аутентификации"""

    pass

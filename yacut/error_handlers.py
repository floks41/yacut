"""Модуль обработчиков ошибок проекта YaCut."""


from http import HTTPStatus

from flask import jsonify, render_template

from yacut import app, db


class InvalidAPIUsage(Exception):
    """Исключение для функций представлений API"""

    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message, status_code=None):
        """Конструктор класса InvalidAPIUsage принимает на вход
        текст сообщения и статус-код ошибки (необязательно)."""
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        """Метод для сериализации переданного сообщения об ошибке."""
        return dict(message=self.message)


#
@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    """Обработчик кастомного исключения для API.
    Возвращает в ответе текст ошибки и статус-код."""
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error):
    """Обработка ошибки 404 NOT_FOUND с выводом кастомной страницы."""
    return render_template('404.html'), HTTPStatus.NOT_FOUND


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_error(error):
    """Обработка ошибки 500 INTERNAL_SERVER_ERROR
    с выводом кастомной страницы."""
    db.session.rollback()
    return render_template('500.html'), HTTPStatus.INTERNAL_SERVER_ERROR

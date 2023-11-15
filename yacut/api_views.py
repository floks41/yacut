"""Модуль представлений API проекта YaCut."""


import re
from http import HTTPStatus
from string import ascii_letters, digits

from flask import jsonify, request

from yacut import app
from yacut.constants import CUSTOM_ID_REGEXP
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.views import get_new_short_link

VALID_SYMBOL_SET = set((ascii_letters + digits))


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_url(short):
    """Возвращает оргинальный URL на основе короткой ссылки."""
    url_map = URLMap.query.filter_by(short=short).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_id():
    """Создает короткую ссылку, сохраняет объект в модели URLMap.
    Возвращает оригинальный URL короткую ссылку (short_link)."""
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    custom_id = data.get('custom_id')

    if not (
        custom_id is None
        or custom_id == ''
        or re.fullmatch(CUSTOM_ID_REGEXP, custom_id)
    ):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    if URLMap.query.filter_by(short=custom_id).first():
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )

    data = {
        'url': data.get('url'),
        'short_link': get_new_short_link(
            original=data.get('url'), custom_id=custom_id
        ),
    }

    return jsonify(data), HTTPStatus.CREATED

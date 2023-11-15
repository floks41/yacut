"""Модуль представлений проекта YaCut."""


from http import HTTPStatus
from random import choices
from string import ascii_letters, digits

from flask import Markup, abort, flash, redirect, render_template, request
from werkzeug.debug import get_current_traceback

from yacut import app, db
from yacut.constants import GENERATED_LINK_LENGTH
from yacut.forms import URLMapForm
from yacut.models import URLMap


def get_unique_short_id() -> str:
    """Создает уникальное короткое имя, проверяетя уникальность в БД."""

    while True:
        short_name = ''.join(
            choices(ascii_letters + digits, k=GENERATED_LINK_LENGTH)
        )
        if URLMap.query.filter_by(short=short_name).first() is None:
            break

    return short_name


def get_new_short_link(original: str, custom_id: str = None) -> str:
    """Создает запись в модели URLMap на основе аргументов
    original - оргинальный URL, custom_id - опциональное короткое имя.
    Возвращает короткую ссылку, состояющую из адреса хоста сервера
    и короткого имени.
    """
    if custom_id is None or custom_id == '':
        custom_id = get_unique_short_id()

    url_map = URLMap(original=original, short=custom_id)

    # Сохранение объекта модели в БД с перехватом и
    # кастомной обработкой внутренней ошибки сервера 500.
    try:
        db.session.add(url_map)
        db.session.commit()
    except Exception:
        traceback = get_current_traceback(
            skip=1, show_hidden_frames=True, ignore_system_exceptions=False
        )
        traceback.log()
        abort(HTTPStatus.INTERNAL_SERVER_ERROR)

    return f'{request.host_url}{custom_id}'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Функция-представление для главной страницы.
    Обработка формы создания короткой ссылки."""
    form = URLMapForm()

    if form.validate_on_submit():
        custom_id = form.custom_id.data

        if custom_id and URLMap.query.filter_by(short=custom_id).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            flash(f'Имя <{custom_id}> уже занято!')
        else:
            short_link = get_new_short_link(
                original=form.original_link.data, custom_id=custom_id
            )
            flash('Ваша новая ссылка готова:')
            flash(Markup(f'<a href="{short_link}">{short_link}</a>'))

    return render_template('yacut.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def resolve_short_link(short):
    """Разрешает короткую ссылку и возвращает редирект на оригинальный URL."""
    url_map = URLMap.query.filter_by(short=short).first_or_404()
    original_link = url_map.original
    return redirect(original_link, code=HTTPStatus.FOUND)

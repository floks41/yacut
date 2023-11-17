"""Модуль форм проекта YaCut."""


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from yacut.constants import CUSTOM_ID_MAX_LENGTH, CUSTOM_ID_REGEXP


class URLMapForm(FlaskForm):
    """Форма для создания короткой ссылки."""
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'), Length(1, 256)],
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(1, CUSTOM_ID_MAX_LENGTH, message='Не более 16 символов'),
            Optional(),
            Regexp(
                CUSTOM_ID_REGEXP,
                message='Допустимы только буквы a-z, A-Z и цифры 0-9',
            ),
        ],
    )
    submit = SubmitField('Создать')

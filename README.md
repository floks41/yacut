# Проект YaCut — это сервис укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис, на базе фреймворка Flask

### Разработчик (исполнитель):

👨🏼‍💻Олег Чужмаров: https://github.com/floks41

### Технологии
- Python 3.9
- Flask 2.0.2

1. Установка
Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
Применить миграции:

```
flask db upgrade
```
2. Использование (запуск из командной строки в режиме разработки). В каталоге проекта (YACUT).

```
(venv) .../yacut $ flask run
```

3. Функции.
- генерация коротких ссылок и связь их с исходными длинными ссылками,
- переадресация на исходный адрес при обращении к коротким ссылкам,
- на главной странице сервиса можно создать короткую ссылку,

4. API доступен всем желающим включает два эндпоинта:
- /api/id/ — POST-запрос на создание новой короткой ссылки,
- /api/id/<short_id>/ — GET-запрос на получение оригинальной ссылки по указанному короткому идентификатору

5. Код проекта проверен flake8 после линтинга isort и black:

```
isort yacut/.
black yacut/. --line-length 79 --skip-string-normalization
```
### Проект UWSGI фреймворка

Установить WSGI-коннектор Gunicorn

`pip install gunicorn`

Запуск фреймворка

`gunicorn main:application`

Для добавления эндпоинтов требуется добавить в файл
`src/urls.py` собственные сопастовления URL и функции обработчика из файла `src/views.py`


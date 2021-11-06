# Дипломный проект: Онлайн-магазин Настольных игр

<b>Задача:</b> 
1. Приобрести навыки команднной разработки
2. В конце получить рабочий продукт
3. Получить нвавыки разработки на Python

## Установка и развертывание
Первичная установка:
1. Сделать `git clone [repo url]`
2. Активировать виртуальное окружение `venv`, для этого надо использовать `virtualenv`:
Если на машине не установлено ничего из окружения то `python -m pip install --user virtualenv`
Активация окружения:
`source venv/bin/activate`
2. Использовать <b>pip</b> для того чтобы заинсталить необходимые библиотеки `pip3 install -r requirements.txt`
3. В случае успеха зайти в `scr/` и запустить `python3 server.py` (Unix style) 
`python server.py` - (Windows style)

## 07.10.2021 Произведен рефактор
Приложение запускать из директории `Project_Tabletop_game_Shop`

Вводить: `export FLASK_APP=src && export FLASK_ENV=development && flask run
`

## 01.11.2021 Добавлена первичная возможность для деплоя.

Запускать
`waitress-serve --call 'src:create_app'`

[Настройка](https://docs.pylonsproject.org/projects/waitress/en/stable/usage.html "этапы работы")

----------------
Будем использовать Heroky

[Информация по настройке Heroky](https://devcenter.heroku.com/articles/getting-started-with-python?singlepage=true "Настройка Heroky")


<b>Update:</b> Добавление Докер файла

[Установка докера на Debian](https://docs.docker.com/engine/install/debian/#install-using-the-repository "Дока на докер(Деб)")

Работать с докером в виртуальном окружении

`docker build -t [name container] [PATH]` - Создание контейнера

`docker run -d -p [порт локальной машины]:[порт внутри контейнера] [name conrainer]`


---------------
<b>gunicorn</b> - Библиотека позволяющая обслуживать больше одного пользователя.

Создан:`src/wsgi.py`

`--bind=0.0.0.0:5000` - выбор на каком порту
`workers = количество ядер цпу + 1`
`src.wsgi:app` - наименования приложения:функция запуска.

Запуск
`gunicorn --bind=0.0.0.0:5000 --workers 3 src.wsgi:app`


`entrypoint.sh`
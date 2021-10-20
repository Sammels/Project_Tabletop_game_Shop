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
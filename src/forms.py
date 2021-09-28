import typing

from wtforms import Form, TextField, BooleanField, StringField, IntegerField, validators, SelectMultipleField
from models import Category


def get_category() -> typing.List[typing.Tuple[str, str]]:
    """ Запрос всех категорий для поля category в форме ProductForm """
    all_category = Category.query.all()
    category = [(category.name, category.name) for category in all_category]
    return category


class CategoryForm(Form):
    """ Форма добавления категории """
    name = StringField('Категория', [validators.Length(min=4, max=120)])


class ProductForm(Form):
    """ Форма добавления Настольной игры"""
    name = StringField('Наименование настольной игры', [validators.Length(min=4, max=120)])
    title = StringField('Краткое описание настолькой игры', [validators.Length(min=6, max=240)])
    price = IntegerField('Цена', [validators.NumberRange(min=0)])
    image = IntegerField('Изобрацения', [validators.NumberRange(min=0)])
    category = SelectMultipleField('Категории (веберите один или несколько)', coerce=str)
    description = TextField('Описание')
    stock = BooleanField('В наличии')

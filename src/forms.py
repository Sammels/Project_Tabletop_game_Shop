import typing
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError
from wtforms import (
    Form,
    BooleanField,
    StringField,
    IntegerField,
    validators,
    SelectMultipleField,
    FileField,
    PasswordField,
    SubmitField,
    MultipleFileField,
    TextAreaField
)
from .models import Category, User


def get_category(all_category=None) -> typing.List[typing.Tuple[str, str]]:
    """ Запрос всех категорий для поля category в форме ProductForm """

    if all_category is None:
        all_category = Category.query.all()
    category = [(category.name, category.name) for category in all_category]
    return category


class CategoryForm(Form):
    """ Форма добавления категории """


    name = StringField(
        "Категория",
        [validators.Length(min=4, max=120)],
        render_kw={"placeholder": "Введите категорию"},
    )



class ProductForm(Form):
    """ Форма добавления Настольной игры"""
    name = StringField('Наименование настольной игры', [validators.Length(min=4, max=120)])
    title = StringField('Краткое описание настолькой игры', [validators.Length(min=6, max=240)])
    price = IntegerField('Цена', [validators.NumberRange(min=0)])
    image_poster = FileField('Постер')
    image_shots = MultipleFileField('Изображения')
    category = SelectMultipleField('Категории (веберите одну или несколько)', coerce=str)
    description = TextAreaField('Описание')
    stock = BooleanField('В наличии')


class LoginForm(FlaskForm):
    """Форма логина. Наследуется от FlaskForm"""

    username = StringField(
        "Логин",
        validators=[DataRequired()],
        render_kw={"placeholder": "Имя пользователя"},
    )
    password = PasswordField(
        "Пароль", validators=[DataRequired()], render_kw={"placeholder": "Пароль"}
    )
    submit = SubmitField("Подтвердить")


# Форма регистрации
class RegisterForm(FlaskForm):
    username = StringField(
        "Логин",
        validators=[DataRequired()],
        render_kw={"placeholder": "Имя пользователя"},
    )
    password = PasswordField(
        "Пароль",
        validators=[DataRequired()],
        render_kw={"placeholder": "Пароль"},
    )
    submit = SubmitField("Регистрация")

    # # Проверка имени пользователя
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("Это имя пользователя уже занято. Исп. другое")

import typing

from flask_wtf import FlaskForm

from wtforms.validators import DataRequired


from src.models import Category

from wtforms import (
    Form,
    TextAreaField,
    BooleanField,
    StringField,
    IntegerField,
    validators,
    SelectMultipleField,
    FileField,
    MultipleFileField,
    PasswordField,
    SubmitField,
)


def get_category() -> typing.List[typing.Tuple[str, str]]:
    """Запрос всех категорий для поля category в форме ProductForm"""
    all_category = Category.query.all()
    category = [(category.name, category.name) for category in all_category]
    return category


class CategoryForm(Form):
    """Форма добавления категории"""

    name = StringField("Категория", [validators.Length(min=4, max=120)])


class ProductForm(Form):
    """Форма добавления Настольной игры"""

    name = StringField(
        "Наименование настольной игры", [validators.Length(min=4, max=120)]
    )
    title = StringField(
        "Краткое описание настолькой игры", [validators.Length(min=6, max=240)]
    )
    price = IntegerField("Цена", [validators.NumberRange(min=0)])
    image_poster = FileField("Постер")
    image_shots = MultipleFileField("Изображения")
    category = SelectMultipleField(
        "Категории (выберите один или несколько)", coerce=str
    )
    description = TextAreaField("Описание")
    stock = BooleanField("В наличии")


class LoginForm(FlaskForm):
    """Форма логинаю Наследуется от FlaskForm"""

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

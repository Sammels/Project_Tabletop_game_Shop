import os

from flask import Flask, flash, request, render_template, redirect, url_for
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.utils import secure_filename

from .forms import ProductForm, CategoryForm, get_category

# Удалить потом flask_bcrypt
from .db import db_session
from .models import Product, Category, User, PosterImage, ShotsImage
from .forms import LoginForm, RegisterForm


# Заводим Фласк
def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(512)

    login_manager = LoginManager()
    login_manager.init_app(app)
    # Присваиваем функцию для работы с логином.
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/admin/add-category/', methods=['GET', 'POST'])
    def add_category():
        """Добавление категорий в БД"""
        form = CategoryForm(request.form)
        if request.method == 'POST' and form.validate():
            category = Category(name=form.name.data)
            db_session.add(category)
            db_session.commit()
            return redirect('/admin/add-category/')
        return render_template('add_category.html', form=form)

    @app.route("/add-product", methods=["GET", "POST"])
    def add_product():
        """
        Добавление настольной игры в БД
        """
        form = ProductForm(request.form)
        form.category.choices = get_category()
        if request.method == 'POST' and form.validate():
            product = Product(name=form.name.data,
                              title=form.title.data,
                              price=form.price.data,
                              description=form.description.data,
                              stock=form.stock.data)

            poster = request.files[form.image_poster.name]
            poster_name = secure_filename(poster.filename)
            mimetype_poster = poster.mimetype
            img_poster = PosterImage(img=poster.read(), name=poster_name, mimetype=mimetype_poster)
            product.image_poster.append(img_poster)

            shots = request.files.getlist(form.image_shots.name)
            for image in shots:
                image_name = secure_filename(image.filename)
                mimetype = image.mimetype
                img = ShotsImage(img=image.read(), name=image_name, mimetype=mimetype)
                product.image_shots.append(img)
            for name in form.category.data:
                category = Category.query.filter_by(name=name).all()
                product.category.append(category[0])
            db_session.add(product)
            db_session.commit()
            return redirect('/add-product')
        return render_template('add_product.html', form=form)

    @app.route('/')
    def all_product():
        """ Рендер всех товаров"""

        q = request.args.get('q')
        if q:
            products = Product.query.filter(Product.name.contains(q) |
                                            Product.title.contains(q))
        else:
            products = Product.query.all()
        return render_template('all_product.html', products=products)

    @app.route('/category/<name>/')
    def search_categories(name):
        category = Category.query.filter_by(name=name).first()
        if category is None:
            flash('Категория не найдена')
            return redirect('/')
        else:
            products = category.products
            return render_template('all_product.html', products=products)

    @app.context_processor
    def all_categories():
        categories = Category.query.all()
        return dict(categories=categories)

    @app.route("/login", methods=["GET", "POST"])
    def login() -> str:
        """Логин форма"""
        if current_user.is_authenticated:
            return redirect(url_for("all_product"))
        title = "Логин"
        form = LoginForm()
        return render_template("login.html", form=form, title=title)

    # Переделать
    @app.route("/reg", methods=["GET", "POST"])
    def registration() -> str:
        """Форма регистрации"""
        form = RegisterForm()
        if form.validate_on_submit():
            new_user = User(username=form.username.data, role="user")
            new_user.set_password(form.password.data)
            db_session.add(new_user)
            db_session.commit()
            return redirect(url_for("all_product"))

        return render_template("register.html", form=form)

    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()

        if form.validate_on_submit():
            user = User.query.filter(User.username == form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Успешный вход')
                return redirect(url_for('all_product'))
        flash('Не очень успещный вход')
        return redirect(url_for("login"))

    @app.route("/logout")
    def logout():
        """Выход"""
        logout_user()
        flash("Успешно вышел")
        return redirect(url_for("all_product"))

    @app.route("/admin")
    @login_required
    def admin_index():
        """Админ"""
        if current_user.is_admin:
            return "Страница администратора"
        else:
            return "Не админ"

    return app

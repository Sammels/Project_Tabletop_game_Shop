import os

from flask import Flask, flash, request, render_template, redirect, url_for, Response, session
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
from .models import Product, Category, User, PosterImage, ShotsImage, category_product, Cart
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
    @login_required
    def add_category():
        """Добавление категорий в БД"""
        form = CategoryForm(request.form)
        if request.method == 'POST' and form.validate():
            category = Category(name=form.name.data)
            db_session.add(category)
            db_session.commit()
            flash('Категория успешно добавлена')
            return redirect('/admin/add-category/')
        return render_template('add_category.html', form=form)

    @app.route('/admin/add-product/', methods=['GET', 'POST'])
    @login_required
    def add_product():
        """Добавление настольной игры в БД"""
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
            flash('Товар успешно добавлен')
            return redirect('/admin/add-product/')
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

    @app.route('/admin/')
    @login_required
    def admin():
        products = Product.query.all()
        return render_template('admin.html', products=products)

    @app.route('/admin/product-delete/<int:product_id>')
    @login_required
    def product_delete(product_id):
        product = Product.query.filter(Product.id.contains(product_id)).first()
        db_session.delete(product)
        db_session.commit()
        flash('Товар успешно удален')
        return redirect('/admin/')

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
                session['user_id'] = user.id
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

    # TODO Подумать как сдеать одну функцию с get_poster_img и get_shots_img
    @app.route('/poster-img/<int:img_id>/')
    def get_poster_img(img_id):
        """ Функция вывода изображения (Постер товара)"""
        img = PosterImage.query.filter_by(id=img_id).first()
        if not img:
            return 'Img Not Found!', 404
        return Response(img.img, mimetype=img.mimetype)

    @app.route('/shots-img/<int:img_id>')
    def get_shots_img(img_id):
        """ Функция вывода изображения (Дополнительные снимки товара)"""
        img = ShotsImage.query.filter_by(id=img_id).first()
        if not img:
            return 'Img Not Found!', 404
        return Response(img.img, mimetype=img.mimetype)

    @app.route('/admin/update-product/<int:product_id>/', methods=['GET', 'POST'])
    def update_product(product_id):
        """Изменение настольной игры в БД"""
        product = Product.query.filter(Product.id.contains(product_id)).first()
        form = ProductForm(request.form)
        form.category.choices = get_category()
        if request.method == 'POST' and form.validate():
            product.name = form.name.data
            product.title = form.title.data
            product.price = form.price.data
            product.description = form.description.data
            product.stock = form.stock.data
            poster = request.files[form.image_poster.name]
            poster_name = secure_filename(poster.filename)
            if poster_name:
                for image in product.image_poster:
                    image_poster_delete = PosterImage.query.filter(PosterImage.id.contains(image.id)).first()
                    db_session.delete(image_poster_delete)
                mimetype_poster = poster.mimetype
                img_poster = PosterImage(img=poster.read(), name=poster_name, mimetype=mimetype_poster)
                product.image_poster.append(img_poster)
            shots_all = request.files.getlist(form.image_shots.name)
            if shots_all[0].filename:
                for shot in product.image_shots:
                    image_shots_delete = ShotsImage.query.filter(ShotsImage.id.contains(shot.id)).first()
                    db_session.delete(image_shots_delete)
                for shots in shots_all:
                    shot_name = secure_filename(shots.filename)
                    mimetype_poster = shots.mimetype
                    img_shots = ShotsImage(img=shots.read(), name=shot_name, mimetype=mimetype_poster)
                    product.image_shots.append(img_shots)
            if form.category.data:
                product.category.clear()
                for name in form.category.data:
                    category = Category.query.filter_by(name=name).all()
                    product.category.append(category[0])
            db_session.commit()
            flash('Товар успешно изменен')
            return redirect(f'/admin/update-product/{product_id}')
        elif request.method == 'GET':
            form.name.data = product.name
            form.title.data = product.title
            form.price.data = product.price
            form.description.data = product.description
            form.stock.data = product.stock
        return render_template('update_product.html', form=form, product=product)

    @app.route('/add-cart/<product_id>', methods=['GET', 'POST'])
    @login_required
    def add_cart(product_id):
        user_id = session['user_id']
        cart_user = Cart.query.filter_by(user_id=user_id, in_oder=True, for_anonymous_user=False).first()
        if not cart_user:
            user_cart = Cart(user_id=user_id, for_anonymous_user=False)
            db_session.add(user_cart)
            db_session.commit()
        if request.method == 'POST':
            product = Product.query.filter_by(id=product_id).first()
            cart_user.total_product += 1
            cart_user.total_price += product.price
            cart_user.product.append(product)
            session[product.name] = session.get(product.name, 0) + 1
            db_session.commit()

        return redirect(url_for("all_product"))

    @app.route('/cart/')
    @login_required
    def cart():
        user_id = session['user_id']
        cart_user = Cart.query.filter_by(user_id=user_id, in_oder=True, for_anonymous_user=False).first()
        return render_template('cart.html', cart=cart_user)


    @app.route('/delete_product_cart/<product_id>', methods=['GET', 'POST'])
    @login_required
    def delete_product_cart(product_id):
        user_id = session['user_id']
        cart_user = Cart.query.filter_by(user_id=user_id, in_oder=True, for_anonymous_user=False).first()
        if request.method == 'POST':
            product = Product.query.filter_by(id=product_id).first()
            cart_user.total_product -= 1
            cart_user.total_price -= product.price
            cart_user.product.remove(product)
            db_session.commit()
        return redirect('/cart')

    return app

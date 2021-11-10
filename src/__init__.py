import os
from flask import Flask, flash, request, render_template, redirect, url_for, Response, current_app
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.utils import secure_filename
from .forms import ProductForm, CategoryForm, get_category, LoginForm, RegisterForm
# Удалить потом flask_bcrypt
from .models import Product, Category, User, PosterImage, ShotsImage, category_product, Cart, ProductCart, db


# Заводим Фласк


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.secret_key = os.urandom(512)
    login_manager = LoginManager()
    login_manager.init_app(app)
    # Присваиваем функцию для работы с логином.
    login_manager.login_view = "login"

    with app.app_context():
        db.init_app(app)
        db.create_all()

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
            db.session.add(category)
            db.session.commit()
            flash('Категория успешно добавлена')
            return redirect(url_for("add_category"))
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
            img_poster = PosterImage(
                img=poster.read(), name=poster_name, mimetype=mimetype_poster
            )
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
            db.session.add(product)
            db.session.commit()
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
        if product is None:
            flash('Товар не найдена')
            return redirect('/admin/')
        db.session.delete(product)
        db.session.commit()
        flash('Товар успешно удален')
        return redirect('/admin/')

    @app.context_processor
    def all_categories():
        categories = Category.query.all()
        return dict(categories=categories)

    @app.route("/img/<class_img>/<int:img_id>")
    def serve_img(class_img, img_id):
        if class_img == 'poster':
            img = PosterImage.query.filter_by(id=img_id).first()
        elif class_img == 'shot':
            img = ShotsImage.query.filter_by(id=img_id).first()

        if not img:
            return "Img Not Found!", 404
        return Response(img.img, mimetype=img.mimetype)

    @app.route("/login", methods=["GET", "POST"])
    def login() -> str:
        """Логин форма"""
        if current_user.is_authenticated:
            return redirect(url_for("all_product"))
        title = "Логин"
        form = LoginForm()
        return render_template("login.html", form=form, title=title)

    @app.route("/reg", methods=["GET", "POST"])
    def registration() -> str:
        """Форма регистрации"""
        form = RegisterForm()
        if form.validate_on_submit():
            new_user = User(username=form.username.data, role="user")
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("all_product"))

        return render_template("register.html", form=form)

    @app.route("/process-login", methods=["POST"])
    def process_login():
        """Процесс логина"""
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter(User.username == form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Успешный вход')
                return redirect(url_for('all_product'))
        flash('Не очень успещный вход')
        return redirect(url_for("login"))

    @app.route("/about_prod", methods=["GET", "POST"])
    def about_product():
        """Функция страницы товара"""
        title = "Страница товара"
        product_information = Product.query.order_by(Product.id).all()
        return render_template("product.html", product_information=product_information, title=title)

    @app.route("/about_prod/<int:id>")
    def about_product_id(id):
        """
            Запрос ID
        """
        product = Product.query.get(id)
        return render_template("product_id.html", product=product)

    @app.route("/logout")
    def logout():
        """Выход"""
        logout_user()
        flash("Успешно вышел")
        return redirect(url_for("all_product"))

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
                    db.session.delete(image_poster_delete)
                mimetype_poster = poster.mimetype
                img_poster = PosterImage(img=poster.read(), name=poster_name, mimetype=mimetype_poster)
                product.image_poster.append(img_poster)
            shots_all = request.files.getlist(form.image_shots.name)
            if shots_all[0].filename:
                for shot in product.image_shots:
                    image_shots_delete = ShotsImage.query.filter(ShotsImage.id.contains(shot.id)).first()
                    db.session.delete(image_shots_delete)
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
            db.session.commit()
            flash('Товар успешно изменен')
            return redirect(f'/admin/update-product/{product_id}')
        elif request.method == 'GET':
            form.name.data = product.name
            form.title.data = product.title
            form.price.data = product.price
            form.description.data = product.description
            form.stock.data = product.stock
        return render_template('update_product.html', form=form, product=product)

    @app.route('/cart/')
    def cart():
        user_id = current_user.get_id()
        if not user_id:
            user_id = request.remote_addr
        cart_user = Cart.query.filter_by(user_id=user_id,
                                         in_oder=True).first()
        product_cart = getattr(cart_user, 'product', None)
        if product_cart:
            cart_user.total_product = sum([product.qty for product in cart_user.product])
            cart_user.total_price = sum([product.qty * product.add_product_cart.price for product in cart_user.product])
            db.session.commit()

        return render_template('cart.html', cart=cart_user)

    def create_cart(user_id):
        user_cart = Cart(user_id=user_id)
        db.session.add(user_cart)
        db.session.commit()

    @app.route('/add-cart/<int:product_id>', methods=['GET', 'POST'])
    def add_cart(product_id):
        if request.method == 'POST':
            user_id = current_user.get_id()
            if not user_id:
                user_id = request.remote_addr
            cart_user = Cart.query.filter_by(user_id=user_id,
                                             in_oder=True).first()
            if not cart_user:
                create_cart(user_id)
                cart_user = Cart.query.filter_by(user_id=user_id,
                                                 in_oder=True, ).first()
            product_cart = ProductCart.query.filter_by(product_cart=product_id, user_id=user_id).first()
            if not product_cart:
                add_product_cart = ProductCart(product_cart=product_id, qty=1, user_id=user_id)
                db.session.add(add_product_cart)
                db.session.commit()
                product_cart = ProductCart.query.filter_by(product_cart=product_id, user_id=user_id).first()
            else:
                product_cart.qty += 1
                db.session.commit()
                product_cart = ProductCart.query.filter_by(product_cart=product_id, user_id=user_id).first()
            cart_user.product.append(product_cart)
            db.session.commit()
        return redirect(url_for("all_product"))

    @app.route('/delete_product_cart/<int:product_id>', methods=['GET', 'POST'])
    def delete_product_cart(product_id):
        user_id = current_user.get_id()
        if not user_id:
            user_id = request.remote_addr
        cart_user = Cart.query.filter_by(user_id=user_id, in_oder=True).first()
        if request.method == 'POST':
            product_cart = ProductCart.query.filter_by(user_id=user_id, product_cart=product_id).first()
            cart_user.total_product -= product_cart.qty
            cart_user.total_price -= product_cart.add_product_cart.price * product_cart.qty
            cart_user.product.remove(product_cart)
            db.session.commit()
        return redirect('/cart')

    # Временные функции

    @app.route("/action")
    def action():
        """Акции проводимые магазином"""
        title = "Акции в магазине"
        return render_template("actions.html", title=title)

    @app.route("/about_us")
    def about():
        """Информация о нас """
        title = "Информация о нас."
        return render_template("about_us.html", title=title)

    # Доставка и оплата
    @app.route("/pay")
    def pay_form():
        """Способы оплаты"""
        title = "Способы оплаты"
        return render_template("pay_form.html", title=title)

    @app.route("/deliver")
    def deliver_form():
        """Способы доставки"""
        title = "Доставка товаров"
        return render_template("deliver_form.html", title=title)

    @app.route("/shop_address")
    def shop_address():
        """Адреса магазинов"""
        title = "Адреса магазинов"
        return render_template("shop_address.html", title=title)

    # Покупателям

    @app.route("/game_choose")
    def choose_the_game():
        """Подобрать игру"""
        title = "Подбор игры"
        return render_template("choose_game.html", title=title)

    @app.route("/help")
    def site_help():
        """Помощь"""
        title = "Подбор игры"
        return render_template("helps.html", title=title)

    @app.route("/bonus")
    def bonus_programm():
        """Бонусная программа"""
        title = "Наши бонусные программы"
        return render_template("bonus.html", title=title)

    @app.route("/shop")
    def shop_info():
        """Бонусная программа"""
        title = "О магазине"
        return render_template("about_shop.html", title=title)

    @app.route("/news")
    def shop_news():
        """Новости"""
        title = "Магазинные сплетни"
        return render_template("shop_news.html", title=title)   
   
    @app.route("/contact")
    def shop_contacts():
        """Новости"""
        title = "Контактные данные"
        return render_template("contacts.html", title=title)

    @app.route("/another_link")
    def redirect_links():
        """Новости"""
        title = "Куда-то"
        return render_template("redirect_to.html", title=title)
      

    @app.route('/change-quantity/<int:product_id>/<minusplus>', methods=['GET', 'POST'])
    def change_quantity(product_id, minusplus):
        user_id = current_user.get_id()
        if not user_id:
            user_id = request.remote_addr
        product_cart = ProductCart.query.filter_by(user_id=user_id, product_cart=product_id).first()
        if minusplus == 'minus':
            product_cart.qty -= 1
        elif minusplus == 'plus':
            product_cart.qty += 1
        db.session.commit()
        return redirect('/cart')

    return app

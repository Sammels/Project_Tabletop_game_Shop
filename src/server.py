import os

from flask import Flask, request, render_template, redirect, Response, flash
from werkzeug.utils import secure_filename

from forms import ProductForm, CategoryForm, get_category
from db import db_session
from models import Product, Category, PosterImage, ShotsImage

# Заводим Фласк
app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/add-category', methods=['GET', 'POST'])
def add_category():
    """
    Добавление категорий в БД
    """
    form = CategoryForm(request.form)
    if request.method == 'POST' and form.validate():
        category = Category(name=form.name.data)
        db_session.add(category)
        db_session.commit()
        return redirect('/add-category')
    return render_template('add_category.html', form=form)


@app.route('/add-product', methods=['GET', 'POST'])
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
        return redirect(url_for('add-product'))
    return render_template(url_for('add_product'), form=form)


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


@app.route('/img/<int:img_id>')
def serve_img(img_id):
    img = PosterImage.query.filter_by(id=img_id).first()
    if not img:
        return 'Img Not Found!', 404
    return Response(img.img, mimetype=img.mimetype)


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


# Заводим через дебаг
if __name__ == '__main__':
    app.run(debug=True)

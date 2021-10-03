import os

from flask import Flask, request, render_template, redirect, Response
from werkzeug.utils import secure_filename

from forms import ProductForm, CategoryForm, get_category
from db import db_session
from models import Product, Category, Image

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

        images = request.files.getlist(form.image.name)
        for image in images:
            image_name = secure_filename(image.filename)
            mimetype = image.mimetype
            img = Image(img=image.read(), name=image_name, mimetype=mimetype)
            print(img.img)
            product.image.append(img)
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
    products = Product.query.all()
    return render_template('all_product.html', products=products)


@app.route('/<int:id>')
def get_img(id):
    img = Image.query.filter_by(id=id).first()
    return img.img


# Заводим через дебаг
if __name__ == '__main__':
    app.run(debug=True)

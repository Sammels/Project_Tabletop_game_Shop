import os

from flask import Flask, request, render_template, redirect
from forms import ProductForm, CategoryForm, get_category
from db import db_session
from models import Product, Category

# Заводим Фласк
app = Flask(__name__)
app.secret_key = os.urandom(24)


# Путь страницы
@app.route('/')
def index() -> str:
    # Титульник
    page_title = "Рай Настольщика"
    return render_template('index.html', title=page_title)


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
        product = Product(name=form.name.data, title=form.title.data,
                          price=form.price.data, image=form.image.data,
                          description=form.description.data, stock=form.stock.data)
        for name in form.category.data:
            category = Category.query.filter_by(name=name).all()
            product.category.append(category[0])
        db_session.add(product)
        db_session.commit()
        return redirect('/add-product')
    return render_template('add_product.html', form=form)


@app.route('/all-product')
def all_product():
    """ Рендер всех товаров"""
    products = Product.query.all()
    return render_template('all_product.html', products=products)


# Заводим через дебаг
if __name__ == '__main__':
    app.run(debug=True)

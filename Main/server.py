from flask import Flask, render_template, request

# Заводим Фласк
app = Flask(__name__)


# Путь страницы
@app.route('/')
def index() -> 'html':
    # Титульник
    page_title = "Рай Настольщика"
    return render_template('index.html', title=page_title)

# Логин и регистрация
@app.route('/login', methods=['GET', 'POST'])
def login() -> 'html':
    """
    Раздумья над реализацией логирования
    
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    return render_template('login.html', error=error)
    """
    page_title = "Регистрация"
    name = "Имя"
    email = "Эл почта"
    return render_template('LogAndReg.html', title=page_title)


# Заводим через дебаг
if __name__ == '__main__':
    app.run(debug=True)

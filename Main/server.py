from flask import Flask, render_template

# Заводим Фласк
app = Flask(__name__)

# Путь страницы
@app.route('/')
def index() -> str:
    # Титульник
    page_title = "Рай Настольщика"
    return render_template('index.html', title=page_title)

# Заводим через дебаг
if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template # type: ignore
from model import *
from data import items

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ecommerce.db"
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', items = items)

@app.route('/404')
def error():
    return render_template('404.html')

@app.route('/login')
def login():
    return render_template('loginPage.html')

@app.route('/register')
def register():
    return render_template('RegistryPage.html')

@app.route('/ProfilePage')
def ProfilePage():
    return render_template('ProfilePage.html')

@app.route('/ProductSingle')
def product_single():
    return render_template('ProductSingle.html', items = items)

if __name__ == "__main__":
    app.run(debug=True)



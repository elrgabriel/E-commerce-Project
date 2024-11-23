from flask import Flask, render_template, request,redirect,url_for, flash # type: ignore
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

@app.route('/login', methods = ["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["login_email"]
        password = request.form["login_password"]

        search_user = Users.query.filter_by(user_email = email).first()
        
        print(search_user.user_email)
        print(search_user.user_password)
        print(email)
        print(password)
        if search_user.user_email == email and search_user.user_password == password:
            print("You're are logged in")
            return redirect(url_for("ProfilePage"))
    return render_template('loginPage.html')

@app.route('/register', methods = ["GET", "POST"])
def register():

    if request.method == "POST":
        email = request.form["register_email"]
        user_re_email = request.form["register_re_email"]
        password = request.form["register_password"]
        user_re_password = request.form["register_re_password"]
        nome = request.form["register_nome"]
        apelido = request.form["register_apelido"]
        morada = request.form["register_morada"]
        distrito = request.form["register_distrito"]

        new_user = Users.query.filter_by(user_email = email).first()
        
        if new_user is None:

            check_email = email == user_re_email
            check_password = password == user_re_password

            print(f"Check email: {check_email}, Check password: {check_password}")

            if check_email and check_password:
                add_user = Users(
                    user_email = email,
                    user_password = password,
                    user_name = nome,
                    user_last_name = apelido,
                    user_address = morada,
                    user_district = distrito
                    )
                db.session.add(add_user)
                db.session.commit()
                print("Registo Bem Sucedido!")
                return redirect(url_for("ProfilePage"))
            else:
                print("Email ou password não correspondem.")
        else:
            print("Usuário já registado")
    return render_template('RegistryPage.html')

@app.route('/ProfilePage')
def ProfilePage():
    return render_template('ProfilePage.html')

@app.route('/ProductSingle')
def product_single():
    return render_template('ProductSingle.html', items = items)

if __name__ == "__main__":
    
    app.run(debug=True)


